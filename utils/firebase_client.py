import gzip
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pyrebase


class FirebaseClient:
    config_path: Path
    db: Any
    firebase: Any
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

        self.firebase = pyrebase.initialize_app(firebase_config)
        self.db = self.firebase.database()

    def create_user(self, username: str, password_hash: str) -> str | None:
        try:
            user_id = f"{username}_{int(time.time())}"

            user_data = {
                "username": username,
                "password_hash": password_hash,
                "created_at": datetime.now().isoformat(),
                "level": None,
                "last_activity": datetime.now().isoformat(),
            }

            self.db.child("users").child(user_id).set(user_data)
            self._initialize_progress(user_id)

            return user_id
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        try:
            users = self.db.child("users").get()

            if users.val() is None:
                return None

            for user_id, user_data in users.val().items():
                if user_data.get("username") == username:
                    user_data["user_id"] = user_id
                    return user_data

            return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def get_user(self, user_id: str) -> dict[str, Any] | None:
        try:
            user = self.db.child("users").child(user_id).get()

            if user.val() is None:
                return None

            data = user.val()
            data["user_id"] = user_id
            return data
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def update_user_level(self, user_id: str, level: str):
        try:
            self.db.child("users").child(user_id).update({"level": level})
        except Exception as e:
            print(f"Erro ao atualizar nível: {e}")

    def update_last_activity(self, user_id: str):
        try:
            self.db.child("users").child(user_id).update(
                {"last_activity": datetime.now().isoformat()}
            )
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
        self.db.child("progress").child(user_id).set(progress_data)

    def get_progress(self, user_id: str) -> dict[str, Any] | None:
        try:
            progress = self.db.child("progress").child(user_id).get()

            if progress.val() is None:
                self._initialize_progress(user_id)
                return self.get_progress(user_id)

            return progress.val()
        except Exception as e:
            print(f"Erro ao buscar progresso: {e}")
            return None

    def update_progress(self, user_id: str, updates: dict[str, Any]):
        try:
            updates["last_activity"] = datetime.now().isoformat()
            self.db.child("progress").child(user_id).update(updates)
        except Exception as e:
            print(f"Erro ao atualizar progresso: {e}")

    def mark_exercise_complete(self, user_id: str, exercise_num: int):
        try:
            progress = self.db.child("progress").child(user_id).get()

            if progress.val() is not None:
                data = progress.val()
                # Garante que data é um dict, não uma lista
                if not isinstance(data, dict):
                    print(f"Aviso: progress.val() retornou tipo inesperado: {type(data)}")
                    return
                completed = data.get("completed_exercises", [])

                if exercise_num not in completed:
                    completed.append(exercise_num)
                    completed.sort()

                    self.db.child("progress").child(user_id).update(
                        {
                            "completed_exercises": completed,
                            "current_exercise": exercise_num + 1,
                            "last_activity": datetime.now().isoformat(),
                        }
                    )
        except Exception as e:
            print(f"Erro ao marcar exercício completo: {e}")

    def add_hint_used(self, user_id: str, exercise_num: int, hint_level: int):
        try:
            progress = self.db.child("progress").child(user_id).get()

            if progress.val() is not None:
                data = progress.val()
                # Garante que data é um dict, não uma lista
                if not isinstance(data, dict):
                    print(f"Aviso: progress.val() retornou tipo inesperado: {type(data)}")
                    return
                hints = data.get("hints_used", {})
                key = str(exercise_num)

                if key not in hints:
                    hints[key] = []

                if hint_level not in hints[key]:
                    hints[key].append(hint_level)
                    hints[key].sort()

                self.db.child("progress").child(user_id).update(
                    {
                        "hints_used": hints,
                        "last_activity": datetime.now().isoformat(),
                    }
                )
        except Exception as e:
            print(f"Erro ao registrar dica: {e}")

    def increment_attempt(self, user_id: str, exercise_num: int):
        """Incrementa contador de tentativas de um exercício"""
        try:
            progress = self.db.child("progress").child(user_id).get()

            data = {}
            if progress.val() is not None:
                val = progress.val()
                # Garante que data é um dict, não uma lista
                if isinstance(val, dict):
                    data = val
                # Silenciosamente converte tipos incorretos para dict vazio

            attempts = data.get("exercise_attempts", {})
            # Garantir que attempts é um dict, não uma lista
            if not isinstance(attempts, dict):
                attempts = {}

            key = str(exercise_num)

            attempts[key] = attempts.get(key, 0) + 1

            self.db.child("progress").child(user_id).update(
                {
                    "exercise_attempts": attempts,
                    "last_activity": datetime.now().isoformat(),
                }
            )
        except Exception as e:
            print(f"Erro ao incrementar tentativa: {e}")

    def save_test_result(self, user_id: str, exercise_num: int, passed: bool):
        try:
            progress = self.db.child("progress").child(user_id).get()

            data = {}
            if progress.val() is not None:
                val = progress.val()
                # Garante que data é um dict, não uma lista
                if isinstance(val, dict):
                    data = val
                # Silenciosamente converte tipos incorretos para dict vazio

            results = data.get("test_results", {})
            # Garantir que results é um dict, não uma lista
            if not isinstance(results, dict):
                results = {}

            key = str(exercise_num)

            if key not in results:
                results[key] = {"passed": False, "attempts": 0}

            results[key]["passed"] = passed
            results[key]["attempts"] = results[key].get("attempts", 0) + 1
            results[key]["last_attempt"] = datetime.now().isoformat()

            self.db.child("progress").child(user_id).update(
                {
                    "test_results": results,
                    "last_activity": datetime.now().isoformat(),
                }
            )
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")

    def save_exercise_solution(self, user_id: str, exercise_num: int, code: str):
        try:
            compressed = gzip.compress(code.encode("utf-8"))

            import base64
            compressed_b64 = base64.b64encode(compressed).decode("ascii")

            progress = self.db.child("progress").child(user_id).get()

            if progress.val() is not None:
                data = progress.val()
                # Garante que data é um dict, não uma lista
                if not isinstance(data, dict):
                    print(f"Aviso: progress.val() retornou tipo inesperado: {type(data)}")
                    return
                solutions = data.get("solutions", {})
                key = str(exercise_num)

                solutions[key] = {
                    "code": compressed_b64,
                    "saved_at": datetime.now().isoformat(),
                    "size": len(code),
                }

                self.db.child("progress").child(user_id).update(
                    {
                        "solutions": solutions,
                        "last_activity": datetime.now().isoformat(),
                    }
                )
        except Exception as e:
            print(f"Erro ao salvar solução: {e}")

    def get_exercise_solution(self, user_id: str, exercise_num: int) -> str | None:
        try:
            progress = self.db.child("progress").child(user_id).get()

            if progress.val() is None:
                return None

            data = progress.val()
            # Garante que data é um dict, não uma lista
            if not isinstance(data, dict):
                print(f"Aviso: progress.val() retornou tipo inesperado: {type(data)}")
                return None
            solutions = data.get("solutions", {})
            key = str(exercise_num)

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
            exercise = self.db.child("exercises").child(exercise_id).get()

            if exercise.val() is None:
                return None

            return exercise.val()
        except Exception as e:
            print(f"Erro ao buscar exercício: {e}")
            return None

    def get_all_exercises(self) -> list[dict[str, Any]]:
        try:
            exercises = self.db.child("exercises").get()

            if exercises.val() is None:
                return []

            # Converte para lista e ordena por 'order'
            exercise_list = []
            for ex_id, ex_data in exercises.val().items():
                ex_data['id'] = ex_id
                exercise_list.append(ex_data)

            # Ordena por 'order' se existir
            exercise_list.sort(key=lambda x: x.get('order', 0))
            return exercise_list
        except Exception as e:
            print(f"Erro ao buscar exercícios: {e}")
            return []

    def get_api_key(self) -> str | None:
        try:
            credentials = self.db.child("system_config").child("api_credentials").get()

            if credentials.val() is None:
                return None

            data = credentials.val()
            return data.get("api_key")
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
            self.db.child("system_config").child("api_credentials").set(data)
        except Exception as e:
            print(f"Erro ao salvar API key: {e}")

    def increment_api_usage(self, user_id: str, exercise_num: int):
        try:
            usage_data = self.db.child("api_usage").child(user_id).get()
            data: dict[str, Any] | None = None

            if usage_data.val() is not None:
                data = usage_data.val()
                # Garante que data é um dict, não uma lista
                if not isinstance(data, dict):
                    print(f"Aviso: api_usage.val() retornou tipo inesperado: {type(data)}")
                    data = None

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
            # Proteção extra para garantir que data é dict
            if not isinstance(data, dict):
                print(f"Erro: data não é dict em increment_api_usage: {type(data)}")
                return
            calls_by_ex = data.get("calls_by_exercise", {})
            if not isinstance(calls_by_ex, dict):
                calls_by_ex = {}
            calls_by_ex[key] = calls_by_ex.get(key, 0) + 1
            data["calls_by_exercise"] = calls_by_ex

            self.db.child("api_usage").child(user_id).set(data)
        except Exception as e:
            print(f"Erro ao incrementar uso de API: {e}")

    def get_api_usage(self, user_id: str) -> dict[str, Any] | None:
        try:
            usage = self.db.child("api_usage").child(user_id).get()

            if usage.val() is None:
                return {
                    "total_calls": 0,
                    "calls_today": 0,
                    "calls_by_exercise": {},
                }

            data = usage.val()
            # Garante que data é um dict, não uma lista
            if not isinstance(data, dict):
                print(f"Aviso: api_usage.val() retornou tipo inesperado: {type(data)}")
                return {
                    "total_calls": 0,
                    "calls_today": 0,
                    "calls_by_exercise": {},
                }

            return data
        except Exception as e:
            print(f"Erro ao buscar uso de API: {e}")
            return {}

    def check_rate_limit(
        self, user_id: str, daily_limit: int = 100, total_limit: int = 200
    ) -> tuple[bool, int, str]:
        usage = self.get_api_usage(user_id)

        if not usage:
            return False, 0, "user_not_found"

        calls_today: int = usage.get("calls_today", 0)
        total_calls: int = usage.get("total_calls", 0)

        if total_calls >= total_limit:
            return False, 0, "total_limit"

        if calls_today >= daily_limit:
            return False, 0, "daily_limit"

        remaining_daily: int = daily_limit - calls_today
        remaining_total: int = total_limit - total_calls
        remaining = min(remaining_daily, remaining_total)

        return True, remaining, "ok"
