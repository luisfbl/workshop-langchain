"""
Exercício 6 - Introdução ao LangGraph (EASY)
============================================

OBJETIVO: Criar seu primeiro StateGraph com LangGraph para automatizar
         um workflow de análise e geração de documentação.

TEMPO: 25 minutos

O QUE VOCÊ VAI APRENDER:
- O que é LangGraph e por que usar
- Criar StateGraph
- Definir nodes (funções que processam state)
- Conectar nodes com edges
- Executar o graph e ver state fluindo

CONTEXTO:
No Dia 1 você viu State management manual. Agora vamos usar LangGraph,
um framework que automatiza o gerenciamento de state em workflows!

LangGraph = Graph (nodes + edges) + State compartilhado

WORKFLOW DESTE EXERCÍCIO:
  START → read_file → analyze_code → generate_docs → END
           ↓            ↓               ↓
         [state é passado e atualizado entre nodes]
"""

# I AM NOT DONE

from typing import TypedDict, List, Annotated
from pathlib import Path
import ast
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# ============================================================================
# TODO 1: Definir o State do workflow
# ============================================================================

class DocGenState(TypedDict):
    """State compartilhado entre todos os nodes do graph.

    Cada node recebe este state, faz seu trabalho, e retorna state atualizado.
    LangGraph automaticamente passa o state entre os nodes!
    """
    # TODO 1.1: Defina os campos do state

    # Campos de entrada (definidos no início):
    file_path: str  # Arquivo a ser documentado

    # Campos de processamento (preenchidos pelos nodes):
    # code_content: str  # Conteúdo do arquivo
    # num_functions: int  # Número de funções
    # num_classes: int  # Número de classes
    # functions_list: List[str]  # Lista de nomes de funções

    # Campo de saída (resultado final):
    # documentation: str  # Documentação gerada

    # Campo de controle:
    # current_step: str  # Para debug: qual node está executando


# ============================================================================
# TODO 2: Criar os Nodes do workflow
# ============================================================================
# IMPORTANTE: Nodes são funções que:
#  1. Recebem state
#  2. Fazem algum processamento
#  3. Retornam dict com campos do state a serem ATUALIZADOS
#
# LangGraph faz merge automático do retorno com o state existente!
# ============================================================================

def read_file_node(state: DocGenState) -> dict:
    """Node 1: Lê o arquivo e adiciona conteúdo ao state.

    Args:
        state: State atual (só precisa de file_path)

    Returns:
        Dict com campos atualizados (code_content, current_step)
    """
    # TODO 2.1: Ler o arquivo
    file_path = state["file_path"]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = None  # TODO: f.read()

        # TODO 2.2: Retornar campos atualizados
        # IMPORTANTE: Retorne apenas os campos que você quer ATUALIZAR!
        return {
            "code_content": None,  # TODO: content
            "current_step": "read_file"
        }

    except FileNotFoundError:
        return {
            "code_content": "",
            "current_step": "error"
        }


def analyze_code_node(state: DocGenState) -> dict:
    """Node 2: Analisa o código usando AST.

    Args:
        state: State atual (precisa de code_content)

    Returns:
        Dict com análise (num_functions, num_classes, functions_list)
    """
    # TODO 2.3: Parsear código com AST
    code = state["code_content"]

    try:
        tree = None  # TODO: ast.parse(code)

        # TODO 2.4: Contar funções e classes
        functions = []
        classes = []

        # TODO: Implementar com ast.walk
        # DICA:
        # for node in ast.walk(tree):
        #     if isinstance(node, ast.FunctionDef):
        #         functions.append(node.name)
        #     elif isinstance(node, ast.ClassDef):
        #         classes.append(node.name)

        num_functions = 0  # TODO: len(functions)
        num_classes = 0  # TODO: len(classes)

        # TODO 2.5: Retornar análise
        return {
            "num_functions": None,  # TODO
            "num_classes": None,  # TODO
            "functions_list": None,  # TODO: functions
            "current_step": "analyze_code"
        }

    except SyntaxError as e:
        return {
            "num_functions": 0,
            "num_classes": 0,
            "functions_list": [],
            "current_step": "error"
        }


def generate_docs_node(state: DocGenState) -> dict:
    """Node 3: Gera documentação usando LLM.

    Args:
        state: State com análise completa

    Returns:
        Dict com documentation
    """
    # TODO 2.6: Criar prompt para o LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente que gera documentação para código Python."),
        ("human", """Analise este arquivo e gere documentação em markdown:

Arquivo: {file_path}
Funções encontradas: {num_functions}
Classes encontradas: {num_classes}
Lista de funções: {functions_list}

Gere documentação concisa com:
1. Título com nome do arquivo
2. Breve descrição do propósito
3. Lista de funções principais
4. Exemplo de uso se aplicável

Formato: Markdown""")
    ])

    # TODO 2.7: Chamar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    chain = None  # TODO: prompt | llm

    try:
        # TODO 2.8: Gerar documentação
        response = None  # TODO: chain.invoke({...})

        # DICA: Passar todos os campos do state que o prompt precisa
        # response = chain.invoke({
        #     "file_path": state["file_path"],
        #     "num_functions": state["num_functions"],
        #     "num_classes": state["num_classes"],
        #     "functions_list": ", ".join(state["functions_list"])
        # })

        documentation = "TODO"  # TODO: response.content

        return {
            "documentation": None,  # TODO: documentation
            "current_step": "generate_docs"
        }

    except Exception as e:
        return {
            "documentation": f"Erro ao gerar documentação: {e}",
            "current_step": "error"
        }


# ============================================================================
# TODO 3: Construir o Graph
# ============================================================================

def create_documentation_graph():
    """Cria o StateGraph com os 3 nodes conectados.

    Returns:
        Graph compilado pronto para executar
    """
    # TODO 3.1: Criar StateGraph com o tipo do state
    workflow = None  # TODO: StateGraph(DocGenState)

    # TODO 3.2: Adicionar os nodes
    # DICA: workflow.add_node(nome, função)

    # TODO: workflow.add_node("read_file", read_file_node)
    # TODO: workflow.add_node("analyze_code", analyze_code_node)
    # TODO: workflow.add_node("generate_docs", generate_docs_node)

    # TODO 3.3: Definir ponto de entrada
    # DICA: workflow.set_entry_point(nome_do_node)
    # TODO: workflow.set_entry_point("read_file")

    # TODO 3.4: Conectar os nodes com edges
    # DICA: workflow.add_edge(de, para)
    # Sequência: read_file → analyze_code → generate_docs → END

    # TODO: workflow.add_edge("read_file", "analyze_code")
    # TODO: workflow.add_edge("analyze_code", "generate_docs")
    # TODO: workflow.add_edge("generate_docs", END)

    # TODO 3.5: Compilar o graph
    graph = None  # TODO: workflow.compile()

    return graph


# ============================================================================
# TODO 4: Executar o workflow
# ============================================================================

def run_documentation_workflow(file_path: str) -> str:
    """Executa o workflow completo e retorna documentação.

    Args:
        file_path: Caminho do arquivo Python para documentar

    Returns:
        Documentação em markdown
    """
    print(f"\n=== WORKFLOW: {Path(file_path).name} ===\n")

    # TODO 4.1: Criar graph
    graph = None  # TODO: create_documentation_graph()

    # TODO 4.2: Criar state inicial
    # IMPORTANTE: Só precisa definir file_path, resto é preenchido pelos nodes!
    initial_state: DocGenState = {
        "file_path": file_path,
        # TODO: Inicialize os outros campos com valores vazios/zero
        # "code_content": "",
        # "num_functions": 0,
        # ...
    }

    # TODO 4.3: Executar graph
    # DICA: graph.invoke(initial_state)
    final_state = None  # TODO: graph.invoke(initial_state)

    # TODO 4.4: Retornar documentação
    return None  # TODO: final_state["documentation"]


# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_langgraph():
    """Testa o workflow com LangGraph."""
    try:
        print("\n=== LANGGRAPH WORKFLOW ===")
        print("State automatico | Nodes conectados | Workflow visual\n")

        documentation = run_documentation_workflow("./sample_project/calculator.py")

        print("\n--- DOCUMENTACAO GERADA ---")
        print(documentation)

        print("\n✓ Workflow completo! Proximo: conditional routing (ex07)\n")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_langgraph()
