"""
Testes para Exercício 5: State Management
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
ex05 = import_exercise(1, 'ex05_state_management')


class TestStateStructure:
    """Testes para estrutura do State"""

    def test_analysis_state_exists(self):
        """Verifica se AnalysisState existe"""
        assert hasattr(ex05, 'AnalysisState')

    def test_initialize_state_exists(self):
        """Verifica se initialize_state existe"""
        assert hasattr(ex05, 'initialize_state')
        assert callable(ex05.initialize_state)

    def test_process_next_file_exists(self):
        """Verifica se process_next_file existe"""
        assert hasattr(ex05, 'process_next_file')
        assert callable(ex05.process_next_file)


class TestStateFunctions:
    """Testes para funções que trabalham com state"""

    def test_initialize_state_creates_correct_structure(self):
        """Testa se initialize_state cria estrutura correta"""
        # Cria diretório temporário com arquivo de teste
        test_dir = Path("test_temp_dir")
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / "test.py"
        test_file.write_text("print('test')\n")
        
        try:
            state = ex05.initialize_state(str(test_dir))
            
            # Verifica campos obrigatórios
            assert "files_to_process" in state
            assert "files_processed" in state
            assert "current_file" in state
            assert "total_functions" in state
            assert "total_lines" in state
            assert "errors" in state
            
            # Verifica valores iniciais
            assert isinstance(state["files_to_process"], list)
            assert isinstance(state["files_processed"], list)
            assert state["total_functions"] == 0
            assert state["total_lines"] == 0
            assert state["errors"] == []
            
        finally:
            test_file.unlink()
            test_dir.rmdir()

    def test_process_next_file_updates_state(self):
        """Testa se process_next_file atualiza state corretamente"""
        # Cria arquivo de teste
        test_file = Path("test_process.py")
        test_content = """def test_func():
    pass

def another_func():
    return 42
"""
        test_file.write_text(test_content)
        
        try:
            # Cria state inicial
            state = ex05.AnalysisState(
                files_to_process=[str(test_file)],
                files_processed=[],
                current_file="",
                total_functions=0,
                total_lines=0,
                errors=[]
            )
            
            # Processa arquivo
            state = ex05.process_next_file(state)
            
            # Verifica atualizações
            assert len(state["files_to_process"]) == 0
            assert len(state["files_processed"]) == 1
            assert state["total_functions"] == 2  # Duas funções
            assert state["total_lines"] > 0
            
        finally:
            if test_file.exists():
                test_file.unlink()


class TestWorkflow:
    """Testes para workflow completo"""

    def test_run_analysis_workflow_exists(self):
        """Verifica se run_analysis_workflow existe"""
        assert hasattr(ex05, 'run_analysis_workflow')
        assert callable(ex05.run_analysis_workflow)

    def test_get_state_summary_exists(self):
        """Verifica se get_state_summary existe"""
        assert hasattr(ex05, 'get_state_summary')
        assert callable(ex05.get_state_summary)

    def test_workflow_processes_directory(self):
        """Testa se workflow processa diretório completo"""
        # Cria diretório temporário com múltiplos arquivos
        test_dir = Path("test_workflow_dir")
        test_dir.mkdir(exist_ok=True)
        
        try:
            # Cria 3 arquivos de teste
            for i in range(3):
                test_file = test_dir / f"test{i}.py"
                test_file.write_text(f"def func{i}():\n    pass\n")
            
            # Executa workflow
            final_state = ex05.run_analysis_workflow(str(test_dir))
            
            # Verifica resultados
            assert final_state is not None
            assert len(final_state["files_processed"]) == 3
            assert len(final_state["files_to_process"]) == 0
            assert final_state["total_functions"] == 3
            
        finally:
            # Limpa arquivos
            for f in test_dir.glob("*.py"):
                f.unlink()
            test_dir.rmdir()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
