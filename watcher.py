import subprocess
import sys
import time
import warnings
from pathlib import Path
from typing import Optional, override

# Silencia warning de deprecação do pkg_resources (dependência do gcloud)
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from utils.api_key_manager import APIKeyManager, RateLimiter, setup_environment_for_test
from utils.auth import Authenticator
from utils.firebase_client import FirebaseClient
from utils.hints import HintManager
from utils.progress_tracker import ProgressTracker, EXERCISES
from utils.exercise_manager import ExerciseManager


console = Console()


class WorkshopSession:
    def __init__(self, session_data: dict, firebase: FirebaseClient):
        self.session = session_data
        self.user_id = session_data["user_id"]
        self.username = session_data["username"]
        self.firebase = firebase

        self.api_manager = APIKeyManager(firebase)
        self.rate_limiter = RateLimiter(firebase, self.user_id)
        self.progress = ProgressTracker(firebase, self.user_id)
        self.hints = HintManager(firebase, self.user_id)

        self.project_root = Path(__file__).parent
        self.exercises_dir = self.project_root / "exercises"

        user_data = self.firebase.get_user(self.user_id)
        self.user_level = user_data.get("level", "medium") if user_data else "medium"
        self.progress.set_user_level(self.user_level)

        # Gerenciador de exercícios
        self.exercise_manager = ExerciseManager(self.project_root)

        # Estado
        self.is_running = False
        self.observer = None
        self.current_test_running = False

    def start(self):
        console.clear()

        # Configura exercícios do nível do usuário (apenas se necessário)
        if not self.exercise_manager.are_exercises_configured(self.user_level):
            console.print("[cyan] Configurando exercícios...[/cyan]")
            if self.exercise_manager.setup_user_exercises(self.user_level):
                console.print("[green] Exercícios configurados![/green]\n")
            else:
                console.print("[yellow]  Aviso: Erro ao configurar exercícios[/yellow]\n")

        console.print("[yellow] Verificando API key...[/yellow]")
        try:
            api_key = self.api_manager.get_api_key()
            console.print("[green] API key carregada![/green]\n")

            level_emoji = "" if self.user_level == "easy" else ""
            level_name = "FÁCIL" if self.user_level == "easy" else "MÉDIO"
            console.print(f"{level_emoji} [bold]Modo: {level_name}[/bold]")
            console.print(f"[dim]Você está usando exercícios do nível {self.user_level}[/dim]\n")
        except Exception as e:
            console.print(f"[red] Erro com API key: {e}[/red]")
            return

        # Mostra boas-vindas
        self.progress.show_welcome_message()

        # Inicia file watcher
        self.is_running = True
        self._start_file_watcher()

        # Loop de comandos
        self._command_loop()

    def _start_file_watcher(self):
        """Inicia monitoramento de arquivos"""
        event_handler = ExerciseWatcher(self)
        self.observer = Observer()

        # Monitora day1 e day2 (exercícios já foram filtrados por nível)
        for day_dir in ["day1", "day2"]:
            watch_dir = self.exercises_dir / day_dir
            if watch_dir.exists():
                self.observer.schedule(event_handler, str(watch_dir), recursive=True)

        self.observer.start()

    def _command_loop(self):
        """Loop principal de comandos"""
        console.print("[dim]Digite 'help' para ver comandos disponíveis.[/dim]\n")

        while self.is_running:
            try:
                command = console.input("[bold cyan]workshop>[/bold cyan] ").strip().lower()

                if not command:
                    continue

                self._handle_command(command)

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'quit' para sair[/yellow]")
            except EOFError:
                break

    def _handle_command(self, command: str):
        """Processa comandos do usuário"""
        parts = command.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        commands = {
            "help": self._cmd_help,
            "?": self._cmd_help,
            "status": self._cmd_status,
            "s": self._cmd_status,
            "hint": self._cmd_hint,
            "h": self._cmd_hint,
            "test": self._cmd_test,
            "run": self._cmd_run,
            "r": self._cmd_run,
            "reset": self._cmd_reset,
            "restore": self._cmd_restore,
            "next": self._cmd_next,
            "prev": self._cmd_prev,
            "quit": self._cmd_quit,
            "exit": self._cmd_quit,
            "stats": self._cmd_statistics,
        }

        if cmd in commands:
            commands[cmd](args)
        else:
            console.print(f"[red] Comando desconhecido: {cmd}[/red]")
            console.print("[dim]Digite 'help' para ver comandos disponíveis.[/dim]")

    def _cmd_help(self, args):
        """Mostra ajuda"""
        help_text = """
[bold cyan]Comandos Disponíveis:[/bold cyan]

[bold]Geral:[/bold]
  help, ?          - Mostra esta ajuda
  status, s        - Mostra seu progresso atual
  stats            - Mostra estatísticas detalhadas
  quit, exit       - Sai do workshop (salva progresso)

[bold]Exercícios:[/bold]
  hint, h          - Pede próxima dica para exercício atual
  test <num>       - Roda testes de um exercício específico (força execução)
  run, r <num>     - Executa o arquivo do exercício (sem rodar testes)
  reset <num>      - Reseta exercício para estado original
  restore [num]    - Restaura soluções salvas do Firebase ( apaga código atual!)
  next             - Vai para próximo exercício (se atual completo)
  prev             - Volta para exercício anterior (apenas visualizar)

[bold]Dicas:[/bold]
  - Salve o arquivo do exercício para rodar testes automaticamente
  - Use dicas com sabedoria - você tem 4 por exercício
  - Exercícios devem ser completados em ordem (1→2→3...)
  - Todos os testes devem passar para avançar
        """
        console.print(Panel(help_text, border_style="cyan", padding=1))

    def _cmd_status(self, args):
        """Mostra status"""
        self.progress.show_status()
        self.progress.show_hints_summary()

    def _cmd_hint(self, args):
        """Pede dica"""
        current_ex = self.progress.get_current_exercise()

        success, hint_text, level = self.hints.get_next_hint(current_ex)

        if success:
            console.print(hint_text)
        else:
            console.print(f"[yellow]{hint_text}[/yellow]")

    def _cmd_test(self, args):
        """Roda testes manualmente"""
        if not args:
            current_ex = self.progress.get_current_exercise()
            self.run_tests(current_ex, force=True)
        else:
            try:
                ex_num = int(args[0])
                if 1 <= ex_num <= 8:
                    self.run_tests(ex_num, force=True)
                else:
                    console.print("[red] Número de exercício inválido (1-8)[/red]")
            except ValueError:
                console.print("[red] Use: test <número>[/red]")

    def _cmd_run(self, args):
        """Executa o arquivo do exercício diretamente"""
        if not args:
            current_ex = self.progress.get_current_exercise()
            self.run_exercise_file(current_ex)
        else:
            try:
                ex_num = int(args[0])
                if 1 <= ex_num <= 8:
                    self.run_exercise_file(ex_num)
                else:
                    console.print("[red] Número de exercício inválido (1-8)[/red]")
            except ValueError:
                console.print("[red] Use: run <número>[/red]")

    def _cmd_reset(self, args):
        """Reseta exercício"""
        console.print("[yellow]  Função de reset ainda não implementada[/yellow]")

    def _cmd_restore(self, args):
        """Restaura soluções salvas do Firebase"""
        from rich.prompt import Confirm

        # Determina quais exercícios restaurar
        if args:
            try:
                ex_num = int(args[0])
                if not (1 <= ex_num <= 8):
                    console.print("[red] Número de exercício inválido (1-8)[/red]")
                    return
                exercises_to_restore = [ex_num]
            except ValueError:
                console.print("[red] Use: restore [número] (sem número restaura todos completos)[/red]")
                return
        else:
            # Restaura todos os exercícios completos
            progress = self.progress.get_progress()
            completed = progress.get("completed_exercises", [])
            if not completed:
                console.print("[yellow]  Você ainda não completou nenhum exercício.[/yellow]")
                console.print("[dim]Não há soluções salvas para restaurar.[/dim]")
                return
            exercises_to_restore = completed

        # Aviso e confirmação
        console.print("\n[bold red]  ATENÇÃO: OPERAÇÃO DESTRUTIVA [/bold red]\n")
        console.print("[yellow]Esta operação irá:[/yellow]")
        console.print("  • [red]APAGAR[/red] todo o código atual dos exercícios selecionados")
        console.print("  • Substituir pelos códigos salvos no Firebase (suas soluções anteriores)")
        console.print("  • [bold]Não há como desfazer esta operação[/bold]\n")

        if len(exercises_to_restore) == 1:
            ex_num = exercises_to_restore[0]
            try:
                ex_info = self.progress.get_exercise_info(ex_num)
                ex_name = ex_info["name"]
            except KeyError:
                ex_name = f"Exercício {ex_num}"
            console.print(f"[cyan]Será restaurado: {ex_name} (#{ex_num})[/cyan]\n")
        else:
            console.print(f"[cyan]Serão restaurados {len(exercises_to_restore)} exercícios:[/cyan]")
            for ex_num in sorted(exercises_to_restore):
                try:
                    ex_info = self.progress.get_exercise_info(ex_num)
                    ex_name = ex_info["name"]
                    console.print(f"  • #{ex_num} - {ex_name}")
                except KeyError:
                    console.print(f"  • #{ex_num}")
            console.print()

        confirmed = Confirm.ask(
            "[bold]Você tem certeza que deseja continuar?[/bold]",
            default=False
        )

        if not confirmed:
            console.print("[cyan]Operação cancelada.[/cyan]")
            return

        # Restaura exercícios
        console.print("\n[yellow] Restaurando soluções...[/yellow]\n")

        restored_count = 0
        not_found_count = 0
        error_count = 0

        for ex_num in sorted(exercises_to_restore):
            try:
                # Busca solução salva
                solution_code = self.firebase.get_exercise_solution(self.user_id, ex_num)

                if solution_code is None:
                    try:
                        ex_info = self.progress.get_exercise_info(ex_num)
                        ex_name = ex_info["name"]
                    except KeyError:
                        ex_name = f"Exercício {ex_num}"
                    console.print(f"[yellow]  Solução não encontrada: {ex_name} (#{ex_num})[/yellow]")
                    not_found_count += 1
                    continue

                # Obtém informações do exercício
                try:
                    ex_info = self.progress.get_exercise_info(ex_num)
                except KeyError:
                    console.print(f"[red] Exercício {ex_num} não está configurado[/red]")
                    error_count += 1
                    continue

                # Restaura usando ExerciseManager
                success = self.exercise_manager.restore_solution(
                    exercise_num=ex_num,
                    code=solution_code,
                    day=ex_info["day"],
                    file_name=ex_info["file"]
                )

                if success:
                    ex_name = ex_info["name"]
                    console.print(f"[green] Restaurado: {ex_name} (#{ex_num})[/green]")
                    restored_count += 1
                else:
                    console.print(f"[red] Erro ao restaurar exercício {ex_num}[/red]")
                    error_count += 1

            except Exception as e:
                console.print(f"[red] Erro ao processar exercício {ex_num}: {e}[/red]")
                error_count += 1

        # Resumo
        console.print(f"\n[bold cyan]Resumo da Restauração:[/bold cyan]")
        console.print(f"  • Restaurados: [green]{restored_count}[/green]")
        if not_found_count > 0:
            console.print(f"  • Não encontrados: [yellow]{not_found_count}[/yellow]")
        if error_count > 0:
            console.print(f"  • Erros: [red]{error_count}[/red]")
        console.print()

    def _cmd_next(self, args):
        """Vai para próximo exercício"""
        current = self.progress.get_current_exercise()
        if self.progress.is_exercise_completed(current):
            if current < 7:
                console.print(f"[green] Avançando para exercício {current + 1}[/green]")
            else:
                console.print("[yellow] Você já completou todos os exercícios![/yellow]")
        else:
            console.print("[yellow]  Complete o exercício atual primeiro[/yellow]")

    def _cmd_prev(self, args):
        """Volta para exercício anterior"""
        current = self.progress.get_current_exercise()
        if current > 1:
            prev_ex = current - 1
            ex_name = EXERCISES[prev_ex]["name"]
            console.print(f"[cyan]Exercício {prev_ex}: {ex_name}[/cyan]")
            console.print("[dim]Você pode visualizar, mas não pode re-submeter.[/dim]")
        else:
            console.print("[yellow]Você já está no primeiro exercício[/yellow]")

    def _cmd_quit(self, args):
        """Sai do workshop"""
        console.print("\n[cyan] Até logo! Seu progresso foi salvo.[/cyan]")
        self.stop()

    def _cmd_statistics(self, args):
        """Mostra estatísticas"""
        self.progress.show_statistics()

    def _compile_check(self, file_path: Path) -> dict:
        """
        Verificação de compilação usando Pyright (super rápido!)
        Retorna: {"success": bool, "errors": List[str]}
        """
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # 1. Verifica sintaxe Python básica primeiro (instantâneo)
            try:
                compile(code, file_path.name, 'exec')
            except SyntaxError as e:
                errors.append(f"[red]error[/red]: sintaxe inválida")
                errors.append(f" --> {file_path.name}:{e.lineno}:{e.offset}")
                errors.append(f"  |")
                if e.text:
                    errors.append(f"  | {e.text.rstrip()}")
                    if e.offset:
                        errors.append(f"  | {' ' * (e.offset - 1)}^ {e.msg}")
                return {"success": False, "errors": errors}

            # 2. Pyright desabilitado - causa muitos falsos positivos
            # Apenas verificação de sintaxe Python é suficiente

            return {"success": True, "errors": []}

        except Exception as e:
            errors.append(f"[red]error[/red]: {str(e)}")
            return {"success": False, "errors": errors}
    def _is_exercise_ready(self, exercise_num: int) -> bool:
        """
        Verifica se o exercício está pronto para testar.
        Retorna False se encontrar 'I AM NOT DONE' no arquivo.
        """
        try:
            ex_info = self.progress.get_exercise_info(exercise_num)
        except KeyError:
            console.print(f"[yellow]  Exercício {exercise_num} não está configurado[/yellow]")
            return True

        day_dir = self.exercises_dir / f"day{ex_info['day']}"
        exercise_path = day_dir / f"{ex_info['file']}.py"

        if not exercise_path.exists():
            console.print(f"[yellow]  Arquivo do exercício {exercise_num} não encontrado ({exercise_path})[/yellow]")
            return True

        try:
            content = exercise_path.read_text(encoding='utf-8')
            # Verifica se contém "I AM NOT DONE" (com ou sem #)
            if "I AM NOT DONE" in content:
                return False
            return True
        except Exception as e:
            console.print(f"[yellow]  Erro ao ler exercício: {e}[/yellow]")
            # Em caso de erro, permite testar
            return True

    def run_exercise_file(self, exercise_num: int):
        """Executa o arquivo do exercício diretamente (sem testes)"""
        try:
            ex_info = self.progress.get_exercise_info(exercise_num)
        except KeyError:
            console.print(f"[red] Exercício {exercise_num} não encontrado[/red]")
            return

        day_dir = self.exercises_dir / f"day{ex_info['day']}"
        exercise_path = day_dir / f"{ex_info['file']}.py"

        if not exercise_path.exists():
            console.print(f"[red] Arquivo não encontrado: {exercise_path}[/red]")
            return

        ex_name = EXERCISES[exercise_num]["name"]
        console.print(f"\n[yellow] Executando Exercício {exercise_num}: {ex_name}...[/yellow]")
        console.print(f"[dim]Arquivo: {exercise_path}[/dim]\n")

        # Prepara ambiente
        api_key = self.api_manager.get_api_key()
        env = setup_environment_for_test(api_key)
        env['WORKSHOP_LEVEL'] = self.user_level

        module_name = f"exercises.day{ex_info['day']}.{ex_info['file']}"

        try:
            result = subprocess.run(
                [sys.executable, "-m", module_name],
                capture_output=True,
                text=True,
                env=env,
                timeout=60,
                cwd=str(self.project_root)
            )

            # Mostra output
            if result.stdout:
                console.print(result.stdout)

            if result.stderr:
                console.print("[red]Erros:[/red]")
                console.print(result.stderr)

            if result.returncode != 0:
                console.print(f"\n[red] Programa terminou com código de erro: {result.returncode}[/red]")
            else:
                console.print(f"\n[green] Execução concluída[/green]")

        except subprocess.TimeoutExpired:
            console.print("[red] Timeout - execução demorou mais de 60 segundos[/red]")
        except Exception as e:
            console.print(f"[red] Erro ao executar: {e}[/red]")

        console.print()

    def run_tests(self, exercise_num: int, force: bool = False):
        """Executa testes para um exercício

        Args:
            exercise_num: Número do exercício
            force: Se True, força execução mesmo se já estiver completo
        """
        if self.current_test_running:
            console.print("[yellow]⏳ Aguarde o teste atual terminar...[/yellow]")
            return

        self.current_test_running = True

        try:
            # Verifica se pode acessar exercício
            if not self.progress.can_access_exercise(exercise_num):
                console.print(f"[red] Exercício {exercise_num} bloqueado. Complete os anteriores primeiro.[/red]")
                return

            # Verifica se já está completo (só se não forçado)
            if not force and self.progress.is_exercise_completed(exercise_num):
                ex_name = EXERCISES[exercise_num]["name"]
                console.print(f"\n[green] Exercício {exercise_num}: {ex_name}[/green]")
                console.print("[dim]Este exercício já está completo.[/dim]")
                console.print(f"[dim]Use 'test {exercise_num}' para forçar a execução dos testes novamente.[/dim]\n")
                return

            # Verifica se o exercício está marcado como "I AM NOT DONE"
            if not self._is_exercise_ready(exercise_num):
                ex_name = EXERCISES[exercise_num]["name"]
                console.print(f"\n[yellow] Exercício {exercise_num}: {ex_name}[/yellow]")
                console.print("[dim]O exercício ainda contém 'I AM NOT DONE'.[/dim]")
                console.print("[dim]Quando terminar de implementar, remova esse comentário para rodar os testes.[/dim]\n")
                return

            # Verifica rate limit de API
            can_use, remaining, message = self.rate_limiter.check_limit()
            if not can_use:
                console.print(f"[red]{message}[/red]")
                return

            # Mostra que está rodando
            ex_name = EXERCISES[exercise_num]["name"]
            console.print(f"\n[yellow] Testando Exercício {exercise_num}: {ex_name}...[/yellow]")

            # Prepara ambiente
            api_key = self.api_manager.get_api_key()
            env = setup_environment_for_test(api_key)

            # Adiciona nível do usuário ao ambiente para os testes
            env['WORKSHOP_LEVEL'] = self.user_level

            # Roda testes
            test_file = self.project_root / "exercises" / "tests" / f"test_ex{exercise_num:02d}.py"

            if not test_file.exists():
                console.print(f"[red] Arquivo de teste não encontrado: {test_file}[/red]")
                return

            start_time = time.time()

            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-v", "-s", "--tb=short"],
                capture_output=True,
                text=True,
                env=env,
                timeout=60,
                cwd=str(self.project_root)
            )

            elapsed = time.time() - start_time

            # Processa resultado
            passed = result.returncode == 0

            if passed:
                console.print(f"[bold green] TODOS OS TESTES PASSARAM! ({elapsed:.1f}s)[/bold green]")

                # Mostrar output dos testes (perguntas e respostas da IA)
                if result.stdout and len(result.stdout.strip()) > 0:
                    console.print("\n[dim]Detalhes da execução:[/dim]")
                    console.print(result.stdout)

                self.progress.save_test_result(exercise_num, True)
                self.rate_limiter.increment_usage(exercise_num)

                # Salva a solução no Firebase
                try:
                    ex_info = self.progress.get_exercise_info(exercise_num)
                    day_dir = self.exercises_dir / f"day{ex_info['day']}"
                    exercise_path = day_dir / f"{ex_info['file']}.py"
                    
                    if exercise_path.exists():
                        solution_code = exercise_path.read_text(encoding='utf-8')
                        self.firebase.save_exercise_solution(self.user_id, exercise_num, solution_code)
                        console.print("[dim] Solução salva no Firebase[/dim]")
                except Exception as e:
                    console.print(f"[yellow]  Aviso: Não foi possível salvar a solução: {e}[/yellow]")
            else:
                console.print(f"[bold red] TESTES FALHARAM ({elapsed:.1f}s)[/bold red]\n")
                console.print("[dim]Saída dos testes:[/dim]")
                console.print(result.stdout)
                if result.stderr:
                    console.print("[dim]Erros:[/dim]")
                    console.print(result.stderr)

                self.progress.save_test_result(exercise_num, False)

        except subprocess.TimeoutExpired:
            console.print("[red] Timeout - teste demorou mais de 60 segundos[/red]")
        except Exception as e:
            console.print(f"[red] Erro ao executar testes: {e}[/red]")
        finally:
            self.current_test_running = False

    def stop(self):
        """Para sessão"""
        self.is_running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()


class ExerciseWatcher(FileSystemEventHandler):
    workshop: WorkshopSession
    last_modified: dict[Path, float]
    debounce_seconds: int

    def __init__(self, workshop: WorkshopSession):
        self.workshop = workshop
        self.last_modified = {}
        self.debounce_seconds = 2

    @override
    def on_modified(self, event: FileSystemEvent):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if not file_path.name.startswith("ex") or not file_path.name.endswith(".py"):
            return

        now = time.time()
        if file_path in self.last_modified:
            if now - self.last_modified[file_path] < self.debounce_seconds:
                return

        self.last_modified[file_path] = now

        try:
            ex_num = int(file_path.name[2:4])

            console.print(f"\n[cyan]Detectada mudança no exercício {ex_num}[/cyan]")
            console.print(f"[dim]   Compiling {file_path.name}...[/dim]")

            compilation_result = self.workshop._compile_check(file_path)

            if compilation_result["success"]:
                console.print(f"[green] Compilação bem-sucedida[/green]")

                if self.workshop._is_exercise_ready(ex_num):
                    console.print(f"[bold yellow] Exercício {ex_num} pronto para testar![/bold yellow]")
                    console.print(f"[dim]   Executando testes...[/dim]\n")
                    self.workshop.run_tests(ex_num)
                else:
                    console.print(f"[dim] Para testar: remova 'I AM NOT DONE' ou digite: test {ex_num}[/dim]")
                    console.print()
            else:
                console.print(f"[red] Compilação falhou[/red]\n")
                for error in compilation_result["errors"]:
                    console.print(error)
                console.print(f"\n[red]error: could not compile `{file_path.name}`[/red]")
                console.print()

        except ValueError:
            pass


def main():
    try:
        firebase = FirebaseClient()
    except Exception as e:
        console.print(f"[red] Erro ao conectar com Firebase: {e}[/red]")
        return 1

    auth = Authenticator(firebase)
    session = auth.require_auth()

    if not session:
        console.print("[red] Você precisa fazer login primeiro. Execute: python main.py[/red]")
        return 1

    workshop = WorkshopSession(session, firebase)
    workshop.start()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Workshop interrompido[/yellow]")
        sys.exit(0)
