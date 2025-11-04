"""
Testes para Exercício 4: Memory - Gerenciamento via histórico de mensagens
"""

import os
import sys
from pathlib import Path

import pytest

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importa usando helper que detecta nível do usuário
from exercises.tests.test_helper import import_exercise, get_user_level

# Importa o exercício do nível correto
ex04 = import_exercise(1, 'ex04_memory')


class TestMemorySetup:
    """Testes para verificar setup de memory"""

    def test_store_exists(self):
        """Verifica se o store existe"""
        assert hasattr(ex04, 'store')
        assert isinstance(ex04.store, dict)

    def test_get_session_history_exists(self):
        """Verifica se get_session_history existe"""
        assert hasattr(ex04, 'get_session_history')
        assert callable(ex04.get_session_history)

    def test_create_chat_with_history_exists(self):
        """Verifica se create_chat_with_history existe"""
        assert hasattr(ex04, 'create_chat_with_history')
        assert callable(ex04.create_chat_with_history)

    def test_chat_function_exists(self):
        """Verifica se a função chat existe"""
        assert hasattr(ex04, 'chat')
        assert callable(ex04.chat)


class TestChatWithHistory:
    """Testes para o chat com histórico"""

    def test_chat_creation(self):
        """Verifica se o chat é criado"""
        chat = ex04.create_chat_with_history()
        assert chat is not None

    def test_session_history_creation(self):
        """Testa se get_session_history cria histórico corretamente"""
        # Limpa o store
        ex04.store.clear()
        
        # Cria nova sessão
        history = ex04.get_session_history("test_session")
        assert history is not None
        assert "test_session" in ex04.store
        
        # Verifica que retorna o mesmo histórico
        history2 = ex04.get_session_history("test_session")
        assert history is history2

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    @pytest.mark.timeout(30)
    def test_single_session_memory(self):
        """Testa se o chat mantém memória em uma sessão"""
        print("\n" + "="*70)
        print(" TESTE: Memory em uma sessão")
        print("="*70)

        # Limpa o store
        ex04.store.clear()
        
        chat_with_history = ex04.create_chat_with_history()
        session_id = "test_session_1"

        # Primeira mensagem
        print("\n Mensagem 1: Meu nome é João")
        response1 = ex04.chat(chat_with_history, session_id, "Meu nome é João")
        print(f" Resposta: {response1}")

        # Segunda mensagem - deve lembrar do nome
        print("\n Mensagem 2: Qual é meu nome?")
        response2 = ex04.chat(chat_with_history, session_id, "Qual é meu nome?")
        print(f" Resposta: {response2}")
        print("="*70)

        # Verifica se o nome aparece na resposta
        assert "joão" in response2.lower() or "joao" in response2.lower()

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    @pytest.mark.timeout(30)
    def test_multiple_sessions_isolation(self):
        """Testa se sessões diferentes são isoladas"""
        print("\n" + "="*70)
        print(" TESTE: Isolamento entre sessões")
        print("="*70)

        # Limpa o store
        ex04.store.clear()
        
        chat_with_history = ex04.create_chat_with_history()

        # Sessão 1
        print("\n Sessão 1: Meu nome é Alice")
        r1 = ex04.chat(chat_with_history, "session_alice", "Meu nome é Alice")
        print(f" Resposta: {r1}")

        # Sessão 2
        print("\n Sessão 2: Meu nome é Bob")
        r2 = ex04.chat(chat_with_history, "session_bob", "Meu nome é Bob")
        print(f" Resposta: {r2}")

        # Voltar para sessão 1
        print("\n Sessão 1: Qual é meu nome?")
        r3 = ex04.chat(chat_with_history, "session_alice", "Qual é meu nome?")
        print(f" Resposta: {r3}")
        print("="*70)

        # Deve lembrar de Alice, não de Bob
        assert "alice" in r3.lower()
        assert "bob" not in r3.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
