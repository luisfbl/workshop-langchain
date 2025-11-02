import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, override

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
from utils.progress_tracker import ProgressTracker


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

        # Estado
        self.is_running = False
        self.observer = None
        self.current_test_running = False

    def start(self):
        console.clear()

        console.print("[yellow]🔑 Verificando API key...[/yellow]")
        try:
            api_key = self.api_manager.get_api_key()
            console.print("[green]✅ API key carregada![/green]\n")

            level_emoji = "🟢" if self.user_level == "easy" else "🟡"
            level_name = "FÁCIL" if self.user_level == "easy" else "MÉDIO"
            console.print(f"{level_emoji} [bold]Modo: {level_name}[/bold]")
            console.print(f"[dim]Você está usando exercícios do nível {self.user_level}[/dim]\n")
        except Exception as e:
            console.print(f"[red]❌ Erro com API key: {e}[/red]")
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

        # Monitora day1/easy, day1/medium, day2/easy, day2/medium
        for day_dir in ["day1", "day2"]:
            for level_dir in ["easy", "medium"]:
                watch_dir = self.exercises_dir / day_dir / level_dir
                if watch_dir.exists():
                    self.observer.schedule(event_handler, str(watch_dir), recursive=False)
                    console.print(f"[dim]Monitorando: {day_dir}/{level_dir}[/dim]")

        self.observer.start()
        console.print("[green]👀 Watcher iniciado! Modificações serão detectadas automaticamente.[/green]\n")

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
            "reset": self._cmd_reset,
            "next": self._cmd_next,
            "prev": self._cmd_prev,
            "quit": self._cmd_quit,
            "exit": self._cmd_quit,
            "stats": self._cmd_statistics,
        }

        if cmd in commands:
            commands[cmd](args)
        else:
            console.print(f"[red]❌ Comando desconhecido: {cmd}[/red]")
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
  test <num>       - Roda testes de um exercício específico
  reset <num>      - Reseta exercício para estado original
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
            self.run_tests(current_ex)
        else:
            try:
                ex_num = int(args[0])
                if 1 <= ex_num <= 7:
                    self.run_tests(ex_num)
                else:
                    console.print("[red]❌ Número de exercício inválido (1-7)[/red]")
            except ValueError:
                console.print("[red]❌ Use: test <número>[/red]")

    def _cmd_reset(self, args):
        """Reseta exercício"""
        console.print("[yellow]⚠️  Função de reset ainda não implementada[/yellow]")

    def _cmd_next(self, args):
        """Vai para próximo exercício"""
        current = self.progress.get_current_exercise()
        if self.progress.is_exercise_completed(current):
            if current < 7:
                console.print(f"[green]✅ Avançando para exercício {current + 1}[/green]")
            else:
                console.print("[yellow]🎉 Você já completou todos os exercícios![/yellow]")
        else:
            console.print("[yellow]⚠️  Complete o exercício atual primeiro[/yellow]")

    def _cmd_prev(self, args):
        """Volta para exercício anterior"""
        current = self.progress.get_current_exercise()
        if current > 1:
            prev_ex = current - 1
            ex_name = self.progress.EXERCISES[prev_ex]["name"]
            console.print(f"[cyan]Exercício {prev_ex}: {ex_name}[/cyan]")
            console.print("[dim]Você pode visualizar, mas não pode re-submeter.[/dim]")
        else:
            console.print("[yellow]Você já está no primeiro exercício[/yellow]")

    def _cmd_quit(self, args):
        """Sai do workshop"""
        console.print("\n[cyan]👋 Até logo! Seu progresso foi salvo.[/cyan]")
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

            # 2. Usa Pyright via subprocess (rápido!)
            try:
                import subprocess
                import shutil

                # Verifica se pyright está instalado
                pyright_path = shutil.which('pyright')
                if not pyright_path:
                    # Pyright não instalado - usa apenas verificação básica
                    return {"success": True, "errors": []}

                # Roda Pyright com timeout de 3 segundos
                result = subprocess.run(
                    ['pyright', '--outputjson', str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=3
                )

                # Parse JSON output
                if result.stdout:
                    import json
                    try:
                        output = json.loads(result.stdout)

                        # Pyright retorna diagnósticos
                        if 'generalDiagnostics' in output:
                            for diag in output['generalDiagnostics']:
                                severity = diag.get('severity', 'error')
                                message = diag.get('message', '')
                                line = diag.get('range', {}).get('start', {}).get('line', 0) + 1

                                # Filtra apenas erros (não warnings)
                                if severity == 'error':
                                    # Traduz mensagens comuns
                                    if 'is not defined' in message or 'Cannot find' in message:
                                        # Extrai nome da variável
                                        import re
                                        match = re.search(r'"([^"]+)"', message)
                                        var_name = match.group(1) if match else "variável"
                                        errors.append(f"[red]error[/red]: nome não definido `{var_name}`")
                                        errors.append(f" --> {file_path.name}:{line}")
                                    else:
                                        errors.append(f"[red]error[/red]: {message}")
                                        errors.append(f" --> {file_path.name}:{line}")

                        if errors:
                            return {"success": False, "errors": errors}

                    except json.JSONDecodeError:
                        # Se não conseguir parsear JSON, ignora Pyright
                        pass

            except subprocess.TimeoutExpired:
                # Timeout - usa verificação básica
                return {"success": True, "errors": []}
            except FileNotFoundError:
                # Pyright não encontrado - usa verificação básica
                return {"success": True, "errors": []}
            except Exception:
                # Qualquer outro erro - usa verificação básica
                return {"success": True, "errors": []}

            return {"success": True, "errors": []}

        except Exception as e:
            errors.append(f"[red]error[/red]: {str(e)}")
            return {"success": False, "errors": errors}
    def _is_exercise_ready(self, exercise_num: int) -> bool:
        """
        Verifica se o exercício está pronto para testar.
        Retorna False se encontrar 'I AM NOT DONE' no arquivo.
        """
        # Determina o diretório do exercício baseado no nível do usuário
        if exercise_num <= 4:
            day = "day1"
        else:
            day = "day2"

        # Usa o nível do usuário (easy ou medium)
        level_dir = self.user_level

        # Monta caminho do arquivo do exercício com nível
        exercise_file = self.exercises_dir / day / level_dir / f"ex{exercise_num:02d}_*.py"

        # Encontra o arquivo (pode ter nomes diferentes)
        from glob import glob
        matches = glob(str(exercise_file))

        if not matches:
            # Se não encontrar no diretório de nível, tenta o antigo (fallback)
            exercise_file_old = self.exercises_dir / day / f"ex{exercise_num:02d}_*.py"
            matches = glob(str(exercise_file_old))

            if not matches:
                console.print(f"[yellow]⚠️  Exercício {exercise_num} não encontrado[/yellow]")
                return True

        exercise_path = Path(matches[0])

        try:
            content = exercise_path.read_text(encoding='utf-8')
            # Verifica se contém "I AM NOT DONE" (com ou sem #)
            if "I AM NOT DONE" in content:
                return False
            return True
        except Exception as e:
            console.print(f"[yellow]⚠️  Erro ao ler exercício: {e}[/yellow]")
            # Em caso de erro, permite testar
            return True

    def run_tests(self, exercise_num: int):
        """Executa testes para um exercício"""
        if self.current_test_running:
            console.print("[yellow]⏳ Aguarde o teste atual terminar...[/yellow]")
            return

        self.current_test_running = True

        try:
            # Verifica se pode acessar exercício
            if not self.progress.can_access_exercise(exercise_num):
                console.print(f"[red]❌ Exercício {exercise_num} bloqueado. Complete os anteriores primeiro.[/red]")
                return

            # Verifica se o exercício está marcado como "I AM NOT DONE"
            if not self._is_exercise_ready(exercise_num):
                ex_name = self.progress.EXERCISES[exercise_num]["name"]
                console.print(f"\n[yellow]📝 Exercício {exercise_num}: {ex_name}[/yellow]")
                console.print("[dim]O exercício ainda contém 'I AM NOT DONE'.[/dim]")
                console.print("[dim]Quando terminar de implementar, remova esse comentário para rodar os testes.[/dim]\n")
                return

            # Verifica rate limit de API
            can_use, remaining, message = self.rate_limiter.check_limit()
            if not can_use:
                console.print(f"[red]{message}[/red]")
                return

            # Mostra que está rodando
            ex_name = self.progress.EXERCISES[exercise_num]["name"]
            console.print(f"\n[yellow]🧪 Testando Exercício {exercise_num}: {ex_name}...[/yellow]")

            # Prepara ambiente
            api_key = self.api_manager.get_api_key()
            env = setup_environment_for_test(api_key)

            # Adiciona nível do usuário ao ambiente para os testes
            env['WORKSHOP_LEVEL'] = self.user_level

            # Roda testes
            test_file = self.project_root / "exercises" / "tests" / f"test_ex{exercise_num:02d}.py"

            if not test_file.exists():
                console.print(f"[red]❌ Arquivo de teste não encontrado: {test_file}[/red]")
                return

            start_time = time.time()

            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                env=env,
                timeout=30,
                cwd=str(self.project_root)
            )

            elapsed = time.time() - start_time

            # Processa resultado
            passed = result.returncode == 0

            if passed:
                console.print(f"[bold green]✅ TODOS OS TESTES PASSARAM! ({elapsed:.1f}s)[/bold green]")
                self.progress.save_test_result(exercise_num, True)
                self.rate_limiter.increment_usage(exercise_num)
            else:
                console.print(f"[bold red]❌ TESTES FALHARAM ({elapsed:.1f}s)[/bold red]\n")
                console.print("[dim]Saída dos testes:[/dim]")
                console.print(result.stdout)
                if result.stderr:
                    console.print("[dim]Erros:[/dim]")
                    console.print(result.stderr)

                self.progress.save_test_result(exercise_num, False)

        except subprocess.TimeoutExpired:
            console.print("[red]❌ Timeout - teste demorou mais de 30 segundos[/red]")
        except Exception as e:
            console.print(f"[red]❌ Erro ao executar testes: {e}[/red]")
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
                console.print(f"[green]✅ Compilação bem-sucedida[/green]")

                if self.workshop._is_exercise_ready(ex_num):
                    console.print(f"[bold yellow]🚀 Exercício {ex_num} pronto para testar![/bold yellow]")
                    console.print(f"[dim]   Executando testes...[/dim]\n")
                    self.workshop.run_tests(ex_num)
                else:
                    console.print(f"[dim]💡 Para testar: remova 'I AM NOT DONE' ou digite: test {ex_num}[/dim]")
                    console.print()
            else:
                console.print(f"[red]❌ Compilação falhou[/red]\n")
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
        console.print(f"[red]❌ Erro ao conectar com Firebase: {e}[/red]")
        return 1

    auth = Authenticator(firebase)
    session = auth.require_auth()

    if not session:
        console.print("[red]❌ Você precisa fazer login primeiro. Execute: python main.py[/red]")
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
