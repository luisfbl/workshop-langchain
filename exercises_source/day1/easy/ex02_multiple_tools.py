"""
Exercício 3 - Agente com Múltiplas Tools (EASY)
================================================

OBJETIVO: Adicionar mais tools e ver o agente escolher qual usar.

TEMPO: 20 minutos

O QUE VOCÊ VAI APRENDER:
- Como o agente escolhe entre múltiplas tools
- Importância de descrições únicas e claras
- Como tools trabalham juntas
- Diferença entre tools específicas vs genéricas

CONTEXTO:
Você já tem uma tool que lista arquivos. Agora vamos adicionar mais 2:
- read_file: lê o conteúdo de um arquivo
- count_lines: conta linhas de código

O agente vai DECIDIR qual tool usar baseado na pergunta do usuário.
"""

# I AM NOT DONE

from pathlib import Path
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Importar a tool do exercício anterior
from .ex02_first_tool import list_python_files

# ============================================================================
# TODO 1: Criar tool para ler arquivo
# ============================================================================

@tool
def read_file(file_path: str) -> str:
    """Lê e retorna o conteúdo completo de um arquivo.

    Use esta ferramenta quando o usuário quiser VER ou LER o conteúdo
    de um arquivo específico.

    Args:
        file_path: Caminho completo do arquivo a ser lido

    Returns:
        Conteúdo do arquivo como string
    """
    # TODO: Implemente a leitura do arquivo
    # DICA: Use open(file_path, 'r', encoding='utf-8')
    # DICA: Não esqueça de tratar erros (arquivo não existe, etc)

    try:
        # TODO: Abra e leia o arquivo
        pass
    except FileNotFoundError:
        return f"Erro: Arquivo '{file_path}' não encontrado."
    except Exception as e:
        return f"Erro ao ler arquivo: {str(e)}"


# ============================================================================
# TODO 2: Criar tool para contar linhas
# ============================================================================

@tool
def count_lines(file_path: str) -> str:
    """Conta quantas linhas de código tem em um arquivo Python.

    Use esta ferramenta quando o usuário perguntar sobre QUANTIDADE,
    TAMANHO ou NÚMERO DE LINHAS de um arquivo.

    Ignora linhas em branco e comentários, conta apenas código.

    Args:
        file_path: Caminho do arquivo

    Returns:
        Número de linhas de código
    """
    # TODO: Implemente a contagem
    # DICA: Leia linha por linha
    # DICA: Use strip() para remover espaços
    # DICA: Ignore linhas vazias (line.strip() == "")
    # DICA: Ignore comentários (line.strip().startswith("#"))

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # TODO: Conte apenas linhas de código
        code_lines = 0

        for line in lines:
            stripped = line.strip()
            # TODO: Verifique se não é vazia e não é comentário
            # Se passar, incremente code_lines
            pass

        return f"O arquivo '{file_path}' tem {code_lines} linhas de código."

    except FileNotFoundError:
        return f"Erro: Arquivo '{file_path}' não encontrado."
    except Exception as e:
        return f"Erro: {str(e)}"


# ============================================================================
# TODO 3: Criar agente com as 3 tools
# ============================================================================

def create_multi_tool_agent():
    """Cria agente com 3 tools: list_python_files, read_file, count_lines."""

    # TODO 3.1: Criar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-5-nano", temperature=0)

    # TODO 3.2: Criar lista de tools com as 3 ferramentas
    # IMPORTANTE: Agora temos 3 tools!
    tools = []  # TODO: [list_python_files, read_file, count_lines]

    # TODO 3.3: Criar agente usando create_agent
    agent = None  # TODO: create_agent(llm, tools)

    return agent


# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_agent():
    """Testa o agente com múltiplas tools."""
    print("🤖 Testando agente com 3 tools...\n")

    try:
        agent = create_multi_tool_agent()

        test_cases = [
            {
                "query": "Liste todos os arquivos Python em ./sample_project",
                "expected_tool": "list_python_files",
                "description": "Deve usar list_python_files"
            },
            {
                "query": "Quantas linhas de código tem o arquivo ./sample_project/calculator.py?",
                "expected_tool": "count_lines",
                "description": "Deve usar count_lines"
            },
            {
                "query": "Mostre o conteúdo do arquivo ./sample_project/calculator.py",
                "expected_tool": "read_file",
                "description": "Deve usar read_file"
            },
            {
                "query": "Quantos arquivos Python existem em ./sample_project e quantas linhas tem o calculator.py?",
                "expected_tool": "list_python_files + count_lines",
                "description": "Deve usar DUAS tools!"
            }
        ]

        for i, test in enumerate(test_cases, 1):
            print("=" * 70)
            print(f"TESTE {i}: {test['query']}")
            print(f"Expectativa: {test['description']}")
            print("=" * 70)

            # API 1.0+ usa messages
            response = agent.invoke({
                "messages": [{"role": "user", "content": test['query']}]
            })

            last_message = response['messages'][-1]
            print(f"\nResposta: {last_message.content}\n")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
