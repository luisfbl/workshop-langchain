import gzip
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.client import Client
from google.cloud.firestore import SERVER_TIMESTAMP, CollectionReference


class FirebaseClient:
    config_path: Path
    db: Client

    users_ref: CollectionReference
    progress_ref: CollectionReference
    exercises_ref: CollectionReference
    api_usage_ref: CollectionReference
    system_config_ref: CollectionReference

    def __init__(self, config: str | None = None):
        if firebase_admin is None:
            raise ImportError("Firebase Admin SDK não instalado")

        config_path = None
        if config is None:
            config_path = (
                Path(__file__).parent.parent / "config" / "firebase_config.json"
            )

        if config_path is None or not config_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração do Firebase não encontrado: {self.config_path}\n"
            )

        self.config_path = Path(config_path)

        if not firebase_admin._apps:
            cred = credentials.Certificate(str(self.config_path))
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

        self.users_ref = self.db.collection("users")
        self.progress_ref = self.db.collection("progress")
        self.exercises_ref = self.db.collection("exercises")
        self.api_usage_ref = self.db.collection("api_usage")
        self.system_config_ref = self.db.collection("system_config")

    def create_user(self, username: str, password_hash: str) -> str | None:
        try:
            user_id = f"{username}_{int(time.time())}"

            user_data = {
                "username": username,
                "password_hash": password_hash,
                "created_at": SERVER_TIMESTAMP,
                "level": None,
                "last_activity": SERVER_TIMESTAMP,
            }

            _ = self.users_ref.document(user_id).set(user_data)
            self._initialize_progress(user_id)

            return user_id
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        try:
            query = self.users_ref.where("username", "==", username).limit(1)
            results = list(query.stream())

            if results:
                doc = results[0]
                data = doc.to_dict()

                if data is None:
                    return None

                data["user_id"] = doc.id
                return data
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def get_user(self, user_id: str) -> dict[str, Any] | None:
        try:
            doc = self.users_ref.document(user_id).get()
            if doc.exists:
                data = doc.to_dict()

                if data is None:
                    return None

                data["user_id"] = doc.id
                return data
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def update_user_level(self, user_id: str, level: str):
        try:
            self.users_ref.document(user_id).update({"level": level})
        except Exception as e:
            print(f"Erro ao atualizar nível: {e}")

    def update_last_activity(self, user_id: str):
        try:
            self.users_ref.document(user_id).update(
                {"last_activity": SERVER_TIMESTAMP}
            )
        except Exception as e:
            print(f"Erro ao atualizar atividade: {e}")

    def _initialize_progress(self, user_id: str):
        progress_data: dict[str, Any] = {
            "current_exercise": 1,
            "completed_exercises": [],
            "exercise_attempts": {},
            "hints_used": {},
            "start_time": SERVER_TIMESTAMP,
            "last_activity": SERVER_TIMESTAMP,
            "test_results": {},
        }
        self.progress_ref.document(user_id).set(progress_data)

    def get_progress(self, user_id: str) -> dict[str, Any] | None:
        try:
            doc = self.progress_ref.document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            else:
                self._initialize_progress(user_id)
                return self.get_progress(user_id)
        except Exception as e:
            print(f"Erro ao buscar progresso: {e}")
            return None

    def update_progress(self, user_id: str, updates: dict[str, Any]):
        try:
            updates["last_activity"] = SERVER_TIMESTAMP
            self.progress_ref.document(user_id).update(updates)
        except Exception as e:
            print(f"Erro ao atualizar progresso: {e}")

    def mark_exercise_complete(self, user_id: str, exercise_num: int):
        try:
            doc_ref = self.progress_ref.document(user_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                completed = data.get("completed_exercises", [])

                if exercise_num not in completed:
                    completed.append(exercise_num)
                    completed.sort()

                    _ = doc_ref.update(
                        {
                            "completed_exercises": completed,
                            "current_exercise": exercise_num + 1,
                            "last_activity": SERVER_TIMESTAMP,
                        }
                    )
        except Exception as e:
            print(f"Erro ao marcar exercício completo: {e}")

    def add_hint_used(self, user_id: str, exercise_num: int, hint_level: int):
        try:
            doc_ref = self.progress_ref.document(user_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                hints = data.get("hints_used", {})
                key = str(exercise_num)

                if key not in hints:
                    hints[key] = []

                if hint_level not in hints[key]:
                    hints[key].append(hint_level)
                    hints[key].sort()

                _ = doc_ref.update(
                    {
                        "hints_used": hints,
                        "last_activity": SERVER_TIMESTAMP,
                    }
                )
        except Exception as e:
            print(f"Erro ao registrar dica: {e}")

    def save_test_result(self, user_id: str, exercise_num: int, passed: bool):
        try:
            doc_ref = self.progress_ref.document(user_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                results = data.get("test_results", {})
                key = str(exercise_num)

                if key not in results:
                    results[key] = {"passed": False, "attempts": 0}

                results[key]["passed"] = passed
                results[key]["attempts"] = results[key].get("attempts", 0) + 1
                results[key]["last_attempt"] = datetime.now().isoformat()

                _ = doc_ref.update(
                    {
                        "test_results": results,
                        "last_activity": SERVER_TIMESTAMP,
                    }
                )
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")

    def save_exercise_solution(self, user_id: str, exercise_num: int, code: str):
        try:
            compressed = gzip.compress(code.encode("utf-8"))

            import base64
            compressed_b64 = base64.b64encode(compressed).decode("ascii")

            doc_ref = self.progress_ref.document(user_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                solutions = data.get("solutions", {})
                key = str(exercise_num)

                solutions[key] = {
                    "code": compressed_b64,
                    "saved_at": datetime.now().isoformat(),
                    "size": len(code),
                }

                _ = doc_ref.update(
                    {
                        "solutions": solutions,
                        "last_activity": SERVER_TIMESTAMP,
                    }
                )
        except Exception as e:
            print(f"Erro ao salvar solução: {e}")

    def get_exercise_solution(self, user_id: str, exercise_num: int) -> str | None:
        try:
            doc = self.progress_ref.document(user_id).get()

            if not doc.exists:
                return None

            data = doc.to_dict()
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
            doc = self.exercises_ref.document(exercise_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Erro ao buscar exercício: {e}")
            return None

    def get_all_exercises(self) -> list[dict[str, Any]]:
        try:
            docs = self.exercises_ref.order_by("order").stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Erro ao buscar exercícios: {e}")
            return []

    def get_api_key(self) -> str | None:
        try:
            doc = self.system_config_ref.document("api_credentials").get()
            if doc.exists:
                data = doc.to_dict()
                return data.get("api_key")
            return None
        except Exception as e:
            print(f"Erro ao buscar API key: {e}")
            return None

    def set_api_key(self, api_key: str, provider: str):
        try:
            data = {
                "api_key": api_key,
                "provider": provider,
                "updated_at": SERVER_TIMESTAMP,
            }
            self.system_config_ref.document("api_credentials").set(data)
        except Exception as e:
            print(f"Erro ao salvar API key: {e}")

    def increment_api_usage(self, user_id: str, exercise_num: int):
        try:
            doc_ref = self.api_usage_ref.document(user_id)
            doc = doc_ref.get()
            data: dict[str, Any] | None = None

            if doc.exists:
                data = doc.to_dict()

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
            calls_by_ex[key] = calls_by_ex.get(key, 0) + 1
            data["calls_by_exercise"] = calls_by_ex

            doc_ref.set(data)
        except Exception as e:
            print(f"Erro ao incrementar uso de API: {e}")

    def get_api_usage(self, user_id: str) -> dict[str, Any] | None:
        try:
            doc = self.api_usage_ref.document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            return {
                "total_calls": 0,
                "calls_today": 0,
                "calls_by_exercise": {},
            }
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
