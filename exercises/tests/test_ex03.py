"""
Testes para Exercício 3: Múltiplas Tools
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
ex03 = import_exercise(1, 'ex02_multiple_tools')


class TestMultipleTools:
    """Testes para múltiplas ferramentas"""

    def test_read_file_exists(self):
        """Verifica se a ferramenta read_file existe"""
        assert hasattr(ex03, 'read_file')
        assert hasattr(ex03.read_file, 'invoke')
        assert hasattr(ex03.read_file, 'description')

    def test_count_lines_exists(self):
        """Verifica se a ferramenta count_lines existe"""
        assert hasattr(ex03, 'count_lines')
        assert hasattr(ex03.count_lines, 'invoke')
        assert hasattr(ex03.count_lines, 'description')


class TestMultiToolAgent:
    """Testes para o agente com múltiplas tools"""

    def test_agent_creation(self):
        """Verifica se o agente é criado"""
        agent = ex03.create_multi_tool_agent()
        assert agent is not None

    def test_agent_has_multiple_tools(self):
        """Verifica se o agente tem múltiplas tools"""
        agent = ex03.create_multi_tool_agent()
        assert hasattr(agent, 'invoke')
        assert callable(agent.invoke)

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_can_use_tools(self):
        """Testa se o agente consegue usar as tools"""
        print("\n" + "="*70)
        print("🧪 TESTE: Agente com Múltiplas Tools")
        print("="*70)

        agent = ex03.create_multi_tool_agent()

        question = "Leia o arquivo ./sample_project/calculator.py e me diga quantas linhas ele tem"
        print(f"\n👤 Pergunta: {question}")

        result = agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })

        assert "messages" in result
        last_message = result["messages"][-1]

        print(f"\n🤖 Resposta: {last_message.content}")
        print(f"\n📊 Total de mensagens: {len(result['messages'])}")
        print("="*70)

        # Deve mencionar informações sobre o arquivo
        assert len(last_message.content) > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
