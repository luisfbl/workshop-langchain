"""
Exercício 2 - Adicionando Sua Primeira Tool (EASY)
===================================================

OBJETIVO: Adicionar UMA tool customizada ao agente.

TEMPO: 10 minutos

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
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

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
    """Cria agente com a tool list_python_files usando LangChain 1.0+ API."""

    # TODO 2.1: Criar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-5-nano", temperature=0)

    # TODO 2.2: Criar lista de tools COM list_python_files
    tools = []

    # TODO 2.3: Criar agente usando create_agent
    agent = None  # TODO: create_agent(llm, tools)

    return agent


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_agent():
    """Testa o agente com tool."""
    print(" Testando agente com tool de listagem...\n")

    try:
        agent = create_agent_with_tool()

        print("=" * 60)
        print("TESTE 1: Pedir para listar arquivos (deve usar a tool)")
        print("=" * 60)

        response = agent.invoke({
            "messages": [{"role": "user", "content": "Liste todos os arquivos Python no diretório ./sample_project"}]
        })

        last_message = response['messages'][-1]
        print(f"\nResposta: {last_message.content}\n")

        print("=" * 60)
        print("TESTE 2: Pergunta geral (NÃO deve usar a tool)")
        print("=" * 60)
        response = agent.invoke({
            "messages": [{"role": "user", "content": "O que é Python?"}]
        })

        last_message = response['messages'][-1]
        print(f"\nResposta: {last_message.content}\n")

    except Exception as e:
        print(f" Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
