"""
Testes para Exercício 6: Saída Estruturada com Pydantic
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
ex06 = import_exercise(1, 'ex05_structured_output')


class TestPydanticModels:
    """Testes para os models Pydantic"""

    def test_function_info_exists(self):
        """Verifica se FunctionInfo existe"""
        assert hasattr(ex06, 'FunctionInfo')

    def test_class_info_exists(self):
        """Verifica se ClassInfo existe"""
        assert hasattr(ex06, 'ClassInfo')

    def test_file_analysis_exists(self):
        """Verifica se FileAnalysis existe"""
        assert hasattr(ex06, 'FileAnalysis')


class TestAnalyzeTool:
    """Testes para a tool de análise"""

    def test_analyze_file_complete_exists(self):
        """Verifica se analyze_file_complete existe"""
        assert hasattr(ex06, 'analyze_file_complete')
        assert hasattr(ex06.analyze_file_complete, 'invoke')


class TestStructuredAgent:
    """Testes para o agente estruturado"""

    def test_agent_creation(self):
        """Verifica se o agente é criado"""
        agent = ex06.create_structured_agent()
        assert agent is not None

    def test_agent_is_callable(self):
        """Verifica se o agente pode ser invocado"""
        agent = ex06.create_structured_agent()
        assert hasattr(agent, 'invoke')
        assert callable(agent.invoke)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
