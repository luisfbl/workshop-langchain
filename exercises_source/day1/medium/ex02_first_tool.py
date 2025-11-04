"""
Exercício 2 - Primeira Tool Customizada (MEDIUM)
=================================================

OBJETIVO: Criar uma tool robusta e observar o padrão ReAct em ação.

TEMPO: 15 minutos

O QUE VOCÊ VAI APRENDER:
- Criar tools com tratamento de erros
- Importância da docstring clara
- Como o agente interpreta e usa tools
- Debugging de agentes com verbose

CONTEXTO:
Vamos adicionar a capacidade de listar arquivos ao agente.
Foque em fazer uma tool robusta que lida com erros.
"""

# I AM NOT DONE

from pathlib import Path
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ============================================================================
# TODO 1: Criar tool robusta de listagem
# ============================================================================

@tool
def list_python_files(directory: str) -> str:
    """
    TODO: Escreva uma docstring clara que explique:
    - O que a tool faz
    - QUANDO o agente deve usá-la (isso é crucial!)
    - O que ela retorna
    - Exemplos de uso se quiser

    Lembre: O LLM vai LER esta docstring para decidir se usa a tool!
    """
    # TODO: Implemente com tratamento de erros
    # Considere:
    # - Diretório não existe
    # - Sem permissão de leitura
    # - Nenhum arquivo .py encontrado
    # - Retorno formatado e útil

    pass


# ============================================================================
# TODO 2: Criar o agente completo
# ============================================================================

def create_agent_with_tool():
    """
    TODO: Implemente a criação completa do agente com a tool.

    Estrutura:
    1. LLM
    2. Prompt
    3. Tools (agora COM list_python_files)
    4. Agent
    5. Executor (com verbose=True para ver o raciocínio)
    """
    pass


# ============================================================================
# TODO 3: DESAFIO EXTRA - Experimente com a docstring
# ============================================================================

def experiment_with_docstrings():
    """
    OPCIONAL: Crie versões da tool com docstrings diferentes e veja
    como isso afeta a decisão do agente de quando usar a tool.

    Experimente docstrings:
    - Muito vagas
    - Muito específicas
    - Com exemplos
    - Sem exemplos
    """
    pass


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_agent():
    """Testa o agente."""
    print("🤖 Testando agente com tool...\n")

    try:
        agent = create_agent_with_tool()

        test_cases = [
            ("Liste arquivos Python em ./sample_project", "Deve usar tool"),
            ("Quantos arquivos Python tem em ./sample_project?", "Deve usar tool"),
            ("O que é um arquivo Python?", "NÃO deve usar tool"),
            ("Liste arquivos em /diretorio/inexistente", "Deve lidar com erro")
        ]

        for query, expectation in test_cases:
            print("=" * 60)
            print(f"TESTE: {query}")
            print(f"Expectativa: {expectation}")
            print("=" * 60)
            response = agent.invoke({"input": query})
            print(f"Resposta: {response['output']}\n")

        print("✅ Todos os testes concluídos!")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent()
