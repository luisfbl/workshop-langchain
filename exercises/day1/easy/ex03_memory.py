"""
Exercício 4 - Adicionando Memory ao Agente (EASY)
==================================================

OBJETIVO: Fazer o agente lembrar de conversas anteriores.

TEMPO: 12 minutos

O QUE VOCÊ VAI APRENDER:
- Por que agentes precisam de memória
- Como usar ConversationBufferMemory
- Diferença entre agente com/sem memory
- Limitações de contexto

CONTEXTO:
Até agora, cada pergunta ao agente é independente. Ele NÃO lembra
do que foi dito antes. Isso torna conversas não-naturais.

Exemplo SEM memory:
  Você: "Analise o calculator.py"
  Agente: "Ok, analisado!"
  Você: "Quantas funções ele tem?"
  Agente: "Quem é 'ele'? Qual arquivo?" ❌

Com memory, o agente vai LEMBRAR!
"""

# I AM NOT DONE

from langchain.agents import create_react_agent, AgentExecutor, tool
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain import hub

# Importar tools dos exercícios anteriores
from ex02_first_tool import list_python_files
from ex03_multiple_tools import read_file, count_lines

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
# TODO 1: Criar agente SEM memory (para comparação)
# ============================================================================

def create_agent_without_memory():
    """Cria agente SEM memory para demonstração."""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = hub.pull("hwchase17/react")
    tools = [list_python_files, read_file, count_lines, get_file_info]

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
    # Note: SEM memory aqui!

    return agent_executor


# ============================================================================
# TODO 2: Criar agente COM memory
# ============================================================================

def create_agent_with_memory():
    """Cria agente COM memory para manter contexto."""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = hub.pull("hwchase17/react")
    tools = [list_python_files, read_file, count_lines, get_file_info]

    # TODO 2.1: Criar a memory
    # DICA: Use ConversationBufferMemory com:
    #   - memory_key="chat_history"
    #   - return_messages=True

    memory = None  # TODO: ConversationBufferMemory(...)

    agent = create_react_agent(llm, tools, prompt)

    # TODO 2.2: Adicionar memory ao executor
    # IMPORTANTE: Adicione o parâmetro memory=memory
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        # memory=memory  # TODO: Descomente e use a memory criada
    )

    return agent_executor


# ============================================================================
# Testes de Comparação (NÃO MODIFIQUE)
# ============================================================================

def test_without_memory():
    """Demonstra limitações SEM memory."""
    print("TESTE 1: AGENTE SEM MEMORY")
    print("=" * 70)

    agent = create_agent_without_memory()

    print("\nConversa 1: Analisar arquivo")
    print("-" * 70)
    r1 = agent.invoke({"input": "Analise o arquivo ./sample_project/calculator.py"})
    print(f"Resposta: {r1['output']}\n")

    print("Conversa 2: Pergunta sobre conversa anterior")
    print("-" * 70)
    r2 = agent.invoke({"input": "Quantas funções ele tem?"})
    print(f"Resposta: {r2['output']}\n")
    print("=" * 70)


def test_with_memory():
    """Demonstra vantagens COM memory."""
    print("\n\n🟢 TESTE 2: AGENTE COM MEMORY")
    print("=" * 70)

    agent = create_agent_with_memory()

    print("\nConversa 1: Analisar arquivo")
    print("-" * 70)
    r1 = agent.invoke({"input": "Analise o arquivo ./sample_project/calculator.py"})
    print(f"Resposta: {r1['output']}\n")

    print("Conversa 2: Pergunta sobre conversa anterior")
    print("-" * 70)
    r2 = agent.invoke({"input": "Quantas funções ele tem?"})
    print(f"Resposta: {r2['output']}\n")

    print("Conversa 3: Outra pergunta contextual")
    print("-" * 70)
    r3 = agent.invoke({"input": "E classes, tinha alguma?"})
    print(f"Resposta: {r3['output']}\n")
    print("=" * 70)


def test_memory():
    try:
        test_without_memory()
        test_with_memory()

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_memory()
