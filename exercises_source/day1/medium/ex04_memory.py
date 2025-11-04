"""
Exercício 3 - Memory Avançado com RunnableWithMessageHistory (MEDIUM)
======================================================================

OBJETIVO: Implementar gerenciamento avançado de memória com múltiplas
         sessões e persistência customizada.

TEMPO: 15 minutos

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
from typing import Any
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, trim_messages, HumanMessage


# ============================================================================
# TODO 1: Criar store simples (dicionário) e função get_session_history
# ============================================================================

# TODO 1.1: Criar dicionário vazio para armazenar sessões
# DICA: store deve ser um dict[str, InMemoryChatMessageHistory]
store = None  # TODO: criar dicionário vazio


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retorna ou cria histórico para uma sessão.
    
    Args:
        session_id: ID da sessão
    
    Returns:
        InMemoryChatMessageHistory da sessão
    """
    # TODO 1.2: Se session_id não existe no store, criar uma nova entrada
    # com InMemoryChatMessageHistory()
    
    # TODO 1.3: Retornar o histórico da sessão
    pass


# ============================================================================
# TODO 2: Criar chat com trimming (limitar histórico)
# ============================================================================

def create_chat_with_history(max_messages: int | None = None):
    # TODO 2.1: Criar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-5-nano", temperature=0)

    # TODO 2.2: Se max_messages definido, adicionar trimming
    runnable = llm
    if max_messages:
        # DICA: Use trim_messages para limitar o histórico
        # trimmer = trim_messages(
        #     max_tokens=max_messages,
        #     strategy="last",
        #     token_counter=len
        # )
        # runnable = trimmer | llm
        pass

    # TODO 2.3: Criar RunnableWithMessageHistory
    chat_with_history = None  # TODO: Implementar

    # DICA: RunnableWithMessageHistory(
    #     runnable=runnable,  # ou apenas llm se não usar trimming
    #     get_session_history=get_session_history,
    # )

    return chat_with_history


# ============================================================================
# TODO 3: Funções de utilidade
# ============================================================================

def chat(chat_with_history, session_id: str, message: str) -> str:
    # TODO 3.1: Invocar chat com session_id
    # DICA: chat_with_history.invoke(
    #     [HumanMessage(content=message)],
    #     config={"configurable": {"session_id": session_id}}
    # )
    response = None  # TODO: Implementar invoke

    return response.content if response else ""


def show_session_stats(session_id: str):
    # TODO 3.2: Obter e mostrar informações da sessão
    # DICA: Verificar se session_id existe no store
    # DICA: Pegar o histórico do store[session_id]
    # DICA: Contar mensagens com len(history.messages)
    
    if session_id not in store:
        print(f"  Sessão '{session_id}' não existe")
        return

    # TODO: Implementar exibição de estatísticas
    print(f"\n   Estatísticas da sessão '{session_id}':")
    print("  " + "-" * 60)
    print(f"  Total de mensagens: ???")  # TODO: mostrar contagem real


def show_all_sessions():
    # TODO: Listar todas as chaves do store
    sessions = list(store.keys())

    print(f"\n   Sessões ativas: {len(sessions)}")
    print("  " + "=" * 60)

    for session_id in sessions:
        # TODO: Para cada sessão, pegar histórico e contar mensagens
        history = store[session_id]
        message_count = len(history.messages)
        print(f"\n  ID: {session_id}")
        print(f"    Mensagens: {message_count}")


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_basic_chat():
    """Testa chat básico com metadados."""
    print("\n" + "=" * 70)
    print(" TESTE 1: CHAT COM METADADOS")
    print("=" * 70)

    chat_with_history = create_chat_with_history()

    # Conversa 1
    print("\n Sessão: user_123")
    print("-" * 70)
    chat(chat_with_history, "user_123", "Meu nome é João")
    chat(chat_with_history, "user_123", "Qual é meu nome?")

    show_session_stats("user_123")

    # Conversa 2
    print("\n\n Sessão: user_456")
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
    print(" TESTE 2: TRIMMING DE MENSAGENS")
    print("=" * 70)

    # Chat com limite de 4 mensagens
    chat_limited = create_chat_with_history(max_messages=4)
    session_id = "test_trim"

    print(f"\n Sessão: {session_id} (máx: 4 mensagens)")
    print("-" * 70)

    messages = [
        "Mensagem 1",
        "Mensagem 2",
        "Mensagem 3",
        "Mensagem 4",
        "Mensagem 5 - as antigas devem ser removidas"
    ]

    for msg in messages:
        print(f"\n Enviando: {msg}")
        chat(chat_limited, session_id, msg)

    show_session_stats(session_id)
    print("\n    Com trimming, apenas as últimas mensagens são mantidas")
    print("=" * 70)


def test_session_management():
    """Testa gerenciamento de sessões."""
    print("\n\n" + "=" * 70)
    print(" TESTE 3: GERENCIAMENTO DE SESSÕES")
    print("=" * 70)

    chat_with_history = create_chat_with_history()

    # Criar várias sessões
    for i in range(3):
        session_id = f"session_{i}"
        chat(chat_with_history, session_id, f"Olá da sessão {i}")

    print("\n  Antes de deletar:")
    show_all_sessions()

    # Deletar uma sessão
    print("\n    Deletando session_1...")
    # TODO: Deletar session_1 do store usando del
    if "session_1" in store:
        del store["session_1"]

    print("\n  Depois de deletar:")
    show_all_sessions()
    print("=" * 70)


def test_memory():
    """Executa todos os testes."""
    try:
        test_basic_chat()
        test_trimming()
        test_session_management()

        print("\n\n RESUMO:")
        print("=" * 70)
        print(" SessionStore adiciona metadados às sessões")
        print(" Trimming limita o tamanho do histórico")
        print(" Gerenciamento completo de múltiplas sessões")
        print("=" * 70)

    except Exception as e:
        print(f"\n Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_memory()
