"""
Exercício 1 - Seu Primeiro Agente LangChain (MEDIUM)
=====================================================

OBJETIVO: Criar um agente conversacional básico e entender o padrão ReAct.

TEMPO: 5 minutos

O QUE VOCÊ VAI APRENDER:
- Inicializar e configurar um LLM
- Entender o prompt ReAct
- Criar agente e executor do zero
- Diferença entre agent e agent_executor

CONTEXTO:
Vamos criar um agente básico sem tools. O foco é entender a estrutura
e o fluxo: LLM → Prompt → Agent → Executor
"""

# I AM NOT DONE

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# ============================================================================
# TODO 1: Crie função que retorna LLM configurado
# ============================================================================

def create_llm():
    """
    TODO: Crie e retorne um ChatOpenAI com:
    - model: gpt-5-nano
    - temperature: 0
    - Considere adicionar outras configurações se quiser experimentar
    """
    pass


# ============================================================================
# TODO 2: Crie função que retorna o agente completo
# ============================================================================

def create_basic_agent():
    """
    TODO: Implemente a criação completa do agente:

    1. Criar LLM usando a função create_llm()
    2. Criar agente com create_agent()

    Retorne: Agente compilado (CompiledStateGraph)
    """
    pass

# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_agent():
    """Testa o agente básico."""
    try:
        agent = create_basic_agent()

        print("=" * 60)
        print("TESTE: Pergunta que NÃO precisa de tools")
        print("=" * 60)
        response = agent.invoke({
            "messages": [{"role": "user", "content": "Explique em uma frase o que é um agente de IA"}]
        })
        print(f"Resposta: {response['messages'][-1].content}\n")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
