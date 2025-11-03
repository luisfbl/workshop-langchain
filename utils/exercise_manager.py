"""
Gerenciador de exercícios - copia exercícios baseado no nível do usuário
"""
import shutil
from pathlib import Path


class ExerciseManager:
    """Gerencia a cópia de exercícios baseado no nível do usuário"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.exercises_source = project_root / "exercises_source"
        self.exercises_dir = project_root / "exercises"

    def are_exercises_configured(self, level: str) -> bool:
        """
        Verifica se os exercícios do nível já estão configurados

        Args:
            level: "easy" ou "medium"

        Returns:
            True se exercícios já estão configurados, False caso contrário
        """
        # Verifica se há exercícios nos diretórios day1 e day2
        for day in ["day1", "day2"]:
            target_day = self.exercises_dir / day

            if not target_day.exists():
                return False

            # Verifica se há pelo menos um arquivo .py
            has_exercises = any(target_day.glob("ex*.py"))
            if not has_exercises:
                return False

        return True

    def setup_user_exercises(self, level: str, force: bool = False) -> bool:
        """
        Copia os exercícios do nível escolhido para a pasta exercises/

        Args:
            level: "easy" ou "medium"
            force: Se True, recopia mesmo se já estiver configurado

        Returns:
            True se sucesso, False se erro
        """
        try:
            # Verifica se já está configurado (a menos que force=True)
            if not force and self.are_exercises_configured(level):
                return True

            # Limpa exercícios antigos (mantém apenas tests/ e main.py)
            self._clean_exercises_dir()

            # Copia exercícios do nível escolhido
            for day in ["day1", "day2"]:
                source_day = self.exercises_source / day / level
                target_day = self.exercises_dir / day

                if source_day.exists():
                    # Cria diretório de destino
                    target_day.mkdir(parents=True, exist_ok=True)

                    # Copia todos os arquivos .py
                    for exercise_file in source_day.glob("*.py"):
                        target_file = target_day / exercise_file.name
                        shutil.copy2(exercise_file, target_file)

            return True

        except Exception as e:
            print(f"Erro ao configurar exercícios: {e}")
            return False

    def _clean_exercises_dir(self):
        """Remove exercícios antigos, mantendo tests/ e main.py"""
        for item in self.exercises_dir.iterdir():
            # Mantém apenas tests/ e main.py
            if item.name in ["tests", "main.py", "__pycache__"]:
                continue

            # Remove diretórios day1, day2, etc
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    def get_available_exercises(self, level: str) -> list[str]:
        """
        Retorna lista de exercícios disponíveis para o nível

        Args:
            level: "easy" ou "medium"

        Returns:
            Lista de nomes de arquivos de exercícios
        """
        exercises = []

        for day in ["day1", "day2"]:
            source_day = self.exercises_source / day / level

            if source_day.exists():
                for exercise_file in sorted(source_day.glob("ex*.py")):
                    exercises.append(exercise_file.name)

        return exercises
