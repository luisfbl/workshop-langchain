"""
Exercício 2 - Adicionando Sua Primeira Tool (EASY)
===================================================

OBJETIVO: Adicionar UMA tool customizada ao agente.

TEMPO: 15 minutos

O QUE VOCÊ VAI APRENDER:
- Criar uma tool com @tool decorator
- Importância da docstring para o LLM
- Como o agente decide usar a tool
- Ver o "pensamento" do agente (ReAct pattern)

CONTEXTO:
Agora vamos dar uma HABILIDADE ao agente: listar arquivos Python.
O agente vai DECIDIR quando usar essa ferramenta.
"""

# I AM NOT DONE

from pathlib import Path
from langchain.agents import create_react_agent, AgentExecutor, tool
from langchain_openai import ChatOpenAI
from langchain import hub

# ============================================================================
# TODO 1: Criar a tool de listagem de arquivos
# ============================================================================

@tool
def list_python_files(directory: str) -> str:
    """Lista todos os arquivos Python (.py) em um diretório.

    Use esta ferramenta quando o usuário pedir para listar, encontrar,
    ou ver quais arquivos Python existem em um diretório.

    Args:
        directory: Caminho do diretório para buscar arquivos

    Returns:
        String formatada com lista de arquivos .py encontrados
    """
    # TODO: Implemente a lógica
    # DICA: Use Path(directory).glob("*.py")
    # DICA: Retorne string formatada: "Encontrei X arquivos:\n- file1.py\n- file2.py"

    path = Path(directory)
    python_files = list(path.glob("*.py"))

    # TODO: Formate e retorne o resultado
    # Se não encontrar arquivos, retorne mensagem apropriada

    pass


# ============================================================================
# TODO 2: Criar agente COM a tool
# ============================================================================

def create_agent_with_tool():
    """Cria agente com a tool list_python_files."""

    # TODO 2.1: Criar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # TODO 2.2: Buscar prompt
    prompt = None  # TODO: hub.pull("hwchase17/react")

    # TODO 2.3: Criar lista de tools COM list_python_files
    # IMPORTANTE: Agora a lista NÃO está vazia!
    tools = []  # TODO: [list_python_files]

    # TODO 2.4: Criar agente
    agent = None  # TODO: create_react_agent(...)

    # TODO 2.5: Criar executor
    agent_executor = None  # TODO: AgentExecutor(..., verbose=True)

    return agent_executor


# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_agent():
    """Testa o agente com tool."""
    print("🤖 Testando agente com tool de listagem...\n")

    try:
        agent = create_agent_with_tool()

        print("=" * 60)
        print("TESTE 1: Pedir para listar arquivos (deve usar a tool)")
        print("=" * 60)
        response = agent.invoke({
            "input": "Liste todos os arquivos Python no diretório ./sample_project"
        })
        print(f"\nResposta: {response['output']}\n")

        print("=" * 60)
        print("TESTE 2: Pergunta geral (NÃO deve usar a tool)")
        print("=" * 60)
        response = agent.invoke({
            "input": "O que é Python?"
        })
        print(f"\nResposta: {response['output']}\n")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
