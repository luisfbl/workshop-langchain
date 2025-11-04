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
from exercises.tests.test_helper import import_exercise, get_user_level

# Importa o exercício do nível correto
ex03 = import_exercise(1, 'ex03_multiple_tools')


class TestToolsExist:
    """Testes para verificar se as tools existem"""

    def test_list_python_files_exists(self):
        """Verifica se list_python_files existe"""
        assert hasattr(ex03, 'list_python_files')

    def test_read_file_exists(self):
        """Verifica se read_file existe"""
        assert hasattr(ex03, 'read_file')

    def test_count_lines_exists(self):
        """Verifica se count_lines existe"""
        assert hasattr(ex03, 'count_lines')

    def test_create_multi_tool_agent_exists(self):
        """Verifica se create_multi_tool_agent existe"""
        assert hasattr(ex03, 'create_multi_tool_agent')
        assert callable(ex03.create_multi_tool_agent)


class TestToolFunctions:
    """Testes para as funções das tools"""

    def test_list_python_files_tool(self):
        """Testa a tool list_python_files"""
        # Testa com diretório que existe
        result = ex03.list_python_files.invoke({"directory": "./sample_project"})
        assert isinstance(result, str)
        # Deve encontrar pelo menos calculator.py
        assert "calculator.py" in result or "Nenhum arquivo" in result

    def test_read_file_tool(self):
        """Testa a tool read_file"""
        # Cria um arquivo temporário para teste
        test_file = Path("test_temp.py")
        test_content = "# Test file\nprint('hello')\n"
        test_file.write_text(test_content)
        
        try:
            result = ex03.read_file.invoke({"file_path": str(test_file)})
            assert isinstance(result, str)
            assert "Test file" in result
        finally:
            test_file.unlink()

    def test_read_file_not_found(self):
        """Testa read_file com arquivo inexistente"""
        result = ex03.read_file.invoke({"file_path": "arquivo_que_nao_existe.py"})
        assert "Erro" in result or "não encontrado" in result

    def test_count_lines_tool(self):
        """Testa a tool count_lines"""
        # Cria um arquivo temporário para teste
        test_file = Path("test_temp.py")
        test_content = """# Comment
print('hello')

# Another comment
print('world')
"""
        test_file.write_text(test_content)
        
        try:
            result = ex03.count_lines.invoke({"file_path": str(test_file)})
            assert isinstance(result, str)
            # Deve contar 2 linhas de código (ignora comentários e vazias)
            assert "2" in result
        finally:
            test_file.unlink()


class TestAgentCreation:
    """Testes para criação do agente"""

    def test_agent_creation(self):
        """Verifica se o agente é criado"""
        agent = ex03.create_multi_tool_agent()
        assert agent is not None

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    @pytest.mark.timeout(30)
    def test_agent_uses_tools(self):
        """Testa se o agente usa as tools corretamente"""
        agent = ex03.create_multi_tool_agent()
        
        # Cria arquivo de teste
        test_file = Path("test_agent.py")
        test_file.write_text("print('test')\n")
        
        try:
            # Testa se o agente lista arquivos
            response = agent.invoke({
                "messages": [{"role": "user", "content": "Liste arquivos Python no diretório atual"}]
            })
            assert response is not None
            
        finally:
            if test_file.exists():
                test_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
