import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.cloud.client import Client
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from utils.firebase_client import FirebaseClient


console = Console()

EXERCISES = {
    1: {"name": "Primeiro Agente", "day": 1, "difficulty": "easy", "estimated_minutes": 20},
    2: {"name": "Múltiplas Ferramentas", "day": 1, "difficulty": "medium", "estimated_minutes": 25},
    3: {"name": "Agente com Memória", "day": 1, "difficulty": "medium", "estimated_minutes": 30},
    4: {"name": "Analisador de Código", "day": 1, "difficulty": "hard", "estimated_minutes": 35},
    5: {"name": "Saída Estruturada", "day": 2, "difficulty": "medium", "estimated_minutes": 25},
    6: {"name": "Gerador de Código", "day": 2, "difficulty": "hard", "estimated_minutes": 40},
    7: {"name": "Orquestrador Multi-Agente", "day": 2, "difficulty": "hard", "estimated_minutes": 45},
}
LOCAL_CACHE_FILE = Path.home() / ".langchain_workshop" / "progress_cache.json"


class ProgressTracker:
    firebase: FirebaseClient
    user_id: str
    local_cache: dict[str, bool]

    def __init__(self, firebase_client: FirebaseClient, user_id: str):
        self.firebase = firebase_client
        self.user_id = user_id
        self.local_cache = {}
        self._load_cache()

    def _load_cache(self):
        if LOCAL_CACHE_FILE.exists():
            try:
                self.local_cache = json.loads(LOCAL_CACHE_FILE.read_text())
            except Exception as _:
                self.local_cache = {}

    def _convert_firestore_to_json(self, obj):
        if obj is None:
            return None
        if isinstance(obj, dict):
            return {k: self._convert_firestore_to_json(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._convert_firestore_to_json(item) for item in obj]
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return obj

    def _save_cache(self):
        LOCAL_CACHE_FILE.parent.mkdir(exist_ok=True, parents=True)
        serializable_cache = self._convert_firestore_to_json(self.local_cache)
        LOCAL_CACHE_FILE.write_text(json.dumps(serializable_cache, indent=2))

    def get_progress(self) -> dict[str, Any]:
        try:
            progress = self.firebase.get_progress(self.user_id)
            if progress:
                self.local_cache = progress
                self._save_cache()
                return progress
        except Exception as e:
            console.print(f"[yellow]⚠️  Erro ao carregar do Firebase, usando cache local: {e}[/yellow]")

        return self.local_cache or self._get_default_progress()

    def _get_default_progress(self) -> dict[str, Any]:
        return {
            "current_exercise": 1,
            "completed_exercises": [],
            "exercise_attempts": {},
            "hints_used": {},
            "start_time": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "test_results": {},
        }

    def get_current_exercise(self) -> int:
        progress = self.get_progress()
        return progress.get("current_exercise", 1)

    def is_exercise_completed(self, exercise_num: int) -> bool:
        progress = self.get_progress()
        return exercise_num in progress.get("completed_exercises", [])

    def can_access_exercise(self, exercise_num: int) -> bool:
        if exercise_num == 1:
            return True

        return self.is_exercise_completed(exercise_num - 1)

    def mark_complete(self, exercise_num: int):
        try:
            self.firebase.mark_exercise_complete(self.user_id, exercise_num)

            progress = self.get_progress()
            if exercise_num not in progress.get("completed_exercises", []):
                progress.setdefault("completed_exercises", []).append(exercise_num)
                progress["current_exercise"] = exercise_num + 1
                self.local_cache = progress
                self._save_cache()

            self._show_completion_message(exercise_num)
        except Exception as e:
            console.print(f"[red]❌ Erro ao marcar exercício completo: {e}[/red]")

    def increment_attempt(self, exercise_num: int):
        try:
            self.firebase.increment_attempt(self.user_id, exercise_num)
        except Exception as e:
            console.print(f"[yellow]⚠️  Erro ao incrementar tentativas: {e}[/yellow]")

    def save_test_result(self, exercise_num: int, passed: bool):
        try:
            self.firebase.save_test_result(self.user_id, exercise_num, passed)
            self.increment_attempt(exercise_num)

            if passed:
                self.mark_complete(exercise_num)
        except Exception as e:
            console.print(f"[yellow]⚠️  Erro ao salvar resultado: {e}[/yellow]")

    def _show_completion_message(self, exercise_num: int):
        ex_info = EXERCISES.get(exercise_num, {})
        ex_name = ex_info.get("name", f"Exercício {exercise_num}")

        progress = self.get_progress()
        completed_count = len(progress.get("completed_exercises", []))
        total = len(EXERCISES)

        message = f"[bold green]🎉 Parabéns! Você completou: {ex_name}[/bold green]\n\n"
        message += f"Progresso: {completed_count}/{total} exercícios completos"

        if completed_count == total:
            message += "\n\n[bold yellow]🏆 WORKSHOP COMPLETO! 🏆[/bold yellow]"
            message += "\nVocê dominou LangChain Agents!"
        elif exercise_num == 4:
            message += "\n\n[bold cyan]✨ Dia 1 completo! ✨[/bold cyan]"
            message += "\nVamos para os exercícios avançados do Dia 2!"

        console.print(Panel(message, border_style="green", padding=1))

    def show_status(self):
        progress = self.get_progress()

        console.print("\n" + "="*60)
        console.print("[bold cyan]📊 SEU PROGRESSO[/bold cyan]")
        console.print("="*60 + "\n")

        current_ex = progress.get("current_exercise", 1)
        completed = progress.get("completed_exercises", [])
        completed_count = len(completed)
        total = len(EXERCISES)

        console.print(f"[bold]Exercício Atual:[/bold] {current_ex}")
        console.print(f"[bold]Completos:[/bold] {completed_count}/{total}")
        console.print(f"[bold]Progresso:[/bold] {int(completed_count/total*100)}%\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=3)
        table.add_column("Nome", width=25)
        table.add_column("Dia", width=4)
        table.add_column("Status", width=12)
        table.add_column("Tentativas", width=10)

        for ex_num in sorted(EXERCISES.keys()):
            ex_info = EXERCISES[ex_num]

            if ex_num in completed:
                status = "[green]✅ Completo[/green]"
            elif ex_num == current_ex:
                status = "[yellow]▶️  Atual[/yellow]"
            elif self.can_access_exercise(ex_num):
                status = "[cyan]🔓 Disponível[/cyan]"
            else:
                status = "[dim]🔒 Bloqueado[/dim]"

            # Tentativas
            attempts = progress.get("exercise_attempts", {}).get(str(ex_num), 0)
            attempts_str = str(attempts) if attempts > 0 else "-"

            table.add_row(
                str(ex_num),
                ex_info["name"],
                f"Dia {ex_info['day']}",
                status,
                attempts_str
            )

        console.print(table)
        console.print()

    def show_hints_summary(self):
        progress = self.get_progress()
        hints_used = progress.get("hints_used", {})

        if not hints_used:
            console.print("[dim]Você ainda não usou nenhuma dica.[/dim]\n")
            return

        console.print("\n[bold]💡 Dicas Usadas:[/bold]\n")

        for ex_str, levels in hints_used.items():
            ex_num = int(ex_str)
            ex_name = EXERCISES.get(ex_num, {}).get("name", f"Exercício {ex_num}")
            console.print(f"  {ex_name}: {len(levels)}/4 dicas ({levels})")

        console.print()

    def show_statistics(self):
        progress = self.get_progress()

        console.print("\n" + "="*60)
        console.print("[bold cyan]📈 ESTATÍSTICAS[/bold cyan]")
        console.print("="*60 + "\n")

        start_time = progress.get("start_time")
        if start_time:
            start = datetime.fromisoformat(start_time)
            elapsed = datetime.now() - start
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            console.print(f"[bold]Tempo Total:[/bold] {hours}h {minutes}min")

        attempts = progress.get("exercise_attempts", {})
        total_attempts = sum(attempts.values())
        console.print(f"[bold]Total de Tentativas:[/bold] {total_attempts}")

        hints = progress.get("hints_used", {})
        total_hints = sum(len(h) for h in hints.values())
        console.print(f"[bold]Dicas Usadas:[/bold] {total_hints}")

        completed = len(progress.get("completed_exercises", []))
        if total_attempts > 0:
            success_rate = (completed / len(EXERCISES)) * 100
            console.print(f"[bold]Taxa de Conclusão:[/bold] {success_rate:.1f}%")

        console.print()

    def show_welcome_message(self):
        user = self.firebase.get_user(self.user_id)
        username = user.get("username", "Estudante")
        level = user.get("level", "medium")

        progress = self.get_progress()
        current_ex = progress.get("current_exercise", 1)
        completed = len(progress.get("completed_exercises", []))

        welcome = f"[bold cyan]Bem-vindo(a) de volta, {username}![/bold cyan]\n\n"
        welcome += f"Nível: [yellow]{level.upper()}[/yellow]\n"
        welcome += f"Progresso: {completed}/7 exercícios completos\n"
        welcome += f"Exercício atual: #{current_ex} - {EXERCISES[current_ex]['name']}\n\n"
        welcome += "[dim]Digite 'help' ou '?' para ver comandos disponíveis[/dim]"

        console.print(Panel(welcome, border_style="cyan", padding=1))
        console.print()

    def export_progress_report(self, output_path: Path | None = None) -> dict[str, Any]:
        progress = self.get_progress()
        user = self.firebase.get_user(self.user_id)

        report = {
            "user": {
                "username": user.get("username"),
                "level": user.get("level"),
            },
            "progress": progress,
            "exercises": EXERCISES,
            "generated_at": datetime.now().isoformat(),
        }

        if output_path is None:
            output_path = Path(f"progress_report_{self.user_id}.json")

        output_path.write_text(json.dumps(report, indent=2))
        console.print(f"[green]✅ Relatório exportado: {output_path}[/green]")

        return report
