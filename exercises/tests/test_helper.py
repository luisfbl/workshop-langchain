"""
Helper para importar exercícios do nível correto do usuário
"""
import os
import sys
from pathlib import Path

def get_user_level():
    """Detecta o nível do usuário (easy ou medium)"""
    # Tenta pegar do ambiente (setado pelo watcher)
    level = os.environ.get('WORKSHOP_LEVEL', 'medium')
    return level

def import_exercise(day: int, exercise_name: str):
    """
    Importa um exercício do nível correto do usuário

    Args:
        day: Número do dia (1 ou 2)
        exercise_name: Nome do arquivo do exercício (ex: 'ex01_first_agent')

    Returns:
        Módulo importado

    Nota: Os exercícios já estão filtrados por nível na pasta exercises/day{X}/
          pelo ExerciseManager, então não há subdire subddiretórios easy/medium
    """
    # Nova estrutura: exercises.day{X}.{exercise_name}
    # Os exercícios do nível do usuário já foram copiados para exercises/day{X}/
    module_path = f"exercises.day{day}.{exercise_name}"

    # Tenta importar
    try:
        import importlib
        module = importlib.import_module(module_path)
        return module
    except ImportError as e:
        raise ImportError(
            f"Não foi possível importar {exercise_name} de day{day}. "
            f"Verifique se o arquivo existe em exercises/day{day}/\n"
            f"Erro: {e}"
        )
