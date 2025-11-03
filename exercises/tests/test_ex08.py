"""
Testes para Exercício 8: Orchestrator Avançado com Checkpointing
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
ex08 = import_exercise(2, 'ex07_orchestrator_advanced')


class TestOrchestratorStructures:
    """Testes para estruturas do orchestrator"""

    def test_error_type_exists(self):
        """Verifica se ErrorType existe"""
        assert hasattr(ex08, 'ErrorType')

    def test_retry_config_exists(self):
        """Verifica se RetryConfig existe"""
        assert hasattr(ex08, 'RetryConfig')

    def test_checkpoint_data_exists(self):
        """Verifica se CheckpointData existe"""
        assert hasattr(ex08, 'CheckpointData')

    def test_advanced_state_exists(self):
        """Verifica se AdvancedOrchestratorState existe"""
        assert hasattr(ex08, 'AdvancedOrchestratorState')


class TestCheckpointFunctions:
    """Testes para funções de checkpoint"""

    def test_save_checkpoint_exists(self):
        """Verifica se save_checkpoint existe"""
        assert hasattr(ex08, 'save_checkpoint')
        assert callable(ex08.save_checkpoint)

    def test_load_checkpoint_exists(self):
        """Verifica se load_checkpoint existe"""
        assert hasattr(ex08, 'load_checkpoint')
        assert callable(ex08.load_checkpoint)


class TestRetryLogic:
    """Testes para lógica de retry"""

    def test_classify_error_exists(self):
        """Verifica se classify_error existe"""
        assert hasattr(ex08, 'classify_error')
        assert callable(ex08.classify_error)

    def test_should_retry_exists(self):
        """Verifica se should_retry existe"""
        assert hasattr(ex08, 'should_retry')
        assert callable(ex08.should_retry)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
