"""
Exercício 7 - Orchestrator com Conditional Routing (MEDIUM)
===========================================================

OBJETIVO: Criar um orchestrator avançado com LangGraph que toma decisões
         baseadas no state usando conditional routing.

TEMPO: 25 minutos

O QUE VOCÊ VAI APRENDER:
- Conditional edges (if/else no graph)
- Error handling e retry logic
- Supervisor pattern
- Processamento de múltiplos arquivos
- Combinação de análise + geração

CONTEXTO:
No ex06 você criou um graph LINEAR (A → B → C → END).
Agora vamos criar um graph INTELIGENTE que toma decisões!

WORKFLOW DESTE EXERCÍCIO:
                       START
                         ↓
                  [list_files]
                         ↓
                  [process_file] ←────┐
                         ↓             │
                   [should_retry?] ───┘ (se erro e attempts < 3)
                         ↓
                  [has_more_files?]
                    ↙         ↘
              [process_file]  [combine_docs]
                                  ↓
                                 END
"""

# I AM NOT DONE

from typing import TypedDict, List, Literal
from pathlib import Path
import ast
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# ============================================================================
# TODO 1: Definir State com campos de controle
# ============================================================================

class OrchestratorState(TypedDict):
    """State para orchestrator que processa múltiplos arquivos."""

    # Input inicial
    directory: str  # Diretório com arquivos Python

    # Lista de arquivos
    files_to_process: List[str]
    files_processed: List[str]

    # Arquivo atual
    current_file: str
    current_code: str

    # Análise do arquivo atual
    current_analysis: dict  # {functions: [], classes: [], lines: 0}

    # Documentação de cada arquivo
    all_docs: List[dict]  # [{file: "x.py", doc: "..."}]

    # Controle de fluxo
    current_step: str
    error: str  # Se houver erro
    retry_count: int  # Tentativas do arquivo atual

    # Output final
    final_documentation: str  # Documentação combinada de todos


# ============================================================================
# TODO 2: Nodes do workflow
# ============================================================================

def list_files_node(state: OrchestratorState) -> dict:
    """Node inicial: Lista arquivos Python do diretório."""
    path = Path(state["directory"])
    # TODO 2.1: Buscar arquivos .py
    python_files = []  # TODO: [str(f) for f in path.glob("*.py")]

    return {
        "files_to_process": None,  # TODO: python_files
        "files_processed": [],
        "all_docs": [],
        "current_step": "list_files"
    }


def process_file_node(state: OrchestratorState) -> dict:
    """Node principal: Processa um arquivo (lê, analisa, gera doc)."""

    # TODO 2.2: Pegar próximo arquivo
    if not state["files_to_process"]:
        return {"current_step": "no_more_files"}

    current_file = state["files_to_process"][0]
    print(f"Processando: {Path(current_file).name}")

    try:
        # TODO 2.3: Ler arquivo
        with open(current_file, 'r', encoding='utf-8') as f:
            code = None  # TODO: f.read()

        # TODO 2.4: Analisar com AST
        tree = None  # TODO: ast.parse(code)

        functions = []
        classes = []
        # TODO: Extrair com ast.walk

        analysis = {
            "functions": functions,
            "classes": classes,
            "lines": len(code.split('\n'))
        }

        # TODO 2.5: Gerar documentação com LLM
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Gere documentação concisa em markdown."),
            ("human", "Arquivo: {file}\nFunções: {funcs}\nClasses: {classes}\n\nGere doc:")
        ])

        chain = prompt | llm
        response = None  # TODO: chain.invoke({...})
        doc = "TODO"  # TODO: response.content

        # TODO 2.6: Adicionar doc à lista
        new_doc = {
            "file": Path(current_file).name,
            "documentation": doc
        }

        all_docs = state["all_docs"].copy()
        all_docs.append(new_doc)

        # TODO 2.7: Mover arquivo para processados
        processed = state["files_processed"].copy()
        processed.append(current_file)

        to_process = state["files_to_process"].copy()
        to_process.pop(0)

        return {
            "current_file": current_file,
            "current_code": code,
            "current_analysis": analysis,
            "all_docs": all_docs,
            "files_processed": processed,
            "files_to_process": to_process,
            "error": "",  # Limpar erro
            "retry_count": 0,  # Reset retry
            "current_step": "process_success"
        }

    except Exception as e:
        return {
            "error": str(e),
            "retry_count": state.get("retry_count", 0) + 1,
            "current_step": "process_error"
        }


def combine_docs_node(state: OrchestratorState) -> dict:
    """Node final: Combina todas as documentações em um README."""
    # TODO 2.8: Criar README combinado
    readme = "# Documentação do Projeto\n\n"
    readme += f"Total de arquivos: {len(state['all_docs'])}\n\n"
    readme += "---\n\n"

    for doc in state["all_docs"]:
        readme += f"## {doc['file']}\n\n"
        readme += doc['documentation']
        readme += "\n\n---\n\n"

    return {
        "final_documentation": readme,
        "current_step": "combine_success"
    }


# ============================================================================
# TODO 3: Conditional Routing Functions
# ============================================================================
# Estas funções decidem qual node executar a seguir baseado no state

def should_retry(state: OrchestratorState) -> Literal["process_file", "skip_file"]:
    """Decide se deve tentar processar o arquivo novamente.

    Lógica:
    - Se teve erro E retry_count < 3: tenta de novo
    - Caso contrário: pula arquivo
    """
    # TODO 3.1: Implementar lógica de retry
    has_error = state.get("error", "") != ""
    attempts = state.get("retry_count", 0)

    if has_error and attempts < 3:
        return "process_file"
    elif has_error:
        # TODO: Mover arquivo para processed mesmo com erro
        return "skip_file"
    else:
        return "skip_file"  # Sem erro, não precisa retry


def has_more_files(state: OrchestratorState) -> Literal["process_file", "combine_docs"]:
    """Decide se deve processar mais arquivos ou combinar resultados.

    Lógica:
    - Se files_to_process não está vazio: processar próximo
    - Caso contrário: combinar docs e finalizar
    """
    # TODO 3.2: Implementar lógica
    if len(state["files_to_process"]) > 0:
        return "process_file"
    else:
        return "combine_docs"


def skip_file_node(state: OrchestratorState) -> dict:
    """Node auxiliar: Remove arquivo com erro da fila."""
    to_process = state["files_to_process"].copy()
    if to_process:
        to_process.pop(0)

    return {
        "files_to_process": to_process,
        "error": "",
        "retry_count": 0,
        "current_step": "file_skipped"
    }


# ============================================================================
# TODO 4: Construir Graph com Conditional Routing
# ============================================================================

def create_orchestrator_graph():
    """Cria graph com conditional routing."""
    # TODO 4.1: Criar StateGraph
    workflow = None  # TODO: StateGraph(OrchestratorState)

    # TODO 4.2: Adicionar nodes
    # TODO: workflow.add_node("list_files", list_files_node)
    # TODO: workflow.add_node("process_file", process_file_node)
    # TODO: workflow.add_node("skip_file", skip_file_node)
    # TODO: workflow.add_node("combine_docs", combine_docs_node)

    # TODO 4.3: Set entry point
    # TODO: workflow.set_entry_point("list_files")

    # TODO 4.4: Adicionar edges normais
    # TODO: workflow.add_edge("list_files", "process_file")
    # TODO: workflow.add_edge("skip_file", ...)  # Para onde vai?
    # TODO: workflow.add_edge("combine_docs", END)

    # TODO 4.5: Adicionar CONDITIONAL EDGES
    # Após process_file, decidir se deve retry ou continuar
    # DICA: workflow.add_conditional_edges(
    #     "process_file",
    #     função_que_decide,
    #     {
    #         "opção1": "node_destino1",
    #         "opção2": "node_destino2"
    #     }
    # )

    # TODO: Após process_file, verificar se deve processar mais ou combinar
    # workflow.add_conditional_edges(
    #     "process_file",
    #     has_more_files,
    #     {
    #         "process_file": "process_file",  # Loop!
    #         "combine_docs": "combine_docs"
    #     }
    # )

    # TODO 4.6: Compilar
    graph = None  # TODO: workflow.compile()

    return graph


# ============================================================================
# TODO 5: Executar Orchestrator
# ============================================================================

def run_orchestrator(directory: str) -> str:
    """Executa orchestrator completo.

    Args:
        directory: Diretório com arquivos Python

    Returns:
        README.md completo
    """
    print(f"\n=== ORCHESTRATOR: {directory} ===\n")

    # TODO 5.1: Criar graph
    graph = None  # TODO: create_orchestrator_graph()

    # TODO 5.2: State inicial
    initial_state: OrchestratorState = {
        "directory": directory,
        # TODO: Inicializar outros campos
        "files_to_process": [],
        "files_processed": [],
        "current_file": "",
        "current_code": "",
        "current_analysis": {},
        "all_docs": [],
        "current_step": "start",
        "error": "",
        "retry_count": 0,
        "final_documentation": ""
    }

    # TODO 5.3: Executar
    final_state = None  # TODO: graph.invoke(initial_state)

    print(f"\n✓ Processados: {len(final_state['files_processed'])} | Docs: {len(final_state['all_docs'])}\n")

    return final_state["final_documentation"]


# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_orchestrator():
    """Testa orchestrator com conditional routing."""
    try:
        print("\n=== ORCHESTRATOR ===")
        print("Conditional routing | Retry logic | Multi-file\n")

        readme = run_orchestrator("./sample_project")

        print("\n--- README GERADO ---")
        print(readme[:500] + "..." if len(readme) > 500 else readme)

        print("\n✓ Completo! Agora integre tudo no main.py\n")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_orchestrator()
