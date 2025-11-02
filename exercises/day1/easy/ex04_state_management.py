"""
Exercicio 4 - State Management (EASY)
=====================================

OBJETIVO: Entender a diferenca entre Memory e State, e como usar State
         para gerenciar dados estruturados durante um workflow.

TEMPO: 15 minutos

O QUE VOCE VAI APRENDER:
- Diferenca entre Memory (conversacao) e State (workflow/dados)
- Criar state com TypedDict
- Funcoes que recebem e retornam state
- Manter dados estruturados durante processamento

CONTEXTO:
No exercicio anterior vimos Memory para conversacao. Agora vamos aprender
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
from ex02_first_tool import list_python_files

# ============================================================================
# TODO 1: Definir o State com TypedDict
# ============================================================================

class AnalysisState(TypedDict):
    """State para trackear analise de multiplos arquivos.

    TypedDict garante type safety e autocomplete.
    """
    # TODO 1.1: Adicione os campos do state:

    # files_to_process: Lista de arquivos que ainda precisam ser analisados
    files_to_process: List[str]  # Ja feito como exemplo

    # TODO: Adicione os outros campos:
    # files_processed: List[str]  # Arquivos ja processados
    # current_file: str  # Arquivo sendo processado agora
    # total_functions: int  # Total de funcoes encontradas ate agora
    # total_lines: int  # Total de linhas de codigo
    # errors: List[str]  # Lista de erros encontrados


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
    # TODO 2.1: Usar list_python_files ou buscar arquivos diretamente
    path = Path(directory)
    python_files = [str(f) for f in path.glob("*.py")]

    # TODO 2.2: Criar e retornar state inicial
    # DICA: Todos os contadores comecam em 0, listas vazias
    state: AnalysisState = {
        "files_to_process": python_files,
        # TODO: Preencha os outros campos
        # "files_processed": [],
        # "current_file": "",
        # "total_functions": 0,
        # "total_lines": 0,
        # "errors": []
    }

    return None  # TODO: Retornar state


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
    if not state["files_to_process"]:
        print("Aviso: Nenhum arquivo para processar!")
        return state

    # TODO 2.4: Pegar primeiro arquivo da fila
    current = None  # TODO: state["files_to_process"][0]

    # TODO 2.5: Atualizar current_file no state
    # state["current_file"] = current

    print(f"\nProcessando: {current}")

    try:
        # TODO 2.6: Ler e analisar arquivo
        with open(current, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)

        # TODO 2.7: Contar funcoes e linhas
        num_functions = 0  # TODO: Conte funcoes com ast.walk
        num_lines = 0  # TODO: len(content.split('\n'))

        # TODO: Implementar contagem
        # DICA: for node in ast.walk(tree):
        #           if isinstance(node, ast.FunctionDef):
        #               num_functions += 1

        print(f"  Funcoes: {num_functions}")
        print(f"  Linhas: {num_lines}")

        # TODO 2.8: Atualizar contadores no state
        # state["total_functions"] += num_functions
        # state["total_lines"] += num_lines

        # TODO 2.9: Mover arquivo de to_process para processed
        # state["files_processed"].append(current)
        # state["files_to_process"].pop(0)

    except Exception as e:
        print(f"  Erro: {e}")
        # TODO 2.10: Adicionar erro ao state
        # state["errors"].append(f"{current}: {str(e)}")
        # state["files_to_process"].pop(0)  # Remove mesmo com erro

    return state


def get_state_summary(state: AnalysisState) -> str:
    """Gera resumo legivel do state atual.

    Args:
        state: State a ser resumido

    Returns:
        String formatada com resumo
    """
    # TODO 2.11: Criar resumo formatado
    summary = f"""
RESUMO DO STATE:
==================
Arquivos processados: {len(state.get('files_processed', []))}
Arquivos pendentes: {len(state.get('files_to_process', []))}
Total de funcoes: {state.get('total_functions', 0)}
Total de linhas: {state.get('total_lines', 0)}
Erros: {len(state.get('errors', []))}
"""

    if state.get('current_file'):
        summary += f"\nProcessando: {state['current_file']}"

    if state.get('errors'):
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

    # TODO 3.1: Inicializar state
    state = None  # TODO: initialize_state(directory)

    print(f"Encontrados {len(state['files_to_process'])} arquivos\n")

    # TODO 3.2: Processar todos os arquivos
    # DICA: Use while state["files_to_process"]:
    #           state = process_next_file(state)

    # TODO: Implementar loop

    # TODO 3.3: Mostrar resumo final
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
