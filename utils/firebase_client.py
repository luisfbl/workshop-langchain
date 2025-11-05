import gzip
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


class FirebaseClient:
    """Cliente Firebase usando REST API"""

    config_path: Path
    database_url: str

    def __init__(self, config: str | None = None):
        config_path = None
        if config is None:
            config_path = (
                Path(__file__).parent.parent / "config" / "firebase_web_config.json"
            )

        if config_path is None or not config_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração do Firebase não encontrado: {config_path}\n" +
                "Certifique-se de que config/firebase_web_config.json existe."
            )

        self.config_path = Path(config_path)

        with open(self.config_path, 'r') as f:
            firebase_config = json.load(f)

        if 'databaseURL' not in firebase_config:
            raise ValueError(
                "O campo 'databaseURL' é obrigatório no arquivo de configuração.\n" +
                "Adicione: \"databaseURL\": \"https://{projectId}-default-rtdb.firebaseio.com\""
            )

        self.database_url = firebase_config['databaseURL'].rstrip('/')

    def _get(self, path: str) -> Any:
        """GET request para Firebase"""
        url = f"{self.database_url}/{path}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _put(self, path: str, data: Any) -> Any:
        """PUT request para Firebase (substitui dados)"""
        url = f"{self.database_url}/{path}.json"
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def _patch(self, path: str, data: Any) -> Any:
        """PATCH request para Firebase (atualiza dados)"""
        url = f"{self.database_url}/{path}.json"
        response = requests.patch(url, json=data)
        response.raise_for_status()
        return response.json()

    def _delete(self, path: str) -> Any:
        """DELETE request para Firebase"""
        url = f"{self.database_url}/{path}.json"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()

    def create_user(self, username: str, password_hash: str) -> str | None:
        try:
            # Sanitiza username para remover caracteres inválidos do Firebase (.,$,#,[,],/)
            sanitized_username = username.replace("$", "_").replace(".", "_").replace("#", "_").replace("[", "_").replace("]", "_").replace("/", "_")
            user_id = f"{sanitized_username}_{int(time.time())}"

            user_data = {
                "username": username,
                "password_hash": password_hash,
                "created_at": datetime.now().isoformat(),
                "level": None,
                "last_activity": datetime.now().isoformat(),
            }

            self._put(f"users/{user_id}", user_data)
            self._initialize_progress(user_id)

            return user_id
        except Exception as e:
            print(f"Erro ao criar usuário: [{e}] {e}")
            return None

    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        try:
            users = self._get("users")

            if users is None:
                return None

            for user_id, user_data in users.items():
                if user_data.get("username") == username:
                    user_data["user_id"] = user_id
                    return user_data

            return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def get_user(self, user_id: str) -> dict[str, Any] | None:
        try:
            data = self._get(f"users/{user_id}")

            if data is None:
                return None

            data["user_id"] = user_id
            return data
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def update_user_level(self, user_id: str, level: str):
        try:
            self._patch(f"users/{user_id}", {"level": level})
        except Exception as e:
            print(f"Erro ao atualizar nível: [{e}] {e}")

    def update_last_activity(self, user_id: str):
        try:
            self._patch(f"users/{user_id}", {
                "last_activity": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"Erro ao atualizar atividade: {e}")

    def _initialize_progress(self, user_id: str):
        progress_data: dict[str, Any] = {
            "current_exercise": 1,
            "completed_exercises": [],
            "exercise_attempts": {},
            "hints_used": {},
            "start_time": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "test_results": {},
        }
        self._put(f"progress/{user_id}", progress_data)

    def get_progress(self, user_id: str) -> dict[str, Any] | None:
        try:
            progress = self._get(f"progress/{user_id}")

            if progress is None:
                self._initialize_progress(user_id)
                return self.get_progress(user_id)

            return progress
        except Exception as e:
            print(f"Erro ao buscar progresso: {e}")
            return None

    def update_progress(self, user_id: str, updates: dict[str, Any]):
        try:
            updates["last_activity"] = datetime.now().isoformat()
            self._patch(f"progress/{user_id}", updates)
        except Exception as e:
            print(f"Erro ao atualizar progresso: {e}")

    def mark_exercise_complete(self, user_id: str, exercise_num: int):
        try:
            progress = self._get(f"progress/{user_id}")

            if progress is not None:
                if not isinstance(progress, dict):
                    print(f"Aviso: progress retornou tipo inesperado: {type(progress)}")
                    return
                completed = progress.get("completed_exercises", [])

                if exercise_num not in completed:
                    completed.append(exercise_num)
                    completed.sort()

                    self._patch(f"progress/{user_id}", {
                        "completed_exercises": completed,
                        "current_exercise": exercise_num + 1,
                        "last_activity": datetime.now().isoformat(),
                    })
        except Exception as e:
            print(f"Erro ao marcar exercício completo: {e}")

    def add_hint_used(self, user_id: str, exercise_num: int, hint_level: int):
        try:
            progress = self._get(f"progress/{user_id}")

            if progress is not None:
                if not isinstance(progress, dict):
                    print(f"Aviso: progress retornou tipo inesperado: {type(progress)}")
                    return
                hints = progress.get("hints_used", {})
                key = str(exercise_num)

                if key not in hints:
                    hints[key] = []

                if hint_level not in hints[key]:
                    hints[key].append(hint_level)
                    hints[key].sort()

                self._patch(f"progress/{user_id}", {
                    "hints_used": hints,
                    "last_activity": datetime.now().isoformat(),
                })
        except Exception as e:
            print(f"Erro ao registrar dica: {e}")

    def increment_attempt(self, user_id: str, exercise_num: int):
        """Incrementa contador de tentativas de um exercício"""
        try:
            progress = self._get(f"progress/{user_id}")

            data = {}
            if progress is not None:
                if isinstance(progress, dict):
                    data = progress

            attempts = data.get("exercise_attempts", {})
            if not isinstance(attempts, dict):
                attempts = {}

            key = str(exercise_num)
            attempts[key] = attempts.get(key, 0) + 1

            self._patch(f"progress/{user_id}", {
                "exercise_attempts": attempts,
                "last_activity": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"Erro ao incrementar tentativa: {e}")

    def save_test_result(self, user_id: str, exercise_num: int, passed: bool):
        try:
            progress = self._get(f"progress/{user_id}")

            data = {}
            if progress is not None:
                if isinstance(progress, dict):
                    data = progress

            results = data.get("test_results", {})
            if not isinstance(results, dict):
                results = {}

            key = str(exercise_num)

            if key not in results:
                results[key] = {"passed": False, "attempts": 0}

            results[key]["passed"] = passed
            results[key]["attempts"] = results[key].get("attempts", 0) + 1
            results[key]["last_attempt"] = datetime.now().isoformat()

            self._patch(f"progress/{user_id}", {
                "test_results": results,
                "last_activity": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")

    def save_exercise_solution(self, user_id: str, exercise_num: int, code: str):
        try:
            compressed = gzip.compress(code.encode("utf-8"))

            import base64
            compressed_b64 = base64.b64encode(compressed).decode("ascii")

            progress = self._get(f"progress/{user_id}")

            if progress is None:
                self._initialize_progress(user_id)
                progress = self._get(f"progress/{user_id}")

            if not isinstance(progress, dict):
                print(f"Erro: progress retornou tipo inesperado: {type(progress)}")
                return

            solutions = progress.get("solutions", {})
            if not isinstance(solutions, dict):
                if isinstance(solutions, list):
                    new_solutions = {}
                    for i, sol in enumerate(solutions):
                        if sol is not None:
                            new_solutions[f"ex{i}"] = sol
                    solutions = new_solutions
                else:
                    solutions = {}

            key = f"ex{exercise_num}"

            solutions[key] = {
                "code": compressed_b64,
                "saved_at": datetime.now().isoformat(),
                "size": len(code),
            }

            self._patch(f"progress/{user_id}", {
                "solutions": solutions,
                "last_activity": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"Erro ao salvar solução: {e}")
            import traceback
            traceback.print_exc()

    def get_exercise_solution(self, user_id: str, exercise_num: int) -> str | None:
        try:
            progress = self._get(f"progress/{user_id}")

            if progress is None:
                return None

            if not isinstance(progress, dict):
                print(f"Aviso: progress retornou tipo inesperado: {type(progress)}")
                return None

            solutions = progress.get("solutions", {})

            if isinstance(solutions, list):
                new_solutions = {}
                for i, sol in enumerate(solutions):
                    if sol is not None:
                        new_solutions[f"ex{i}"] = sol
                solutions = new_solutions

            key = f"ex{exercise_num}"

            if key not in solutions:
                return None

            import base64
            compressed_b64 = solutions[key]["code"]
            compressed = base64.b64decode(compressed_b64.encode("ascii"))
            code = gzip.decompress(compressed).decode("utf-8")

            return code
        except Exception as e:
            print(f"Erro ao recuperar solução: {e}")
            return None

    def get_exercise(self, exercise_id: str) -> dict[str, Any] | None:
        try:
            exercise = self._get(f"exercises/{exercise_id}")
            return exercise
        except Exception as e:
            print(f"Erro ao buscar exercício: {e}")
            return None

    def get_all_exercises(self) -> list[dict[str, Any]]:
        try:
            exercises = self._get("exercises")

            if exercises is None:
                return []

            exercise_list = []
            for ex_id, ex_data in exercises.items():
                ex_data['id'] = ex_id
                exercise_list.append(ex_data)

            exercise_list.sort(key=lambda x: x.get('order', 0))
            return exercise_list
        except Exception as e:
            print(f"Erro ao buscar exercícios: {e}")
            return []

    def get_api_key(self) -> str | None:
        try:
            credentials = self._get("system_config/api_credentials")

            if credentials is None:
                return None

            return credentials.get("api_key")
        except Exception as e:
            print(f"Erro ao buscar API key: {e}")
            return None

    def set_api_key(self, api_key: str, provider: str):
        try:
            data = {
                "api_key": api_key,
                "provider": provider,
                "updated_at": datetime.now().isoformat(),
            }
            self._put("system_config/api_credentials", data)
        except Exception as e:
            print(f"Erro ao salvar API key: {e}")

    def increment_api_usage(self, user_id: str, exercise_num: int):
        try:
            usage_data = self._get(f"api_usage/{user_id}")
            data: dict[str, Any] | None = None

            if usage_data is not None:
                if isinstance(usage_data, dict):
                    data = usage_data

            if data is None:
                data = {
                    "total_calls": 0,
                    "calls_today": 0,
                    "last_reset": datetime.now().isoformat(),
                    "calls_by_exercise": {},
                    "estimated_cost": 0.0,
                }

            last_reset = datetime.fromisoformat(data["last_reset"])
            now = datetime.now()
            if now.date() > last_reset.date():
                data["calls_today"] = 0
                data["last_reset"] = now.isoformat()

            data["total_calls"] += 1
            data["calls_today"] += 1

            key = str(exercise_num)
            calls_by_ex = data.get("calls_by_exercise", {})
            if not isinstance(calls_by_ex, dict):
                calls_by_ex = {}
            calls_by_ex[key] = calls_by_ex.get(key, 0) + 1
            data["calls_by_exercise"] = calls_by_ex

            self._put(f"api_usage/{user_id}", data)
        except Exception as e:
            print(f"Erro ao incrementar uso de API: {e}")

    def get_api_usage(self, user_id: str) -> dict[str, Any] | None:
        try:
            usage = self._get(f"api_usage/{user_id}")

            if usage is None:
                return {
                    "total_calls": 0,
                    "calls_today": 0,
                    "calls_by_exercise": {},
                }

            if not isinstance(usage, dict):
                print(f"Aviso: api_usage retornou tipo inesperado: {type(usage)}")
                return {
                    "total_calls": 0,
                    "calls_today": 0,
                    "calls_by_exercise": {},
                }

            return usage
        except Exception as e:
            print(f"Erro ao buscar uso de API: {e}")
            return {}

    def check_rate_limit(
        self, user_id: str, daily_limit: int = 100, total_limit: int = 200
    ) -> tuple[bool, int, str]:
        return True, 100, "ok"
