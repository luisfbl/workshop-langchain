"""
Testes para Exercício 6: Saída Estruturada com Pydantic
"""

import os
import sys
from pathlib import Path
import json

import pytest

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importa usando helper que detecta nível do usuário
from exercises.tests.test_helper import import_exercise

# Importa o exercício do nível correto
ex06 = import_exercise(1, 'ex06_structured_output')


class TestPydanticModels:
    """Testes para os models Pydantic"""

    def test_function_info_exists(self):
        """Verifica se FunctionInfo existe"""
        assert hasattr(ex06, 'FunctionInfo')

    def test_file_analysis_exists(self):
        """Verifica se FileAnalysis existe"""
        assert hasattr(ex06, 'FileAnalysis')
        
    def test_function_info_has_correct_fields(self):
        """Verifica se FunctionInfo tem os campos corretos"""
        func_info = ex06.FunctionInfo(
            name="test_func",
            args=["arg1", "arg2"],
            has_docstring=True,
            docstring="Test docstring"
        )
        assert func_info.name == "test_func"
        assert func_info.args == ["arg1", "arg2"]
        assert func_info.has_docstring == True
        assert func_info.docstring == "Test docstring"

    def test_file_analysis_has_correct_fields(self):
        """Verifica se FileAnalysis tem os campos corretos"""
        func = ex06.FunctionInfo(
            name="test",
            args=[],
            has_docstring=False,
            docstring=None
        )
        analysis = ex06.FileAnalysis(
            file_name="test.py",
            file_path="/path/to/test.py",
            total_lines=10,
            functions=[func],
            needs_documentation=True
        )
        assert analysis.file_name == "test.py"
        assert analysis.total_lines == 10
        assert len(analysis.functions) == 1
        assert analysis.needs_documentation == True


class TestAnalyzeTool:
    """Testes para a tool de análise"""

    def test_analyze_file_structured_exists(self):
        """Verifica se analyze_file_structured existe"""
        assert hasattr(ex06, 'analyze_file_structured')

    def test_analyze_file_structured_returns_json(self):
        """Testa se analyze_file_structured retorna JSON válido"""
        # Cria arquivo de teste
        test_file = Path("test_structured.py")
        test_content = '''def test_func(arg1, arg2):
    """Test function"""
    pass

def no_doc_func():
    pass
'''
        test_file.write_text(test_content)
        
        try:
            result = ex06.analyze_file_structured.invoke({"file_path": str(test_file)})
            
            # Verifica se é JSON válido
            data = json.loads(result)
            
            # Verifica campos esperados
            assert "file_name" in data
            assert "total_lines" in data
            assert "functions" in data
            assert "needs_documentation" in data
            
            # Verifica que encontrou 2 funções
            assert len(data["functions"]) == 2
            
            # Verifica que precisa documentação (no_doc_func não tem docstring)
            assert data["needs_documentation"] == True
            
        finally:
            if test_file.exists():
                test_file.unlink()


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

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    @pytest.mark.timeout(30)
    def test_agent_analyzes_file(self):
        """Testa se o agente analisa arquivo e retorna informações estruturadas"""
        agent = ex06.create_structured_agent()
        
        # Cria arquivo de teste
        test_file = Path("test_agent_analysis.py")
        test_content = '''def greet(name):
    """Greets a person"""
    return f"Hello, {name}"
'''
        test_file.write_text(test_content)
        
        try:
            response = agent.invoke({
                "messages": [{"role": "user", "content": f"Analise o arquivo {test_file} de forma estruturada"}]
            })
            
            last_message = response['messages'][-1].content
            
            # Verifica se a resposta contém informações da análise
            # O agente pode retornar em texto ou JSON, ambos são válidos
            assert "greet" in last_message.lower()  # Nome da função
            assert "name" in last_message.lower()  # Argumento
            
        finally:
            if test_file.exists():
                test_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
