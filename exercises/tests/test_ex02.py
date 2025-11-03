"""
Testes para Exercício 2: Primeira Tool
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
ex02 = import_exercise(1, 'ex02_first_tool')
list_python_files = ex02.list_python_files
create_agent_with_tool = ex02.create_agent_with_tool


class TestTools:
    """Testes para as ferramentas"""
    
    def test_list_python_files_exists(self):
        """Verifica se a ferramenta list_python_files foi criada"""
        assert list_python_files is not None
        # StructuredTool não é diretamente callable, mas tem invoke
        assert hasattr(list_python_files, 'invoke')
        assert hasattr(list_python_files, 'description')
        assert list_python_files.description is not None
    
    def test_list_python_files_works(self, tmp_path):
        """Testa listagem de arquivos"""
        (tmp_path / "test1.py").write_text("# test")
        (tmp_path / "test2.py").write_text("# test")

        result = list_python_files.invoke({"directory": str(tmp_path)})
        assert "test1.py" in result
        assert "test2.py" in result


class TestAgentWithTool:
    """Testes para o agente com tool"""

    def test_agent_creation(self):
        """Verifica se o agente é criado"""
        agent = create_agent_with_tool()
        assert agent is not None

    def test_agent_has_tool(self):
        """Verifica se o agente tem a tool list_python_files"""
        agent = create_agent_with_tool()
        # Na API 1.0+, o agente é um CompiledStateGraph
        assert hasattr(agent, 'invoke')
        assert callable(agent.invoke)

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_agent_can_use_tool(self):
        """Testa se o agente consegue usar a tool"""
        print("\n" + "="*70)
        print("🧪 TESTE: Agente usando Tool")
        print("="*70)

        agent = create_agent_with_tool()

        question = "Liste os arquivos Python no diretório ./sample_project"
        print(f"\n👤 Pergunta: {question}")

        result = agent.invoke({
            "messages": [{"role": "user", "content": question}]
        })

        assert "messages" in result
        last_message = result["messages"][-1]

        print(f"\n🤖 Resposta: {last_message.content}")
        print(f"\n📊 Total de mensagens: {len(result['messages'])}")
        print("="*70)

        # Deve mencionar alguns arquivos
        assert len(last_message.content) > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
