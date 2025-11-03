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
"""

# I AM NOT DONE

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# ============================================================================
# TODO 1: Inicializar o modelo LLM
# ============================================================================

def create_llm():
    """
    Cria e retorna um modelo de linguagem ChatOpenAI.

    TODO: Inicialize ChatOpenAI com:
    - model="gpt-5-nano"
    - temperature=0 (para respostas determinísticas)
    """
    llm = None  # TODO: Substitua por ChatOpenAI(...)

    return llm


# ============================================================================
# TODO 2: Criar agente básico
# ============================================================================

def create_basic_agent():
    # TODO 2.1: Criar o LLM usando a função create_llm
    llm = None

    # TODO 2.3: Criar o agente usando create_agent
    agent = None

    return agent


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_agent():
    print("🤖 Testando agente básico...\n")

    try:
        agent = create_basic_agent()

        # Teste 1: Pergunta simples
        print("=" * 60)
        print("TESTE 1: Pergunta simples")
        print("=" * 60)

        response = agent.invoke({
            "messages": [{"role": "user", "content": "Olá! Qual é a capital do Brasil?"}]
        })

        # A resposta está em messages[-1]
        last_message = response['messages'][-1]
        print(f"Resposta: {last_message.content}\n")

        # Teste 2: Pergunta que precisaria de ferramenta (mas não temos ainda)
        print("=" * 60)
        print("TESTE 2: Pergunta sobre arquivos (sem tool, vai falhar graciosamente)")
        print("=" * 60)
        response = agent.invoke({
            "messages": [{"role": "user", "content": "Liste arquivos Python no diretório atual"}]
        })
        last_message = response['messages'][-1]
        print(f"Resposta: {last_message.content}\n")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
