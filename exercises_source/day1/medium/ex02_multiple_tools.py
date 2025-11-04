"""
Exercício 3 - Múltiplas Tools e Tool Selection (MEDIUM)
========================================================

OBJETIVO: Criar múltiplas tools e entender como o agente decide entre elas.

TEMPO: 25 minutos

O QUE VOCÊ VAI APRENDER:
- Design de tools com responsabilidades únicas
- Como docstrings influenciam tool selection
- Tratamento de erros robusto
- Observar o padrão ReAct com múltiplas opções

CONTEXTO:
Vamos expandir as capacidades do agente com mais ferramentas.
O desafio é fazer cada tool ter uma descrição ÚNICA e CLARA para que
o agente saiba exatamente quando usar cada uma.
"""

# I AM NOT DONE

from pathlib import Path
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Importar tool do exercício anterior
from .ex02_first_tool import list_python_files

# ============================================================================
# TODO 1: Criar tool read_file
# ============================================================================

@tool
def read_file(file_path: str) -> str:
    """
    TODO: Escreva uma docstring que deixe CLARO:
    - Quando usar esta tool vs outras
    - Que esta tool retorna CONTEÚDO completo
    - Diferença entre esta e count_lines

    Pense: Como o agente vai diferenciar "ler arquivo" de "contar linhas"?
    """
    # TODO: Implemente com tratamento de erros robusto
    # Considere:
    # - Arquivo não existe
    # - Arquivo muito grande (truncar?)
    # - Encoding diferente de utf-8
    # - Permissões de leitura

    pass


# ============================================================================
# TODO 2: Criar tool count_lines com métricas extras
# ============================================================================

@tool
def count_lines(file_path: str) -> str:
    """
    TODO: Docstring clara que diferencia esta tool.

    Esta tool deve ser escolhida quando o usuário pergunta sobre:
    - Quantidade, tamanho, número de linhas
    - Estatísticas do arquivo

    NÃO deve ser escolhida quando o usuário quer VER o conteúdo.
    """
    # TODO: Implemente contagem com estatísticas extras
    # Retorne:
    # - Total de linhas
    # - Linhas de código (sem vazias/comentários)
    # - Linhas de comentário
    # - Linhas vazias
    # - Percentual de cada tipo

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total_lines = len(lines)
        code_lines = 0
        comment_lines = 0
        blank_lines = 0

        # TODO: Conte cada tipo de linha
        for line in lines:
            stripped = line.strip()
            # TODO: Classifique a linha
            pass

        # TODO: Calcule percentuais e retorne formatado
        result = f"""Estatísticas de '{file_path}':
- Total: {total_lines} linhas
- Código: {code_lines} linhas
- Comentários: {comment_lines} linhas
- Vazias: {blank_lines} linhas"""

        return result

    except Exception as e:
        return f"Erro: {str(e)}"


# ============================================================================
# TODO 3: DESAFIO - Adicione uma 4ª tool (OPCIONAL)
# ============================================================================

@tool
def extract_functions(file_path: str) -> str:
    """
    DESAFIO EXTRA: Crie uma tool que lista todas as funções de um arquivo.

    TODO: Docstring explicando quando usar

    DICA: Procure por linhas que começam com "def "
    """
    # TODO: Implemente se quiser o desafio extra
    pass


# ============================================================================
# TODO 4: Criar o agente com todas as tools
# ============================================================================

def create_multi_tool_agent():
    """
    TODO: Implemente o agente completo.

    Tools disponíveis:
    - list_python_files (do ex02)
    - read_file
    - count_lines
    - extract_functions (se implementou)

    Configure com verbose=True para ver as decisões do agente.
    """
    pass


# ============================================================================
# TODO 5: Experimento com docstrings (OPCIONAL)
# ============================================================================

def experiment_tool_selection():
    """
    OPCIONAL: Experimente criar tools com docstrings ambíguas
    e veja o agente ficando confuso sobre qual usar.

    Depois melhore as docstrings e observe a diferença.
    """
    pass


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_agent():
    try:
        agent = create_multi_tool_agent()

        test_cases = [
            ("Liste arquivos Python em ./sample_project", "list_python_files"),
            ("Qual o tamanho do calculator.py?", "count_lines"),
            ("Me mostre o código do calculator.py", "read_file"),
            ("Quantos arquivos tem e quantas linhas tem o maior?", "múltiplas tools"),
        ]

        for i, (query, expected) in enumerate(test_cases, 1):
            print("=" * 70)
            print(f"TESTE {i}: {query}")
            print(f"Tool esperada: {expected}")
            print("=" * 70)

            response = agent.invoke({"input": query})
            print(f"\nResposta: {response['output']}\n")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
