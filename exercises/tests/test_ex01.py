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
list_python_files = ex01.list_python_files
create_file_explorer_agent = ex01.create_file_explorer_agent


class TestListPythonFiles:
    """Testes para a ferramenta list_python_files"""
    
    def test_tool_exists(self):
        """Verifica se a ferramenta foi criada"""
        assert list_python_files is not None
        assert callable(list_python_files)
    
    def test_tool_has_docstring(self):
        """Verifica se a ferramenta tem docstring"""
        # O decorator @tool expõe a docstring via description
        assert hasattr(list_python_files, 'description')
        assert len(list_python_files.description) > 20
    
    def test_lists_python_files(self, tmp_path):
        """Testa se lista arquivos Python corretamente"""
        # Cria arquivos de teste
        (tmp_path / "test1.py").write_text("# test")
        (tmp_path / "test2.py").write_text("# test")
        (tmp_path / "test.txt").write_text("# not python")
        
        result = list_python_files.invoke(str(tmp_path))
        
        assert "test1.py" in result
        assert "test2.py" in result
        assert "test.txt" not in result
    
    def test_handles_empty_directory(self, tmp_path):
        """Testa diretório vazio"""
        result = list_python_files.invoke(str(tmp_path))
        # Deve retornar alguma mensagem, não erro
        assert isinstance(result, str)
        assert len(result) > 0


class TestFileExplorerAgent:
    """Testes para o agente criado"""
    
    @pytest.fixture
    def api_key(self):
        """Obtém API key do ambiente de teste"""
        return os.getenv("OPENAI_API_KEY", "test-key")
    
    def test_agent_creation(self, api_key):
        """Verifica se o agente é criado sem erros"""
        agent = create_file_explorer_agent(api_key)
        assert agent is not None
    
    def test_agent_has_tools(self, api_key):
        """Verifica se o agente tem ferramentas configuradas"""
        agent = create_file_explorer_agent(api_key)
        assert hasattr(agent, 'tools')
        assert len(agent.tools) > 0
        
        # Deve ter list_python_files
        tool_names = [tool.name for tool in agent.tools]
        assert 'list_python_files' in tool_names
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_can_list_files(self, api_key):
        """Testa se o agente consegue listar arquivos"""
        agent = create_file_explorer_agent(api_key)
        
        result = agent.invoke({
            "input": "Liste os arquivos Python no diretório sample_project"
        })
        
        assert "output" in result
        output = result["output"]
        
        # Deve mencionar pelo menos um arquivo Python
        assert "calculator" in output.lower() or ".py" in output.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
