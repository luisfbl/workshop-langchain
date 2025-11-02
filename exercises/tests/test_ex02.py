"""
Testes para Exercício 2: Múltiplas Tools - Code Reader
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
ex02 = import_exercise(1, 'ex02_code_reader')
list_python_files = ex02.list_python_files
read_file = ex02.read_file
create_code_reader_agent = ex02.create_code_reader_agent


class TestTools:
    """Testes para as ferramentas"""
    
    def test_list_python_files_exists(self):
        """Verifica se a ferramenta list_python_files foi criada"""
        assert list_python_files is not None
        assert callable(list_python_files)
        assert hasattr(list_python_files, 'description')
    
    def test_read_file_exists(self):
        """Verifica se a ferramenta read_file foi criada"""
        assert read_file is not None
        assert callable(read_file)
        assert hasattr(read_file, 'description')
    
    def test_list_python_files_works(self, tmp_path):
        """Testa listagem de arquivos"""
        (tmp_path / "test1.py").write_text("# test")
        (tmp_path / "test2.py").write_text("# test")
        
        result = list_python_files.invoke(str(tmp_path))
        assert "test1.py" in result
        assert "test2.py" in result
    
    def test_read_file_works(self, tmp_path):
        """Testa leitura de arquivo"""
        test_file = tmp_path / "test.py"
        test_content = "def hello():\n    return 'world'"
        test_file.write_text(test_content)
        
        result = read_file.invoke(str(test_file))
        assert "hello" in result
        assert "world" in result


class TestCodeReaderAgent:
    """Testes para o agente"""
    
    @pytest.fixture
    def api_key(self):
        """Obtém API key do ambiente de teste"""
        return os.getenv("OPENAI_API_KEY", "test-key")
    
    def test_agent_creation(self, api_key):
        """Verifica se o agente é criado"""
        agent = create_code_reader_agent(api_key)
        assert agent is not None
    
    def test_agent_has_multiple_tools(self, api_key):
        """Verifica se o agente tem múltiplas ferramentas"""
        agent = create_code_reader_agent(api_key)
        assert hasattr(agent, 'tools')
        
        # Deve ter pelo menos 2 tools
        assert len(agent.tools) >= 2
        
        tool_names = [tool.name for tool in agent.tools]
        assert 'list_python_files' in tool_names
        assert 'read_file' in tool_names
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_can_read_code(self, api_key):
        """Testa se o agente consegue ler código"""
        agent = create_code_reader_agent(api_key)
        
        result = agent.invoke({
            "input": "Leia o arquivo sample_project/calculator.py e me diga o que ele contém"
        })
        
        assert "output" in result
        output = result["output"]
        
        # Deve mencionar algo sobre o conteúdo
        assert len(output) > 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
