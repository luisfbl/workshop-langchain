"""
Exercício 3 - Memory Avançado com RunnableWithMessageHistory (MEDIUM)
======================================================================

OBJETIVO: Implementar gerenciamento avançado de memória com múltiplas
         sessões e persistência customizada.

TEMPO: 20 minutos

O QUE VOCÊ VAI APRENDER:
- RunnableWithMessageHistory com configuração avançada
- Criar chat store customizado com metadados
- Gerenciar múltiplas sessões simultaneamente
- Implementar trimming de mensagens antigas
- Estatísticas de uso de memória

CONTEXTO:
No nível EASY vimos o básico de RunnableWithMessageHistory. Agora vamos
explorar recursos avançados como:
- Adicionar metadados às sessões (timestamp, user info)
- Limitar tamanho do histórico (trimming)
- Estatísticas de uso de memória
- Gerenciamento de múltiplas sessões
"""

# I AM NOT DONE

from datetime import datetime
from typing import Dict, List, Optional
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, trim_messages


# ============================================================================
# TODO 1: Criar SessionStore com metadados
# ============================================================================

class SessionStore:
    """Store customizado que adiciona metadados às sessões."""

    def __init__(self):
        # TODO 1.1: Criar dicionários para armazenar dados
        self._sessions: Dict[str, InMemoryChatMessageHistory] = {}
        self._metadata: Dict[str, dict] = {}  # Metadados por sessão

    def get_session(self, session_id: str) -> InMemoryChatMessageHistory:
        """Retorna ou cria sessão com metadados.

        Args:
            session_id: ID da sessão

        Returns:
            InMemoryChatMessageHistory da sessão
        """
        # TODO 1.2: Se sessão não existe, criar nova e adicionar metadados
        if session_id not in self._sessions:
            self._sessions[session_id] = None  # TODO: InMemoryChatMessageHistory()
            self._metadata[session_id] = {
                "created_at": None,  # TODO: datetime.now()
                "message_count": 0,
                "last_accessed": None  # TODO: datetime.now()
            }

        # TODO 1.3: Atualizar last_accessed
        # self._metadata[session_id]["last_accessed"] = datetime.now()

        return self._sessions[session_id]

    def get_session_info(self, session_id: str) -> Optional[dict]:
        """Retorna informações sobre uma sessão.

        Args:
            session_id: ID da sessão

        Returns:
            Dicionário com metadados ou None se não existir
        """
        # TODO 1.4: Retornar metadados + contagem de mensagens
        if session_id not in self._sessions:
            return None

        history = self._sessions[session_id]
        metadata = self._metadata[session_id].copy()
        metadata["message_count"] = None  # TODO: len(history.messages)

        return metadata

    def list_sessions(self) -> List[str]:
        """Lista todos os IDs de sessões."""
        return list(self._sessions.keys())

    def delete_session(self, session_id: str) -> bool:
        """Deleta uma sessão.

        Args:
            session_id: ID da sessão

        Returns:
            True se deletou, False se sessão não existia
        """
        # TODO 1.5: Remover sessão e seus metadados
        if session_id in self._sessions:
            del self._sessions[session_id]
            del self._metadata[session_id]
            return True
        return False


# Instância global do store
store = SessionStore()


# ============================================================================
# TODO 2: Criar chat com trimming (limitar histórico)
# ============================================================================

def create_chat_with_history(max_messages: Optional[int] = None):
    """Cria chat com histórico e opção de limitar mensagens.

    Args:
        max_messages: Número máximo de mensagens no histórico.
                     Se None, mantém todas as mensagens.

    Returns:
        RunnableWithMessageHistory configurado
    """
    # TODO 2.1: Criar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # TODO 2.2: Se max_messages definido, adicionar trimming
    if max_messages:
        # DICA: Use trim_messages para limitar o histórico
        # trimmer = trim_messages(
        #     max_tokens=max_messages,  # ou use strategy="last"
        #     strategy="last",
        #     token_counter=len,
        # )
        # llm_with_trimming = trimmer | llm
        pass

    # TODO 2.3: Criar RunnableWithMessageHistory
    chat_with_history = None  # TODO: Implementar

    # DICA: RunnableWithMessageHistory(
    #     runnable=llm,  # ou llm_with_trimming
    #     get_session_history=lambda session_id: store.get_session(session_id),
    #     input_messages_key="input",
    #     history_messages_key="chat_history",
    # )

    return chat_with_history


# ============================================================================
# TODO 3: Funções de utilidade
# ============================================================================

def chat(chat_with_history, session_id: str, message: str) -> str:
    """Envia mensagem e retorna resposta.

    Args:
        chat_with_history: Chat configurado
        session_id: ID da sessão
        message: Mensagem do usuário

    Returns:
        Resposta do assistente
    """
    # TODO 3.1: Invocar chat com session_id
    response = None  # TODO: Implementar invoke

    return response.content if response else ""


def show_session_stats(session_id: str):
    """Mostra estatísticas de uma sessão.

    Args:
        session_id: ID da sessão
    """
    # TODO 3.2: Obter e mostrar informações da sessão
    info = None  # TODO: store.get_session_info(session_id)

    if not info:
        print(f"  Sessão '{session_id}' não existe")
        return

    print(f"\n  📊 Estatísticas da sessão '{session_id}':")
    print("  " + "-" * 60)
    print(f"  Criada em: {info.get('created_at')}")
    print(f"  Último acesso: {info.get('last_accessed')}")
    print(f"  Total de mensagens: {info.get('message_count')}")


def show_all_sessions():
    """Mostra todas as sessões ativas."""
    sessions = store.list_sessions()

    print(f"\n  📋 Sessões ativas: {len(sessions)}")
    print("  " + "=" * 60)

    for session_id in sessions:
        info = store.get_session_info(session_id)
        print(f"\n  ID: {session_id}")
        print(f"    Mensagens: {info['message_count']}")
        print(f"    Último acesso: {info['last_accessed']}")


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_basic_chat():
    """Testa chat básico com metadados."""
    print("\n" + "=" * 70)
    print("🧪 TESTE 1: CHAT COM METADADOS")
    print("=" * 70)

    chat_with_history = create_chat_with_history()

    # Conversa 1
    print("\n👤 Sessão: user_123")
    print("-" * 70)
    chat(chat_with_history, "user_123", "Meu nome é João")
    chat(chat_with_history, "user_123", "Qual é meu nome?")

    show_session_stats("user_123")

    # Conversa 2
    print("\n\n👤 Sessão: user_456")
    print("-" * 70)
    chat(chat_with_history, "user_456", "Meu nome é Maria")
    chat(chat_with_history, "user_456", "Eu gosto de Python")

    show_session_stats("user_456")

    # Mostrar todas as sessões
    show_all_sessions()
    print("=" * 70)


def test_trimming():
    """Testa limitação de histórico."""
    print("\n\n" + "=" * 70)
    print("🧪 TESTE 2: TRIMMING DE MENSAGENS")
    print("=" * 70)

    # Chat com limite de 4 mensagens
    chat_limited = create_chat_with_history(max_messages=4)
    session_id = "test_trim"

    print(f"\n👤 Sessão: {session_id} (máx: 4 mensagens)")
    print("-" * 70)

    messages = [
        "Mensagem 1",
        "Mensagem 2",
        "Mensagem 3",
        "Mensagem 4",
        "Mensagem 5 - as antigas devem ser removidas"
    ]

    for msg in messages:
        print(f"\n👤 Enviando: {msg}")
        chat(chat_limited, session_id, msg)

    show_session_stats(session_id)
    print("\n  ⚠️  Com trimming, apenas as últimas mensagens são mantidas")
    print("=" * 70)


def test_session_management():
    """Testa gerenciamento de sessões."""
    print("\n\n" + "=" * 70)
    print("🧪 TESTE 3: GERENCIAMENTO DE SESSÕES")
    print("=" * 70)

    chat_with_history = create_chat_with_history()

    # Criar várias sessões
    for i in range(3):
        session_id = f"session_{i}"
        chat(chat_with_history, session_id, f"Olá da sessão {i}")

    print("\n  Antes de deletar:")
    show_all_sessions()

    # Deletar uma sessão
    print("\n  🗑️  Deletando session_1...")
    store.delete_session("session_1")

    print("\n  Depois de deletar:")
    show_all_sessions()
    print("=" * 70)


def test_memory():
    """Executa todos os testes."""
    try:
        test_basic_chat()
        test_trimming()
        test_session_management()

        print("\n\n📝 RESUMO:")
        print("=" * 70)
        print("✅ SessionStore adiciona metadados às sessões")
        print("✅ Trimming limita o tamanho do histórico")
        print("✅ Gerenciamento completo de múltiplas sessões")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_memory()
