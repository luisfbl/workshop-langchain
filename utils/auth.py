import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import bcrypt
from cryptography.fernet import Fernet
from google.cloud.client import Client

from utils.firebase_client import FirebaseClient

SESSION_TIMEOUT_HOURS = 3
SESSION_FILE = Path.home() / ".langchain_workshop" / "session.enc"

class AuthenticationError(Exception):
    pass


class SessionManager:
    session_dir: Path

    def __init__(self):
        self.session_dir = SESSION_FILE.parent
        self.session_dir.mkdir(exist_ok=True, parents=True)
        self._ensure_session_key()

    def _ensure_session_key(self):
        key_file = self.session_dir / ".session_key"
        if not key_file.exists():
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            os.chmod(key_file, 0o600)
        self.cipher = Fernet(key_file.read_bytes())

    def create_session(self, user_id: str, username: str) -> dict[str, Any]:
        session_data = {
            "user_id": user_id,
            "username": username,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
        }

        encrypted = self.cipher.encrypt(json.dumps(session_data).encode())
        _ = SESSION_FILE.write_bytes(encrypted)
        os.chmod(SESSION_FILE, 0o600)

        return session_data

    def get_session(self) -> dict[str, Any] | None:
        if not SESSION_FILE.exists():
            return None

        try:
            encrypted = SESSION_FILE.read_bytes()
            decrypted = self.cipher.decrypt(encrypted)
            session_data = json.loads(decrypted.decode())

            last_activity = datetime.fromisoformat(session_data["last_activity"])
            if datetime.now() - last_activity > timedelta(hours=SESSION_TIMEOUT_HOURS):
                self.clear_session()
                return None

            session_data["last_activity"] = datetime.now().isoformat()
            self.create_session(session_data["user_id"], session_data["username"])

            return session_data
        except Exception:
            self.clear_session()
            return None

    def clear_session(self):
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()


class Authenticator:
    firebase: FirebaseClient
    session_manager: SessionManager

    def __init__(self, firebase_client: FirebaseClient):
        self.firebase = firebase_client
        self.session_manager = SessionManager()

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), password_hash.encode())

    def register(self, username: str, password: str) -> tuple[bool, str]:
        if len(username) < 3:
            return (False, "Nome de usuário deve ter pelo menos 3 caracteres")

        if not username.isalnum():
            return (False, "Nome de usuário deve conter apenas letras e números")
        if len(password) < 6:
            return (False, "Senha deve ter pelo menos 6 caracteres")

        existing = self.firebase.get_user_by_username(username)
        if existing:
            return False, "Nome de usuário já existe"

        password_hash = self.hash_password(password)
        user_id = self.firebase.create_user(username, password_hash)

        if user_id:
            return True, f"${user_id}"
        else:
            return False, "Erro ao criar usuário no banco de dados"

    def login(self, username: str, password: str) -> tuple[bool, str, dict[str, Any] | None]:
        user = self.firebase.get_user_by_username(username)
        if not user:
            return False, "Usuário ou senha incorretos.", None

        if not self.verify_password(password, user["password_hash"]):
            return False, "Usuário ou senha incorretos.", None

        session = self.session_manager.create_session(user["user_id"], username)
        self.firebase.update_last_activity(user["user_id"])

        return True, "Login realizado com sucesso!", session

    def logout(self):
        self.session_manager.clear_session()

    def get_current_session(self) -> Optional[dict]:
        return self.session_manager.get_session()

    def require_auth(self) -> dict:
        session = self.get_current_session()
        if not session:
            raise AuthenticationError("Você precisa fazer login primeiro. Execute 'python main.py'")
        return session
