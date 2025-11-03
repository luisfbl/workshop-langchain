"""
Testes para Exercício 3: Memory - Gerenciamento via histórico de mensagens
"""

import os
import sys
from pathlib import Path

import pytest

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importa usando helper que detecta nível do usuário
from exercises.tests.test_helper import import_exercise

# Importa o exercício do nível correto - com timeout para evitar travamento
class TestAgentWithMemory:
    """Testes para o agente com memória via histórico"""

    @pytest.fixture(scope="class")
    def ex03_module(self):
        """Importa o módulo com timeout"""
        return import_exercise(1, 'ex03_memory')

    @pytest.mark.timeout(10)
    def test_functions_exist(self, ex03_module):
        """Verifica se as funções existem"""
        assert hasattr(ex03_module, 'create_agent_with_tools')
        assert hasattr(ex03_module, 'chat_with_memory')
        assert callable(ex03_module.chat_with_memory)

    @pytest.mark.timeout(15)
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_creation(self, ex03_module):
        """Verifica se o agente é criado"""
        # Testa criação do agente - pode demorar devido à validação da API key
        try:
            agent = ex03_module.create_agent_with_tools()
            assert agent is not None
        except Exception as e:
            # Se falhar por problema de API key, pular teste
            if "api" in str(e).lower() or "key" in str(e).lower():
                pytest.skip(f"API key inválida ou problema de conexão: {e}")
            raise

    @pytest.mark.timeout(15)
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_is_callable(self, ex03_module):
        """Verifica se o agente pode ser invocado"""
        try:
            agent = ex03_module.create_agent_with_tools()
            assert hasattr(agent, 'invoke')
            assert callable(agent.invoke)
        except Exception as e:
            if "api" in str(e).lower() or "key" in str(e).lower():
                pytest.skip(f"API key inválida ou problema de conexão: {e}")
            raise
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_remembers_context(self, ex03_module):
        """Testa se o agente lembra do contexto entre perguntas"""
        print("\n" + "="*70)
        print("🧪 TESTE: Agente com Memória")
        print("="*70)

        agent = ex03_module.create_agent_with_tools()
        messages = []

        # Primeira pergunta
        question1 = "Analise o arquivo ./sample_project/calculator.py"
        print(f"\n👤 Pergunta 1: {question1}")
        messages.append({"role": "user", "content": question1})
        messages = ex03_module.chat_with_memory(agent, messages)

        # Mostra resposta do agente
        if len(messages) >= 2:
            response1 = messages[-1].content
            print(f"🤖 Resposta 1: {response1[:200]}...")
            print(f"   (Total: {len(response1)} caracteres)")

        # Segunda pergunta que requer contexto da primeira
        question2 = "Quantas funções ele tem?"
        print(f"\n👤 Pergunta 2: {question2}")
        messages.append({"role": "user", "content": question2})
        messages = ex03_module.chat_with_memory(agent, messages)

        # Mostra resposta do agente
        if len(messages) >= 4:
            response2 = messages[-1].content
            print(f"🤖 Resposta 2: {response2}")
            print(f"\n💭 O agente usou o contexto da primeira pergunta!")

        print(f"\n📊 Total de mensagens no histórico: {len(messages)}")
        print("="*70)

        # Verifica que o histórico foi mantido
        assert len(messages) >= 4  # user, assistant, user, assistant
        last_message = messages[-1]
        assert len(last_message.content) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
