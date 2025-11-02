"""
Exercício 1 - Seu Primeiro Agente LangChain (EASY)
===================================================

OBJETIVO: Criar um agente conversacional básico SEM ferramentas.

TEMPO: 10 minutos

O QUE VOCÊ VAI APRENDER:
- Inicializar um LLM (ChatOpenAI)
- Criar um agente simples
- Entender a diferença entre LLM direto vs Agente

CONTEXTO:
Antes de adicionar tools, vamos entender o básico: como criar um agente
que pode conversar. No próximo exercício adicionaremos ferramentas.

IMPORTANTE: Este agente ainda NÃO tem tools! É só conversação.
"""

# I AM NOT DONE

from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub

# ============================================================================
# TODO 1: Inicializar o modelo LLM
# ============================================================================

def create_llm():
    """
    Cria e retorna um modelo de linguagem ChatOpenAI.

    TODO: Inicialize ChatOpenAI com:
    - model="gpt-4o-mini"
    - temperature=0 (para respostas determinísticas)
    """
    # DICA: llm = ChatOpenAI(model="...", temperature=...)
    llm = None  # TODO: Substitua por ChatOpenAI(...)

    return llm


# ============================================================================
# TODO 2: Criar agente básico
# ============================================================================

def create_basic_agent():
    """
    Cria um agente ReAct básico sem nenhuma tool.

    TODO: Complete os passos abaixo.
    """
    # TODO 2.1: Criar o LLM usando a função acima
    llm = None  # TODO: Chamar create_llm()

    # TODO 2.2: Buscar o prompt ReAct do hub
    # DICA: O prompt padrão está em "hwchase17/react"
    prompt = None  # TODO: hub.pull("hwchase17/react")

    # TODO 2.3: Criar lista de tools (vazia por enquanto!)
    # IMPORTANTE: Mesmo sem tools, precisamos passar uma lista vazia
    tools = []  # Deixe vazio - sem tools neste exercício!

    # TODO 2.4: Criar o agente ReAct
    # DICA: create_react_agent precisa de (llm, tools, prompt)
    agent = None  # TODO: create_react_agent(llm, tools, prompt)

    # TODO 2.5: Criar o executor do agente
    # DICA: AgentExecutor(agent=..., tools=..., verbose=True)
    # verbose=True mostra o "pensamento" do agente
    agent_executor = None  # TODO: AgentExecutor(...)

    return agent_executor


# ============================================================================
# Teste local (NÃO MODIFIQUE - use para testar seu código)
# ============================================================================

def test_agent():
    """Testa o agente localmente."""
    print("🤖 Testando agente básico...\n")

    try:
        agent = create_basic_agent()

        # Teste 1: Pergunta simples
        print("=" * 60)
        print("TESTE 1: Pergunta simples")
        print("=" * 60)
        response = agent.invoke({
            "input": "Olá! Qual é a capital do Brasil?"
        })
        print(f"Resposta: {response['output']}\n")

        # Teste 2: Pergunta que precisaria de ferramenta (mas não temos ainda)
        print("=" * 60)
        print("TESTE 2: Pergunta sobre arquivos (sem tool, vai falhar graciosamente)")
        print("=" * 60)
        response = agent.invoke({
            "input": "Liste arquivos Python no diretório atual"
        })
        print(f"Resposta: {response['output']}\n")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
