"""
Testes para Exercício 5: State Management Avançado
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
ex05 = import_exercise(1, 'ex04_state_management')


class TestStateManagementStructures:
    """Testes para estruturas de dados"""

    def test_file_metrics_exists(self):
        """Verifica se FileMetrics existe"""
        assert hasattr(ex05, 'FileMetrics')
        FileMetrics = ex05.FileMetrics
        # Testa se é dataclass
        assert hasattr(FileMetrics, '__dataclass_fields__')

    def test_quality_state_exists(self):
        """Verifica se QualityState existe"""
        assert hasattr(ex05, 'QualityState')


class TestAnalysisFunctions:
    """Testes para funções de análise"""

    def test_analyze_file_exists(self):
        """Verifica se analyze_file existe"""
        assert hasattr(ex05, 'analyze_file')
        assert callable(ex05.analyze_file)

    def test_calculate_complexity_exists(self):
        """Verifica se calculate_complexity existe"""
        assert hasattr(ex05, 'calculate_complexity')
        assert callable(ex05.calculate_complexity)

    def test_calculate_quality_score_exists(self):
        """Verifica se calculate_quality_score existe"""
        assert hasattr(ex05, 'calculate_quality_score')
        assert callable(ex05.calculate_quality_score)


class TestQualityPipeline:
    """Testes para o pipeline de qualidade"""

    def test_initialize_quality_state_exists(self):
        """Verifica se initialize_quality_state existe"""
        assert hasattr(ex05, 'initialize_quality_state')
        assert callable(ex05.initialize_quality_state)

    def test_process_file_stage_exists(self):
        """Verifica se process_file_stage existe"""
        assert hasattr(ex05, 'process_file_stage')
        assert callable(ex05.process_file_stage)

    def test_generate_quality_report_exists(self):
        """Verifica se generate_quality_report existe"""
        assert hasattr(ex05, 'generate_quality_report')
        assert callable(ex05.generate_quality_report)

    def test_run_quality_pipeline_exists(self):
        """Verifica se run_quality_pipeline existe"""
        assert hasattr(ex05, 'run_quality_pipeline')
        assert callable(ex05.run_quality_pipeline)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
