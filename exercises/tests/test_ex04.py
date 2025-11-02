"""
Testes para Exercício 4: Code Analyzer Especializado
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
ex04 = import_exercise(1, 'ex04_code_analyzer')
create_code_quality_analyzer = ex04.create_code_quality_analyzer


class TestCodeQualityTools:
    """Testes para as ferramentas de análise"""
    
    def test_check_docstrings_exists(self):
        """Verifica se a ferramenta check_docstrings existe"""
        # Importa a ferramenta do módulo
        module = import_exercise(1, 'ex04_code_analyzer')
        assert hasattr(module, 'check_docstrings')
        tool = module.check_docstrings
        assert callable(tool)
        assert hasattr(tool, 'description')
    
    def test_count_lines_exists(self):
        """Verifica se a ferramenta count_lines existe"""
        module = import_exercise(1, 'ex04_code_analyzer')
        assert hasattr(module, 'count_lines')
        tool = module.count_lines
        assert callable(tool)
        assert hasattr(tool, 'description')


class TestCodeQualityAnalyzer:
    """Testes para o agente analisador"""
    
    @pytest.fixture
    def api_key(self):
        """Obtém API key do ambiente de teste"""
        return os.getenv("OPENAI_API_KEY", "test-key")
    
    def test_agent_creation(self, api_key):
        """Verifica se o agente é criado"""
        agent = create_code_quality_analyzer(api_key)
        assert agent is not None
    
    def test_agent_has_quality_tools(self, api_key):
        """Verifica se o agente tem ferramentas de qualidade"""
        agent = create_code_quality_analyzer(api_key)
        assert hasattr(agent, 'tools')
        assert len(agent.tools) >= 2
        
        tool_names = [tool.name for tool in agent.tools]
        # Deve ter pelo menos check_docstrings e count_lines
        assert 'check_docstrings' in tool_names or 'check_docstrings_and_types' in tool_names
        assert 'count_lines' in tool_names
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_analyzes_code_quality(self, api_key):
        """Testa se o agente analisa qualidade de código"""
        agent = create_code_quality_analyzer(api_key)
        
        result = agent.invoke({
            "input": "Analise a qualidade do código em sample_project/utils.py"
        })
        
        assert "output" in result
        output = result["output"]
        
        # Deve fornecer alguma análise
        assert len(output) > 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
