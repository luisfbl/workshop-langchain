"""
Exercício 4 - Adicionando Memory ao Agente (EASY)
==================================================

OBJETIVO: Fazer o agente lembrar de conversas anteriores.

TEMPO: 12 minutos

O QUE VOCÊ VAI APRENDER:
- Por que agentes precisam de memória
- Como usar o histórico de mensagens built-in do LangChain 1.0+
- Diferença entre agente com/sem memory
- Como manter contexto entre chamadas

CONTEXTO:
Até agora, cada pergunta ao agente é independente. Ele NÃO lembra
do que foi dito antes. Isso torna conversas não-naturais.

Exemplo SEM memory:
  Você: "Analise o calculator.py"
  Agente: "Ok, analisado!"
  Você: "Quantas funções ele tem?"
  Agente: "Quem é 'ele'? Qual arquivo?" ❌

Com memory, o agente vai LEMBRAR!

IMPORTANTE: Na API LangChain 1.0+, o agente mantém memória automaticamente
através do histórico de mensagens. Você só precisa passar o histórico anterior!
"""

# I AM NOT DONE

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Importar tools dos exercícios anteriores
from .ex02_first_tool import list_python_files
from .ex02_multiple_tools import read_file, count_lines

# ============================================================================
# Tool simples para este exercício (já implementada)
# ============================================================================

@tool
def get_file_info(file_path: str) -> str:
    """Retorna informações básicas sobre um arquivo Python.

    Use quando precisar de um resumo rápido do arquivo.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total = len(lines)
        functions = sum(1 for line in lines if line.strip().startswith('def '))
        classes = sum(1 for line in lines if line.strip().startswith('class '))

        return f"""Informações de '{file_path}':
- Total de linhas: {total}
- Funções: {functions}
- Classes: {classes}"""
    except Exception as e:
        return f"Erro: {str(e)}"


# ============================================================================
# TODO 1: Criar agente com tools
# ============================================================================

def create_agent_with_tools():
    """Cria agente com tools usando LangChain 1.0+ API.

    Na API 1.0+, o agente automaticamente mantém memória através do histórico
    de mensagens. Não precisa configurar memory separadamente!
    """

    # TODO 1.1: Criar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-5-nano", temperature=0)

    # TODO 1.2: Criar lista de tools
    tools = []  # TODO: [list_python_files, read_file, count_lines, get_file_info]

    # TODO 1.3: Criar agente
    # O agente já suporta memória automaticamente!
    agent = None  # TODO: create_agent(llm, tools)

    return agent


# ============================================================================
# Função auxiliar para demonstrar memória
# ============================================================================

def chat_with_memory(agent, messages_history):
    """
    Envia uma mensagem ao agente mantendo o histórico.

    Args:
        agent: O agente criado
        messages_history: Lista de mensagens anteriores

    Returns:
        Histórico atualizado com a nova resposta
    """
    # Invoca o agente com o histórico completo
    result = agent.invoke({"messages": messages_history})

    # Retorna as mensagens atualizadas (incluindo a nova resposta)
    return result["messages"]


# ============================================================================
# Testes de Comparação (NÃO MODIFIQUE)
# ============================================================================

def test_without_memory():
    """Demonstra limitações SEM memory (chamadas independentes)."""
    print("TESTE 1: CHAMADAS INDEPENDENTES (SEM HISTÓRICO)")
    print("=" * 70)

    agent = create_agent_with_tools()

    print("\nConversa 1: Analisar arquivo")
    print("-" * 70)
    # Cada invoke é independente - sem histórico
    r1 = agent.invoke({
        "messages": [{"role": "user", "content": "Analise o arquivo ./sample_project/calculator.py"}]
    })
    print(f"Resposta: {r1['messages'][-1].content}\n")

    print("Conversa 2: Pergunta sobre conversa anterior (SEM histórico)")
    print("-" * 70)
    # Nova chamada SEM passar o histórico anterior
    r2 = agent.invoke({
        "messages": [{"role": "user", "content": "Quantas funções ele tem?"}]
    })
    print(f"Resposta: {r2['messages'][-1].content}")
    print("⚠️ Agente NÃO sabe sobre qual arquivo você está falando!\n")
    print("=" * 70)


def test_with_memory():
    """Demonstra vantagens COM memory (mantendo histórico)."""
    print("\n\n🟢 TESTE 2: MANTENDO HISTÓRICO (COM MEMÓRIA)")
    print("=" * 70)

    agent = create_agent_with_tools()

    # Inicia o histórico de mensagens
    messages = []

    print("\nConversa 1: Analisar arquivo")
    print("-" * 70)
    # Adiciona primeira pergunta
    messages.append({"role": "user", "content": "Analise o arquivo ./sample_project/calculator.py"})

    # Invoca e atualiza histórico
    messages = chat_with_memory(agent, messages)
    print(f"Resposta: {messages[-1].content}\n")

    print("Conversa 2: Pergunta sobre conversa anterior (COM histórico)")
    print("-" * 70)
    # Adiciona segunda pergunta ao histórico existente
    messages.append({"role": "user", "content": "Quantas funções ele tem?"})

    # Invoca com histórico completo
    messages = chat_with_memory(agent, messages)
    print(f"Resposta: {messages[-1].content}\n")

    print("Conversa 3: Outra pergunta contextual")
    print("-" * 70)
    messages.append({"role": "user", "content": "E classes, tinha alguma?"})

    messages = chat_with_memory(agent, messages)
    print(f"Resposta: {messages[-1].content}\n")
    print("=" * 70)


def test_memory():
    try:
        test_without_memory()
        test_with_memory()

        print("\n📝 RESUMO:")
        print("=" * 70)
        print("SEM MEMÓRIA: Cada invoke() é independente")
        print("COM MEMÓRIA: Passe o histórico de messages em cada invoke()")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_memory()
