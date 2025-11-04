import os

from utils.firebase_client import FirebaseClient

class APIKeyError(Exception):
    pass


class APIKeyManager:
    firebase: FirebaseClient
    _api_key_cache: str | None

    def __init__(self, firebase_client: FirebaseClient):
        self.firebase = firebase_client
        self._api_key_cache = None

    def get_api_key(self) -> str:
        if self._api_key_cache:
            return self._api_key_cache

        api_key = self.firebase.get_api_key()

        if not api_key:
            raise APIKeyError(
                "API key não encontrada no Firebase.\n\n"
            )

        self._api_key_cache = api_key
        return self._api_key_cache

    def clear_cache(self):
        self._api_key_cache = None

    def set_api_key(self, api_key: str, provider: str = "openai"):
        if not api_key or not api_key.strip():
            raise APIKeyError("API key não pode estar vazia")

        if provider not in ["openai"]:
            raise APIKeyError("Provider deve ser 'openai'")

        self.firebase.set_api_key(api_key.strip(), provider)
        self._api_key_cache = api_key.strip()

        print(f"API key configurada com sucesso (Provider: {provider})")

    def test_api_key(self, provider: str = "openai") -> bool:
        try:
            api_key = self.get_api_key()

            if provider == "openai":
                import openai

                client = openai.OpenAI(api_key=api_key)
                _ = client.models.list()
                return True

            return False

        except Exception as e:
            print(f" Erro ao testar API key: {e}")
            return False

    def get_provider(self) -> str:
        try:
            doc = self.firebase.system_config_ref.document("api_credentials").get()
            if doc.exists:
                return doc.to_dict().get("provider", "openai")
            return "openai"
        except:
            return "openai"


class RateLimiter:
    DEFAULT_DAILY_LIMIT = 100

    def __init__(self, firebase_client, user_id: str):
        self.firebase = firebase_client
        self.user_id = user_id

    def check_limit(
        self, daily_limit: int = None, total_limit: int = None
    ) -> tuple[bool, int, str]:
        if daily_limit is None:
            daily_limit = self.DEFAULT_DAILY_LIMIT
        if total_limit is None:
            total_limit = 200

        can_use, remaining, reason = self.firebase.check_rate_limit(
            self.user_id, daily_limit, total_limit
        )

        if not can_use:
            if reason == "total_limit":
                message = (
                    f" Limite TOTAL de API atingido ({total_limit} chamadas).\n"
                    f"   Você atingiu o máximo de chamadas permitidas durante TODO o workshop.\n"
                    f"   Fale com o instrutor se você precisa de mais chamadas."
                )
            else:  # daily_limit
                message = (
                    f" Limite diário de API atingido ({daily_limit} chamadas).\n"
                    f"   O limite será resetado à meia-noite UTC.\n"
                    f"   Se você precisa de mais chamadas, fale com o instrutor."
                )
            return False, 0, message

        if remaining <= 10:
            message = f"  Atenção: apenas {remaining} chamadas restantes."
        else:
            message = f" Você tem {remaining} chamadas de API disponíveis."

        return True, remaining, message

    def increment_usage(self, exercise_num: int):
        self.firebase.increment_api_usage(self.user_id, exercise_num)

    def get_usage_stats(self) -> dict:
        return self.firebase.get_api_usage(self.user_id)


def setup_environment_for_test(api_key: str) -> dict:
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = api_key
    env["ANTHROPIC_API_KEY"] = api_key
    return env


def cleanup_environment():
    sensitive_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    for var in sensitive_vars:
        if var in os.environ:
            del os.environ[var]
