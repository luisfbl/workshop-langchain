"""
Testes para Exercício 1: Primeiro Agente
"""

import os
import sys
from pathlib import Path

import pytest

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importa usando helper que detecta nível do usuário
from exercises.tests.test_helper import import_exercise

# Importa o exercício do nível correto
ex01 = import_exercise(1, 'ex01_first_agent')
create_llm = ex01.create_llm
create_basic_agent = ex01.create_basic_agent


class TestCreateLLM:
    """Testes para a função create_llm"""

    def test_llm_exists(self):
        """Verifica se a função create_llm existe"""
        assert create_llm is not None
        assert callable(create_llm)

    def test_llm_creation(self):
        """Verifica se create_llm retorna um LLM válido"""
        llm = create_llm()
        assert llm is not None

        # Verifica se é um ChatOpenAI
        assert hasattr(llm, 'model_name') or hasattr(llm, 'model')

    def test_llm_configuration(self):
        """Verifica configurações do LLM"""
        llm = create_llm()

        # Verifica modelo
        model = getattr(llm, 'model_name', None) or getattr(llm, 'model', None)
        assert model == "gpt-5-nano"

        # Verifica temperature
        assert llm.temperature is not None or hasattr(llm, 'model_kwargs')
        # Temperature pode estar em model_kwargs ou como atributo direto
        if llm.temperature is not None:
            assert llm.temperature == 0


class TestBasicAgent:
    """Testes para o agente criado"""

    def test_agent_creation(self):
        """Verifica se o agente é criado sem erros"""
        agent = create_basic_agent()
        assert agent is not None

    def test_agent_is_callable(self):
        """Verifica se o agente pode ser invocado"""
        agent = create_basic_agent()

        # Na API 1.0+, o agente tem método invoke
        assert hasattr(agent, 'invoke')
        assert callable(agent.invoke)

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_can_respond(self):
        """Testa se o agente consegue responder perguntas simples"""
        print("\n" + "="*70)
        print(" TESTE: Primeiro Agente")
        print("="*70)

        agent = create_basic_agent()

        question = "Diga apenas 'OK'"
        print(f"\n Pergunta: {question}")

        # API 1.0+ usa messages
        result = agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })

        # Verifica que retornou messages
        assert "messages" in result
        assert len(result["messages"]) > 0

        # Verifica que a última mensagem tem conteúdo
        last_message = result["messages"][-1]
        assert hasattr(last_message, 'content')
        assert len(last_message.content) > 0

        print(f"\n Resposta: {last_message.content}")
        print(f"\n Total de mensagens: {len(result['messages'])}")
        print("="*70)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
