"""
Exercicio 4 - State Management (EASY)
=====================================

OBJETIVO: Entender a diferenca entre Memory e State, e como usar State
         para gerenciar dados estruturados durante um workflow.

TEMPO: 15 minutos

O QUE VOCE VAI APRENDER:
- Diferenca entre Memory (conversacao) e State (workflow/dados)
- Criar state com TypedDict
- Funções que recebem e retornam state
- Manter dados estruturados durante processamento

CONTEXTO:
No exercício anterior vimos Memory para conversação. Agora vamos aprender
State, que e diferente:

MEMORY: Guarda historico de CONVERSAS (perguntas e respostas)
STATE: Guarda DADOS ESTRUTURADOS que mudam durante um workflow

Exemplo: Sistema que processa multiplos arquivos:
- Memory: Lembra que o usuario perguntou sobre calculator.py
- State: Trackeia quais arquivos foram processados, quantas funcoes encontradas, etc.
"""

# I AM NOT DONE

from typing import TypedDict, List
from pathlib import Path
import ast

# Importar tools dos exercicios anteriores
from .ex02_first_tool import list_python_files

# ============================================================================
# TODO 1: Definir o State com TypedDict
# ============================================================================

class AnalysisState(TypedDict):
    """State para trackear analise de multiplos arquivos.

    TypedDict garante type safety e autocomplete.

    TODO 1.1: Complete a definição do TypedDict abaixo com os campos necessários.
    Já fornecemos files_to_process como exemplo.
    """
    files_to_process: list[str]  # Arquivos que ainda precisam ser analisados
    # TODO: Adicione os outros campos:
    # files_processed: list[str]  # Arquivos ja processados
    # current_file: str  # Arquivo sendo processado agora
    # total_functions: int  # Total de funcoes encontradas
    # total_lines: int  # Total de linhas de codigo
    # errors: list[str]  # Lista de erros encontrados


# ============================================================================
# TODO 2: Criar funcoes que trabalham com State
# ============================================================================

def initialize_state(directory: str) -> AnalysisState:
    """Inicializa o state com lista de arquivos Python de um diretorio.

    Args:
        directory: Diretorio para buscar arquivos .py

    Returns:
        State inicial com files_to_process populado
    """
    # TODO 2.1: Buscar arquivos Python e criar state inicial
    # DICA: Use Path(directory).glob("*.py") para buscar arquivos
    # DICA: Converta para lista de strings: [str(f) for f in path.glob("*.py")]
    path = Path(directory)
    python_files = None  # TODO: Substitua por lista de arquivos .py como strings

    # TODO 2.2: Preencha o state com os valores iniciais
    # DICA: Listas vazias [], strings vazias "", números = 0
    state: AnalysisState = {
        "files_to_process": python_files,
        # TODO: Adicione os outros campos aqui com valores iniciais
        # "files_processed": [],
        # "current_file": "",
        # "total_functions": 0,
        # "total_lines": 0,
        # "errors": []
    }

    return state


def process_next_file(state: AnalysisState) -> AnalysisState:
    """Processa o proximo arquivo da fila e atualiza o state.

    Esta e a funcao CORE do workflow. Ela:
    1. Pega o proximo arquivo de files_to_process
    2. Analisa o arquivo (conta funcoes e linhas)
    3. Atualiza os contadores no state
    4. Move o arquivo para files_processed

    Args:
        state: State atual

    Returns:
        State atualizado
    """
    # TODO 2.3: Verificar se ha arquivos para processar
    # Se lista vazia, retorne state sem modificar
    if not state["files_to_process"]:
        return state

    # TODO 2.4: Pegar primeiro arquivo e atualizar current_file
    current = None  # TODO: state["files_to_process"][0]
    # TODO: state["current_file"] = current

    print(f"\nProcessando: {current}")

    try:
        # TODO 2.5: Ler arquivo e parsear com AST
        # TODO: Abra o arquivo, leia content e faça ast.parse(content)
        content = None  # TODO: Implementar leitura
        tree = None  # TODO: ast.parse(content)

        # TODO 2.6: Contar funcoes e linhas
        # DICA 1: Para funcoes, use ast.walk(tree) e conte isinstance(node, ast.FunctionDef)
        # DICA 2: Para linhas, use len(content.split('\n'))
        num_functions = 0  # TODO: Implemente contagem de funcoes
        num_lines = 0  # TODO: Implemente contagem de linhas

        print(f"  Funcoes: {num_functions}")
        print(f"  Linhas: {num_lines}")

        # TODO 2.7: Atualizar state com resultados
        # Incremente os contadores e mova o arquivo de to_process para processed
        # state["total_functions"] += num_functions
        # state["total_lines"] += num_lines
        # state["files_processed"].append(current)
        # state["files_to_process"].pop(0)

    except Exception as e:
        print(f"  Erro: {e}")
        # TODO 2.8: Tratar erro - adicione ao state["errors"] e remova da fila
        # state["errors"].append(f"{current}: {str(e)}")
        # state["files_to_process"].pop(0)

    return state


def get_state_summary(state: AnalysisState) -> str:
    """Gera resumo legivel do state atual.

    Args:
        state: State a ser resumido

    Returns:
        String formatada com resumo
    """
    # Ja implementado - apenas retorna resumo formatado
    summary = f"""
RESUMO DO STATE:
==================
Arquivos processados: {len(state['files_processed'])}
Arquivos pendentes: {len(state['files_to_process'])}
Total de funcoes: {state['total_functions']}
Total de linhas: {state['total_lines']}
Erros: {len(state['errors'])}
"""

    if state['current_file']:
        summary += f"\nProcessando: {state['current_file']}"

    if state['errors']:
        summary += "\n\nErros encontrados:"
        for error in state['errors']:
            summary += f"\n  - {error}"

    return summary


# ============================================================================
# TODO 3: Executar workflow usando State
# ============================================================================

def run_analysis_workflow(directory: str) -> AnalysisState:
    """Executa workflow completo de analise usando state.

    Args:
        directory: Diretorio com arquivos Python

    Returns:
        State final apos processar todos os arquivos
    """
    print(f"Analisando: {directory}")

    # TODO 3.1: Inicializar state chamando initialize_state()
    state = None  # TODO: initialize_state(directory)

    print(f"Encontrados {len(state['files_to_process'])} arquivos\n")

    # TODO 3.2: Processar todos os arquivos usando loop while
    # DICA: while state["files_to_process"]:
    #           state = process_next_file(state)

    # TODO: Implementar loop aqui

    # Mostrar resumo final
    print(get_state_summary(state))

    return state


# ============================================================================
# Testes (NAO MODIFIQUE)
# ============================================================================

def test_workflow():
    """Testa workflow com state."""
    try:
        return run_analysis_workflow("./sample_project")
    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_workflow()
