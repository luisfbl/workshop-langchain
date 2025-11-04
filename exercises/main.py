#!/usr/bin/env python3
"""
Projeto Final - Gerador Automático de Documentação
==================================================

Este é o projeto final do workshop de Agentes de IA com LangChain!

Ele integra TUDO que você aprendeu:
- DIA 1: Agentes, Tools, Memory, State, Structured Output
- DIA 2: LangGraph, StateGraph, Conditional Routing, Orchestrator

FUNCIONALIDADE:
  CLI que recebe um diretório com código Python e gera README.md
  automaticamente com documentação de todos os arquivos.

USO:
  python main.py --path ./meu_projeto
  python main.py --path ./sample_project --output DOCS.md
  python main.py --help
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Importar o orchestrator do ex07
# (Em um projeto real, você refatoraria isso em módulos)
# Nota: Os exercícios são copiados dinamicamente baseado no nível do usuário
try:
    from day2.ex07_orchestrator import (
        create_orchestrator_graph,
        OrchestratorState
    )
except ImportError:
    # Fallback para quando exercícios não estão configurados
    print("  Exercícios ainda não configurados. Execute 'python main.py' primeiro.")
    create_orchestrator_graph = None
    OrchestratorState = None


# ============================================================================
# CLI e Interface Principal
# ============================================================================

def validate_directory(path: str) -> Path:
    """Valida se o diretório existe e tem arquivos Python.

    Args:
        path: Caminho do diretório

    Returns:
        Path object validado

    Raises:
        ValueError: Se diretório inválido
    """
    dir_path = Path(path)

    if not dir_path.exists():
        raise ValueError(f"Diretório não encontrado: {path}")

    if not dir_path.is_dir():
        raise ValueError(f"Caminho não é um diretório: {path}")

    # Verificar se tem arquivos .py
    py_files = list(dir_path.glob("*.py"))
    if not py_files:
        raise ValueError(f"Nenhum arquivo Python (.py) encontrado em: {path}")

    return dir_path


def generate_documentation(
    directory: str,
    output_file: str = "README.md",
    verbose: bool = False
) -> None:
    """Gera documentação para um projeto Python.

    Args:
        directory: Diretório com código Python
        output_file: Nome do arquivo de saída
        verbose: Se deve mostrar logs detalhados
    """
    print(f"\n=== GERADOR DE DOCUMENTAÇÃO ===")
    print(f"Diretório: {directory} | Output: {output_file}\n")

    try:
        # Validar diretório
        dir_path = validate_directory(directory)
        py_files = list(dir_path.glob("*.py"))
        print(f"Encontrados {len(py_files)} arquivos Python\n")

        # Criar graph do orchestrator
        graph = create_orchestrator_graph()

        # State inicial
        initial_state: OrchestratorState = {
            "directory": directory,
            "files_to_process": [],
            "files_processed": [],
            "current_file": "",
            "current_code": "",
            "current_analysis": {},
            "all_docs": [],
            "current_step": "start",
            "error": "",
            "retry_count": 0,
            "final_documentation": ""
        }

        # Executar workflow
        final_state = graph.invoke(initial_state)

        # Salvar resultado
        output_path = Path(directory) / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_state["final_documentation"])

        # Resumo
        print(f"\n Documentação gerada!")
        print(f"  Arquivos: {len(final_state['files_processed'])} | Docs: {len(final_state['all_docs'])}")
        print(f"  Salvo em: {output_path}")

        # Preview
        print(f"\n--- Preview (20 linhas) ---")
        lines = final_state["final_documentation"].split('\n')[:20]
        print('\n'.join(lines))
        if len(final_state["final_documentation"].split('\n')) > 20:
            print("...")

    except ValueError as e:
        print(f"\nErro: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Função principal do CLI."""
    parser = argparse.ArgumentParser(
        description="Gera documentação automática para projetos Python usando IA",
        epilog="""
Exemplos:
  %(prog)s --path ./meu_projeto
  %(prog)s --path ./sample_project --output DOCS.md
  %(prog)s --path ~/projetos/api --verbose

Este projeto usa:
  - LangChain para agentes e tools
  - LangGraph para workflow orchestration
  - OpenAI gpt-5-nano para geração de docs
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Caminho do diretório com código Python"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="README.md",
        help="Nome do arquivo de saída (padrão: README.md)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostra logs detalhados do processamento"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0 - Workshop Agentes IA"
    )

    args = parser.parse_args()

    # Executar geração
    generate_documentation(
        directory=args.path,
        output_file=args.output,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
