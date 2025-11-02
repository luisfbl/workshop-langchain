"""Modelos de dados."""

from dataclasses import dataclass
from typing import List


@dataclass
class User:
    """Representa um usuário do sistema."""
    id: int
    name: str
    email: str
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Database:
    """Banco de dados em memória."""
    
    def __init__(self):
        self.users: List[User] = []
    
    def add_user(self, user: User):
        """Adiciona um usuário."""
        self.users.append(user)
    
    def get_user(self, user_id: int):
        for user in self.users:
            if user.id == user_id:
                return user
        return None
