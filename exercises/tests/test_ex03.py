"""
Testes para Exercício 3: Memory e Context
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
ex03 = import_exercise(1, 'ex03_memory')
create_code_reader_with_memory = ex03.create_code_reader_with_memory


class TestAgentWithMemory:
    """Testes para o agente com memória"""
    
    @pytest.fixture
    def api_key(self):
        """Obtém API key do ambiente de teste"""
        return os.getenv("OPENAI_API_KEY", "test-key")
    
    def test_agent_creation(self, api_key):
        """Verifica se o agente é criado"""
        agent = create_code_reader_with_memory(api_key)
        assert agent is not None
    
    def test_agent_has_memory(self, api_key):
        """Verifica se o agente tem memória configurada"""
        agent = create_code_reader_with_memory(api_key)
        assert hasattr(agent, 'memory')
        assert agent.memory is not None
        
        # Deve ter memory_key configurado
        assert hasattr(agent.memory, 'memory_key')
        assert agent.memory.memory_key == "chat_history"
    
    def test_agent_has_tools(self, api_key):
        """Verifica se o agente tem ferramentas"""
        agent = create_code_reader_with_memory(api_key)
        assert hasattr(agent, 'tools')
        assert len(agent.tools) >= 2
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_remembers_context(self, api_key):
        """Testa se o agente lembra do contexto entre perguntas"""
        agent = create_code_reader_with_memory(api_key)
        
        # Primeira pergunta
        result1 = agent.invoke({
            "input": "Liste os arquivos em sample_project"
        })
        assert "output" in result1
        
        # Segunda pergunta que depende do contexto
        # O agente deve usar a memória para entender "o primeiro"
        result2 = agent.invoke({
            "input": "Qual foi o primeiro arquivo que você mencionou?"
        })
        
        assert "output" in result2
        output = result2["output"]
        
        # Deve mencionar um arquivo específico (usando memória)
        assert len(output) > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
