"""
Testes para Exercício 7: LangGraph com Processamento Paralelo
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
ex07 = import_exercise(2, 'ex07_langgraph_parallel')


class TestParallelStructures:
    """Testes para estruturas de dados paralelas"""

    def test_file_result_exists(self):
        """Verifica se FileResult existe"""
        assert hasattr(ex07, 'FileResult')

    def test_parallel_state_exists(self):
        """Verifica se ParallelDocGenState existe"""
        assert hasattr(ex07, 'ParallelDocGenState')


class TestParallelFunctions:
    """Testes para funções de processamento paralelo"""

    def test_analyze_single_file_exists(self):
        """Verifica se analyze_single_file existe"""
        assert hasattr(ex07, 'analyze_single_file')
        assert callable(ex07.analyze_single_file)

    def test_list_files_node_exists(self):
        """Verifica se list_files_node existe"""
        assert hasattr(ex07, 'list_files_node')
        assert callable(ex07.list_files_node)

    def test_process_parallel_node_exists(self):
        """Verifica se process_files_parallel_node existe"""
        assert hasattr(ex07, 'process_files_parallel_node')
        assert callable(ex07.process_files_parallel_node)

    def test_combine_results_node_exists(self):
        """Verifica se combine_results_node existe"""
        assert hasattr(ex07, 'combine_results_node')
        assert callable(ex07.combine_results_node)


class TestParallelGraph:
    """Testes para o graph paralelo"""

    def test_create_parallel_graph_exists(self):
        """Verifica se create_parallel_graph existe"""
        assert hasattr(ex07, 'create_parallel_graph')
        assert callable(ex07.create_parallel_graph)

    def test_run_parallel_workflow_exists(self):
        """Verifica se run_parallel_workflow existe"""
        assert hasattr(ex07, 'run_parallel_workflow')
        assert callable(ex07.run_parallel_workflow)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
