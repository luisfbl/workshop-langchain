"""
Exercício 4 - Memory e Gestão de Contexto (MEDIUM)
===================================================

OBJETIVO: Implementar e entender diferentes estratégias de memory.

TEMPO: 15 minutos

O QUE VOCÊ VAI APRENDER:
- ConversationBufferMemory
- Como memory afeta o contexto do LLM
- Trade-offs de diferentes tipos de memory
- State management em agentes

CONTEXTO:
Memory é essencial para conversas naturais, mas tem limitações.
Vamos explorar como funciona e quando usar.
"""

# I AM NOT DONE

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Importar tools
from .ex02_first_tool import list_python_files
from .ex02_multiple_tools import read_file, count_lines

# ============================================================================
# Tool para demonstração (já implementada)
# ============================================================================

@tool
def get_file_info(file_path: str) -> str:
    """Retorna resumo de um arquivo Python."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total = len(lines)
        functions = sum(1 for line in lines if line.strip().startswith('def '))
        classes = sum(1 for line in lines if line.strip().startswith('class '))

        return f"Arquivo '{file_path}': {total} linhas, {functions} funções, {classes} classes"
    except Exception as e:
        return f"Erro: {str(e)}"


# ============================================================================
# TODO 1: Criar agente SEM memory
# ============================================================================

def create_agent_without_memory():
    """
    TODO: Implemente um agente SEM memory.

    Use todas as 4 tools e verbose=True.
    """
    pass


# ============================================================================
# TODO 2: Criar agente COM ConversationBufferMemory
# ============================================================================

def create_agent_with_memory():
    """
    TODO: Implemente um agente COM ConversationBufferMemory.

    Configure:
    - memory_key="chat_history"
    - return_messages=True

    Adicione ao AgentExecutor.
    """
    pass


# ============================================================================
# TODO 3: DESAFIO - Implementar tracking customizado
# ============================================================================

# Estado para tracking (simplificado)
analyzed_files = []

@tool
def track_analyzed_file(file_path: str) -> str:
    """
    DESAFIO OPCIONAL: Rastreia arquivos já analisados.

    TODO: Implemente lógica que:
    - Adiciona arquivo à lista analyzed_files
    - Retorna se arquivo já foi analisado antes
    - Evita análises duplicadas
    """
    # TODO: Implemente
    pass


@tool
def list_analyzed_files() -> str:
    """
    DESAFIO OPCIONAL: Lista arquivos já analisados nesta sessão.

    TODO: Retorne a lista de analyzed_files formatada.
    """
    # TODO: Implemente
    pass


# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_memory():
    try:
        conversation = [
            "Analise o arquivo ./sample_project/calculator.py",
            "Quantas funções ele tem?",
            "Tem classes também?",
            "Agora analise o utils.py",
            "Qual dos dois arquivos tem mais funções?"
        ]

        print("=" * 70)
        print("TESTE 1: SEM MEMORY")
        print("=" * 70)
        agent_no_mem = create_agent_without_memory()

        for i, query in enumerate(conversation, 1):
            print(f"\nPergunta {i}: {query}")
            response = agent_no_mem.invoke({"input": query})
            print(f"Resposta: {response['output'][:100]}...")

        print("\n\n" + "=" * 70)
        print("TESTE 2: COM MEMORY")
        print("=" * 70)
        agent_with_mem = create_agent_with_memory()

        for i, query in enumerate(conversation, 1):
            print(f"\nPergunta {i}: {query}")
            response = agent_with_mem.invoke({"input": query})
            print(f"Resposta: {response['output'][:100]}...")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_memory()
