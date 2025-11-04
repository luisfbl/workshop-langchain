"""
Exercício 3 - Memory com RunnableWithMessageHistory (EASY)
===========================================================

OBJETIVO: Aprender a usar RunnableWithMessageHistory para gerenciar
         conversas persistentes automaticamente.

TEMPO: 15 minutos

O QUE VOCÊ VAI APRENDER:
- O que é RunnableWithMessageHistory
- Como criar um chat store para guardar mensagens
- Diferença entre sessões de conversa
- Como usar session_id para múltiplas conversas

CONTEXTO:
Até agora, passamos o histórico manualmente. Mas o LangChain tem uma
forma mais elegante: RunnableWithMessageHistory.

Ele gerencia automaticamente:
- Salvar mensagens de cada conversa
- Recuperar histórico por session_id
- Manter múltiplas conversas separadas
"""

# I AM NOT DONE

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# ============================================================================
# TODO 1: Criar o store para guardar históricos
# ============================================================================

# Dictionary que armazena histórico de cada sessão
# Chave: session_id (string)
# Valor: InMemoryChatMessageHistory (objeto que guarda mensagens)
store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retorna ou cria histórico para uma sessão.

    Esta função é chamada automaticamente pelo RunnableWithMessageHistory
    sempre que precisa acessar o histórico de uma conversa.

    Args:
        session_id: ID único da sessão/conversa

    Returns:
        InMemoryChatMessageHistory com as mensagens da sessão
    """
    # TODO 1.1: Verificar se session_id já existe no store
    # Se não existir, criar novo InMemoryChatMessageHistory()
    # Retornar o histórico

    if session_id not in store:
        store[session_id] = None  # TODO: InMemoryChatMessageHistory()

    return store[session_id]


# ============================================================================
# TODO 2: Criar chat com histórico automático
# ============================================================================

def create_chat_with_history():
    """Cria um chat que gerencia histórico automaticamente.

    Returns:
        RunnableWithMessageHistory configurado
    """
    # TODO 2.1: Criar o LLM base
    llm = None  # TODO: ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # TODO 2.2: Envolver o LLM com RunnableWithMessageHistory
    # DICA: RunnableWithMessageHistory(
    #    runnable=llm,
    #    get_session_history=get_session_history,
    #)
    chat_with_history = None

    return chat_with_history


# ============================================================================
# TODO 3: Usar o chat em diferentes sessões
# ============================================================================

def chat(chat_with_history, session_id: str, message: str) -> str:
    """Envia mensagem para o chat com histórico.

    Args:
        chat_with_history: Chat configurado com RunnableWithMessageHistory
        session_id: ID da sessão (cada conversa tem seu próprio ID)
        message: Mensagem do usuário

    Returns:
        Resposta do assistente
    """
    # TODO 3.1: Invocar o chat passando:
    # - input: a mensagem do usuário
    # - config: {"configurable": {"session_id": session_id}}

    response = None  # TODO: Implementar invoke

    # DICA: result = chat_with_history.invoke(
    #     [HumanMessage(content=message)],
    #     config={"configurable": {"session_id": session_id}}
    # )

    return response.content if response else ""


def show_session_history(session_id: str):
    """Mostra o histórico completo de uma sessão.

    Args:
        session_id: ID da sessão para visualizar
    """
    if session_id not in store:
        print(f"  Sessão '{session_id}' não existe ainda")
        return

    history = store[session_id]
    messages = history.messages

    print(f"\n   Histórico da sessão '{session_id}' ({len(messages)} mensagens):")
    print("  " + "-" * 60)

    for msg in messages:
        role = " Usuário" if msg.type == "human" else " Assistente"
        content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
        print(f"  {role}: {content}")


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_single_session():
    print("\n" + "=" * 70)
    print(" TESTE 1: CONVERSA EM UMA ÚNICA SESSÃO")
    print("=" * 70)

    chat_with_history = create_chat_with_history()
    session_id = "user_123"

    print(f"\n Sessão: {session_id}")
    print("-" * 70)

    # Primeira mensagem
    print("\n Usuário: Meu nome é João e eu gosto de Python")
    response1 = chat(chat_with_history, session_id, "Meu nome é João e eu gosto de Python")
    print(f" Assistente: {response1}\n")

    # Segunda mensagem - deve lembrar do nome
    print(" Usuário: Qual é meu nome?")
    response2 = chat(chat_with_history, session_id, "Qual é meu nome?")
    print(f" Assistente: {response2}\n")

    # Terceira mensagem - deve lembrar da linguagem
    print(" Usuário: Qual linguagem eu gosto?")
    response3 = chat(chat_with_history, session_id, "Qual linguagem eu gosto?")
    print(f" Assistente: {response3}\n")

    # Mostrar histórico
    show_session_history(session_id)
    print("=" * 70)


def test_multiple_sessions():
    """Testa múltiplas sessões independentes."""
    print("\n\n" + "=" * 70)
    print(" TESTE 2: MÚLTIPLAS SESSÕES INDEPENDENTES")
    print("=" * 70)

    chat_with_history = create_chat_with_history()

    # Sessão 1
    print("\n Sessão: user_alice")
    print("-" * 70)
    print(" Alice: Meu nome é Alice e eu moro em São Paulo")
    r1 = chat(chat_with_history, "user_alice", "Meu nome é Alice e eu moro em São Paulo")
    print(f" Assistente: {r1}\n")

    # Sessão 2
    print("\n Sessão: user_bob")
    print("-" * 70)
    print(" Bob: Meu nome é Bob e eu moro no Rio")
    r2 = chat(chat_with_history, "user_bob", "Meu nome é Bob e eu moro no Rio")
    print(f" Assistente: {r2}\n")

    # Voltar para sessão 1 - deve lembrar de Alice
    print("\n Sessão: user_alice (voltando)")
    print("-" * 70)
    print(" Alice: Onde eu moro?")
    r3 = chat(chat_with_history, "user_alice", "Onde eu moro?")
    print(f" Assistente: {r3}\n")

    print("\n Sessão: user_bob (voltando)")
    print("-" * 70)
    print(" Bob: Qual é meu nome?")
    r4 = chat(chat_with_history, "user_bob", "Qual é meu nome?")
    print(f" Assistente: {r4}\n")

    show_session_history("user_alice")
    show_session_history("user_bob")
    print("=" * 70)


def test_memory():
    try:
        test_single_session()
        test_multiple_sessions()
    except Exception as e:
        print(f"\n Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_memory()
