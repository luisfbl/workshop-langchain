"""
Testes para Exercício 3: Memory com RunnableWithMessageHistory
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
ex03 = import_exercise(1, 'ex03_memory')


class TestMemorySetup:
    """Testes para verificar setup de memory"""

    def test_store_exists(self):
        """Verifica se o store existe"""
        assert hasattr(ex03, 'store')
        # No easy é dict, no medium é SessionStore
        level = get_user_level()
        if level == 'easy':
            assert isinstance(ex03.store, dict)
        else:
            # Medium: verifica se tem os métodos necessários
            assert hasattr(ex03.store, 'get_session')
            assert hasattr(ex03.store, 'list_sessions')

    def test_get_session_history_exists(self):
        """Verifica se get_session_history existe"""
        # Easy tem função get_session_history, Medium tem no SessionStore
        level = get_user_level()
        if level == 'easy':
            assert hasattr(ex03, 'get_session_history')
            assert callable(ex03.get_session_history)
        else:
            # Medium: verifica métodos do SessionStore
            assert hasattr(ex03.store, 'get_session')
            assert callable(ex03.store.get_session)

    def test_create_chat_with_history_exists(self):
        """Verifica se create_chat_with_history existe"""
        assert hasattr(ex03, 'create_chat_with_history')
        assert callable(ex03.create_chat_with_history)


class TestChatWithHistory:
    """Testes para o chat com histórico"""

    def test_chat_creation(self):
        """Verifica se o chat é criado"""
        chat = ex03.create_chat_with_history()
        assert chat is not None

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_single_session_memory(self):
        """Testa se o chat mantém memória em uma sessão"""
        print("\n" + "="*70)
        print("🧪 TESTE: Memory em uma sessão")
        print("="*70)

        chat_with_history = ex03.create_chat_with_history()
        session_id = "test_session_1"

        # Primeira mensagem
        print("\n👤 Mensagem 1: Meu nome é João")
        response1 = ex03.chat(chat_with_history, session_id, "Meu nome é João")
        print(f"🤖 Resposta: {response1}")

        # Segunda mensagem - deve lembrar do nome
        print("\n👤 Mensagem 2: Qual é meu nome?")
        response2 = ex03.chat(chat_with_history, session_id, "Qual é meu nome?")
        print(f"🤖 Resposta: {response2}")
        print("="*70)

        # Verifica se o nome aparece na resposta
        assert "joão" in response2.lower() or "joao" in response2.lower()

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requer OPENAI_API_KEY")
    def test_multiple_sessions_isolation(self):
        """Testa se sessões diferentes são isoladas"""
        print("\n" + "="*70)
        print("🧪 TESTE: Isolamento entre sessões")
        print("="*70)

        chat_with_history = ex03.create_chat_with_history()

        # Sessão 1
        print("\n👤 Sessão 1: Meu nome é Alice")
        r1 = ex03.chat(chat_with_history, "session_alice", "Meu nome é Alice")
        print(f"🤖 Resposta: {r1}")

        # Sessão 2
        print("\n👤 Sessão 2: Meu nome é Bob")
        r2 = ex03.chat(chat_with_history, "session_bob", "Meu nome é Bob")
        print(f"🤖 Resposta: {r2}")

        # Voltar para sessão 1
        print("\n👤 Sessão 1: Qual é meu nome?")
        r3 = ex03.chat(chat_with_history, "session_alice", "Qual é meu nome?")
        print(f"🤖 Resposta: {r3}")
        print("="*70)

        # Deve lembrar de Alice, não de Bob
        assert "alice" in r3.lower()
        assert "bob" not in r3.lower()


class TestMediumFeatures:
    """Testes específicos para recursos do nível Medium"""

    def test_session_store_methods(self):
        """Testa métodos do SessionStore (apenas Medium)"""
        level = get_user_level()
        if level != 'medium':
            pytest.skip("Teste apenas para nível Medium")

        # Verifica se SessionStore tem todos os métodos necessários
        assert hasattr(ex03.store, 'get_session')
        assert hasattr(ex03.store, 'get_session_info')
        assert hasattr(ex03.store, 'list_sessions')
        assert hasattr(ex03.store, 'delete_session')

    def test_session_metadata(self):
        """Testa se metadados são criados (apenas Medium)"""
        level = get_user_level()
        if level != 'medium':
            pytest.skip("Teste apenas para nível Medium")

        # Limpa sessões existentes
        for sid in ex03.store.list_sessions():
            ex03.store.delete_session(sid)

        # Cria uma sessão
        ex03.store.get_session("test_metadata")

        # Verifica metadados
        info = ex03.store.get_session_info("test_metadata")
        assert info is not None
        assert 'created_at' in info
        assert 'last_accessed' in info
        assert 'message_count' in info

    def test_session_deletion(self):
        """Testa remoção de sessões (apenas Medium)"""
        level = get_user_level()
        if level != 'medium':
            pytest.skip("Teste apenas para nível Medium")

        # Cria e deleta sessão
        ex03.store.get_session("test_delete")
        assert "test_delete" in ex03.store.list_sessions()

        result = ex03.store.delete_session("test_delete")
        assert result is True
        assert "test_delete" not in ex03.store.list_sessions()

        # Tentar deletar novamente deve retornar False
        result = ex03.store.delete_session("test_delete")
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
