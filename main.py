import sys
import warnings
from pathlib import Path
from typing import Any

# Silencia warning de deprecação do pkg_resources (dependência do gcloud)
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt

from utils.auth import Authenticator
from utils.exercise_manager import ExerciseManager
from utils.firebase_client import FirebaseClient

console = Console()


def show_banner():
    banner = """
[bold cyan]╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🤖  LANGCHAIN AGENTS WORKSHOP  🤖                  ║
║                                                           ║
║           Aprenda a Criar Agentes Inteligentes           ║
║              com LangChain e Python                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝[/bold cyan]
    """
    console.print(banner)


def run_initial_quiz() -> str:
    console.print("\n[bold yellow]📋 AVALIAÇÃO INICIAL[/bold yellow]\n")
    console.print("Responda 5 perguntas para determinarmos o melhor nível para você.\n")

    score = 0

    console.print(
        "[bold]1. Você já usou APIs de LLM (OpenAI, Anthropic, etc.) antes?[/bold]"
    )
    q1 = Prompt.ask("   Resposta", choices=["sim", "nao", "s", "n"], default="nao")
    if q1 in ["sim", "s"]:
        score += 3

    console.print("\n[bold]2. Qual seu nível de familiaridade com LangChain?[/bold]")
    console.print("   1 - Nunca ouvi falar")
    console.print("   2 - Já ouvi falar mas nunca usei")
    console.print("   3 - Já usei algumas vezes")
    console.print("   4 - Uso frequentemente")
    q2 = IntPrompt.ask("   Escolha (1-4)", default=1)
    score += max(0, q2 - 1)

    console.print(
        "\n[bold]3. Como você avalia seu conhecimento de Python async/await?[/bold]"
    )
    console.print("   Escala de 1 (iniciante) a 5 (expert)")
    q3 = IntPrompt.ask("   Nota (1-5)", default=3)
    if q3 >= 4:
        score += 2
    elif q3 >= 3:
        score += 1

    console.print(
        "\n[bold]4. Você entende o conceito de 'function calling' em LLMs?[/bold]"
    )
    q4 = Prompt.ask(
        "   Resposta",
        choices=["sim", "nao", "mais-ou-menos", "s", "n", "m"],
        default="nao",
    )
    if q4 in ["sim", "s"]:
        score += 3
    elif q4 in ["mais-ou-menos", "m"]:
        score += 1

    console.print("\n[bold]5. Você já construiu algum agente de IA antes?[/bold]")
    q5 = Prompt.ask("   Resposta", choices=["sim", "nao", "s", "n"], default="nao")
    if q5 in ["sim", "s"]:
        score += 3

    console.print(f"\n[dim]Pontuação: {score}/14[/dim]\n")

    if score <= 7:
        level = "easy"
        message = (
            "[bold green]Nível recomendado: FÁCIL[/bold green]\n\n"
            "Este nível oferece:\n"
            "  • Mais código inicial (scaffolding)\n"
            "  • Comentários detalhados\n"
            "  • Explicações passo-a-passo\n"
            "  • Exercícios mais guiados"
        )
    else:
        level = "medium"
        message = (
            "[bold yellow]Nível recomendado: MÉDIO[/bold yellow]\n\n"
            "Este nível oferece:\n"
            "  • Menos código inicial\n"
            "  • Mais desafios\n"
            "  • Maior liberdade de implementação\n"
            "  • Foco em boas práticas"
        )

    console.print(Panel(message, border_style="cyan", padding=1))

    change = Confirm.ask("\nDeseja mudar o nível?", default=False)
    if change:
        choice = Prompt.ask(
            "Escolha o nível", choices=["easy", "medium", "facil", "medio"]
        )
        if choice in ["easy", "facil"]:
            level = "easy"
        else:
            level = "medium"

    return level


def register_flow(auth: Authenticator, firebase: FirebaseClient):
    console.print("\n[bold cyan]📝 REGISTRO DE NOVO USUÁRIO[/bold cyan]\n")

    while True:
        username = Prompt.ask(
            "Nome de usuário (mínimo 3 caracteres, apenas letras e números)"
        )

        if len(username) < 3:
            console.print("[red]❌ Nome muito curto. Mínimo 3 caracteres.[/red]")
            continue

        if not username.isalnum():
            console.print("[red]❌ Use apenas letras e números.[/red]")
            continue

        existing = firebase.get_user_by_username(username)
        if existing:
            console.print("[red]❌ Nome de usuário já existe. Escolha outro.[/red]")
            continue

        break

    while True:
        password = Prompt.ask("Senha (mínimo 6 caracteres)", password=True)

        if len(password) < 6:
            console.print("[red]❌ Senha muito curta. Mínimo 6 caracteres.[/red]")
            continue

        password_confirm = Prompt.ask("Confirme a senha", password=True)

        if password != password_confirm:
            console.print("[red]❌ Senhas não coincidem. Tente novamente.[/red]")
            continue

        break

    success, result = auth.register(username, password)

    if success:
        user_id = result
        console.print("\n[green]✅ Usuário criado com sucesso![/green]\n")

        level = run_initial_quiz()
        firebase.update_user_level(user_id, level)

        console.print(f"\n[green]✅ Nível definido: {level.upper()}[/green]")

        # Configura exercícios do nível escolhido
        console.print("\n[cyan]📁 Configurando exercícios do seu nível...[/cyan]")
        exercise_manager = ExerciseManager(Path(__file__).parent)
        if exercise_manager.setup_user_exercises(level):
            console.print("[green]✅ Exercícios configurados![/green]")
        else:
            console.print("[yellow]⚠️  Aviso: Erro ao configurar exercícios[/yellow]")

        console.print("\n[dim]Faça login para começar o workshop.[/dim]\n")

        return True
    else:
        console.print(f"\n[red]❌ Erro no registro: {result}[/red]\n")
        return False


def login_flow(auth: Authenticator) -> dict[str, Any] | None:
    console.print("\n[bold cyan]🔐 LOGIN[/bold cyan]\n")

    username = Prompt.ask("Nome de usuário")
    password = Prompt.ask("Senha", password=True)

    success, message, session = auth.login(username, password)

    if success:
        console.print(f"\n[green]✅ {message}[/green]\n")
        return session
    else:
        console.print(f"\n[red]❌ {message}[/red]\n")
        return None


def main():
    show_banner()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        try:
            firebase = FirebaseClient()
        except Exception as e:
            console.print(f"[red]❌ Erro ao conectar com Firebase: {e}[/red]")
            return 1
        else:
            console.print(f"[red]❌ Comando desconhecido: {command}[/red]")
            console.print("\nComandos disponíveis:")
            console.print("  --init-api-key      : Configura API key (instrutor)")
            return 1

    try:
        firebase = FirebaseClient()
    except Exception as e:
        console.print(f"[red]❌ Erro ao conectar com Firebase: {e}[/red]")
        console.print(
            "\nVerifique se o arquivo config/firebase_config.json existe e está correto."
        )
        return 1

    auth = Authenticator(firebase)

    existing_session = auth.get_current_session()

    if existing_session:
        console.print(
            f"\n[green]Bem-vindo de volta, {existing_session['username']}![/green]\n"
        )
        use_existing = Confirm.ask("Continuar com esta sessão?", default=True)

        if use_existing:
            console.print("\n[cyan]Iniciando workshop...[/cyan]\n")
            from watcher import WorkshopSession

            workshop = WorkshopSession(existing_session, firebase)
            workshop.start()
            return 0
        else:
            auth.logout()

    while True:
        console.print("\n[bold]O que você deseja fazer?[/bold]")
        console.print("  1 - Login")
        console.print("  2 - Registrar novo usuário")
        console.print("  3 - Sair")

        choice = Prompt.ask("Escolha", choices=["1", "2", "3"], default="1")

        if choice == "1":
            session = login_flow(auth)
            if session:
                console.print("\n[cyan]Iniciando workshop...[/cyan]\n")
                from watcher import WorkshopSession

                workshop = WorkshopSession(session, firebase)
                workshop.start()
                break

        elif choice == "2":
            success = register_flow(auth, firebase)
            if success:
                continue

        elif choice == "3":
            console.print("\n[cyan]👋 Até logo![/cyan]")
            break

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Interrompido pelo usuário[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ Erro fatal: {e}[/bold red]")
        import traceback

        traceback.print_exc()
        sys.exit(1)
