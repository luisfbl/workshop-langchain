"""
Exercicio 6 - LangGraph com Processamento Paralelo (MEDIUM)
===========================================================

OBJETIVO: Criar workflow com LangGraph que processa múltiplos arquivos
         em paralelo e combina resultados.

TEMPO: 35 minutos

O QUE VOCE VAI IMPLEMENTAR:
- Graph com processamento paralelo de múltiplos arquivos
- Fan-out pattern (1 node -> N nodes paralelos)
- Fan-in pattern (N nodes -> 1 node combinador)
- Error handling individual por arquivo
- Progress tracking

DESAFIO:
Diferente do EASY que processa UM arquivo linearmente, você vai:
1. Processar MULTIPLOS arquivos ao mesmo tempo
2. Cada arquivo tem seu próprio sub-workflow
3. Combinar todos os resultados no final
4. Lidar com erros sem travar todo o pipeline

WORKFLOW:
            START
              ↓
          [list_files]
              ↓
     ┌────────┴────────┐
     ↓        ↓        ↓
  [proc_1] [proc_2] [proc_3]  <- PARALELO
     ↓        ↓        ↓
     └────────┬────────┘
              ↓
        [combine_all]
              ↓
             END
"""

# I AM NOT DONE

from typing import TypedDict, List, Dict, Optional
from pathlib import Path
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

# ============================================================================
# TODO 1: Definir State para processamento paralelo
# ============================================================================

class FileResult(TypedDict):
    """Resultado do processamento de um arquivo individual."""
    file_path: str
    success: bool
    documentation: Optional[str]
    error: Optional[str]
    num_functions: int
    num_classes: int


class ParallelDocGenState(TypedDict):
    """State para workflow paralelo.

    Diferente do EASY, este state precisa trackear múltiplos arquivos
    sendo processados simultaneamente.
    """
    # Input
    directory: str
    files_to_process: List[str]

    # Processing results (um por arquivo)
    file_results: Dict[str, FileResult]  # filepath -> result

    # Aggregated output
    combined_documentation: str
    total_files: int
    successful: int
    failed: int

    # Progress
    current_stage: str


# ============================================================================
# TODO 2: Funcoes auxiliares para processar cada arquivo
# ============================================================================

def analyze_single_file(file_path: str) -> FileResult:
    """Analisa UM arquivo e retorna resultado.

    Esta funcao sera chamada em paralelo para cada arquivo.

    Args:
        file_path: Caminho do arquivo

    Returns:
        FileResult com analise ou erro
    """
    # TODO: Implementar analise completa
    # DICA: Similar ao ex06 easy, mas retorna FileResult

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)

        # TODO: Contar funcoes e classes
        num_functions = 0
        num_classes = 0

        # TODO: Implemente contagem

        # TODO: Gerar documentacao
        llm = ChatOpenAI(model="gpt-5-nano", temperature=0.7)
        # ... gere doc

        documentation = "TODO"  # TODO: gerar de verdade

        return FileResult(
            file_path=file_path,
            success=True,
            documentation=documentation,
            error=None,
            num_functions=num_functions,
            num_classes=num_classes
        )

    except Exception as e:
        # Capturar erro SEM travar todo o pipeline
        return FileResult(
            file_path=file_path,
            success=False,
            documentation=None,
            error=str(e),
            num_functions=0,
            num_classes=0
        )


# ============================================================================
# TODO 3: Nodes do workflow paralelo
# ============================================================================

def list_files_node(state: ParallelDocGenState) -> dict:
    """Node inicial: Lista arquivos para processar."""
    path = Path(state["directory"])
    python_files = [str(f) for f in path.glob("*.py")]

    print(f"Encontrados {len(python_files)} arquivos para processar\n")

    return {
        "files_to_process": python_files,
        "total_files": len(python_files),
        "file_results": {},
        "current_stage": "listed"
    }


def process_files_parallel_node(state: ParallelDocGenState) -> dict:
    """Node que processa TODOS os arquivos em PARALELO.

    Este e o node mais importante! Usa ThreadPoolExecutor para
    processar multiplos arquivos simultaneamente.
    """
    files = state["files_to_process"]

    if not files:
        return {"current_stage": "no_files"}

    print(f"Processando {len(files)} arquivos em paralelo...")

    results = {}

    # TODO: Implementar processamento paralelo
    # DICA: Use ThreadPoolExecutor
    # DICA: with ThreadPoolExecutor(max_workers=4) as executor:
    #           futures = {executor.submit(analyze_single_file, f): f for f in files}
    #           for future in as_completed(futures):
    #               file_path = futures[future]
    #               result = future.result()
    #               results[file_path] = result

    # TODO: Implemente aqui

    # Contar sucessos e falhas
    successful = sum(1 for r in results.values() if r["success"])
    failed = len(results) - successful

    print(f"Completo: {successful} sucesso, {failed} falhas")

    return {
        "file_results": results,
        "successful": successful,
        "failed": failed,
        "current_stage": "processed"
    }


def combine_results_node(state: ParallelDocGenState) -> dict:
    """Node final: Combina todos os resultados em uma documentacao."""
    results = state["file_results"]

    # TODO: Criar documentacao combinada
    readme = "# Documentacao do Projeto\n\n"
    readme += f"Total de arquivos: {state['total_files']}\n"
    readme += f"Processados com sucesso: {state['successful']}\n"
    readme += f"Falhas: {state['failed']}\n\n"
    readme += "---\n\n"

    # TODO: Adicionar documentacao de cada arquivo bem-sucedido
    for file_path, result in results.items():
        if result["success"]:
            readme += f"## {Path(file_path).name}\n\n"
            readme += result["documentation"]
            readme += "\n\n---\n\n"

    # TODO: Adicionar secao de erros
    failed_files = [f for f, r in results.items() if not r["success"]]
    if failed_files:
        readme += "## Arquivos com Erro\n\n"
        for file_path in failed_files:
            error = results[file_path]["error"]
            readme += f"- **{Path(file_path).name}**: {error}\n"

    return {
        "combined_documentation": readme,
        "current_stage": "combined"
    }


# ============================================================================
# TODO 4: Construir graph paralelo
# ============================================================================

def create_parallel_graph():
    """Cria graph com processamento paralelo.

    Estrutura:
    list_files -> process_parallel -> combine -> END
    """
    # TODO: Criar workflow
    workflow = None  # TODO: StateGraph(ParallelDocGenState)

    # TODO: Adicionar nodes
    # workflow.add_node("list_files", list_files_node)
    # workflow.add_node("process_parallel", process_files_parallel_node)
    # workflow.add_node("combine", combine_results_node)

    # TODO: Conectar
    # workflow.set_entry_point("list_files")
    # workflow.add_edge("list_files", "process_parallel")
    # workflow.add_edge("process_parallel", "combine")
    # workflow.add_edge("combine", END)

    # TODO: Compilar
    graph = None  # TODO: workflow.compile()

    return graph


# ============================================================================
# TODO 5: Executar workflow paralelo
# ============================================================================

def run_parallel_workflow(directory: str) -> str:
    """Executa workflow paralelo completo.

    Args:
        directory: Diretorio com arquivos Python

    Returns:
        Documentacao combinada
    """
    print(f"\n=== WORKFLOW PARALELO: {directory} ===\n")

    # TODO: Criar graph
    graph = None  # TODO: create_parallel_graph()

    # TODO: State inicial
    initial_state: ParallelDocGenState = {
        "directory": directory,
        "files_to_process": [],
        "file_results": {},
        "combined_documentation": "",
        "total_files": 0,
        "successful": 0,
        "failed": 0,
        "current_stage": "start"
    }

    # TODO: Executar
    final_state = None  # TODO: graph.invoke(initial_state)

    return final_state["combined_documentation"]


# ============================================================================
# Testes (NAO MODIFIQUE)
# ============================================================================

def test_parallel_workflow():
    """Testa workflow paralelo."""
    try:
        print("\n=== PROCESSAMENTO PARALELO ===")
        print("Fan-out | Concurrent | Fan-in | Error handling\n")

        import time
        start = time.time()

        readme = run_parallel_workflow("./sample_project")

        elapsed = time.time() - start

        print(f"\n--- README GERADO em {elapsed:.2f}s ---")
        print(readme[:500] + "..." if len(readme) > 500 else readme)

        print("\n✓ VANTAGENS DO PARALELO:")
        print("  - Mais rapido para muitos arquivos")
        print("  - Erros nao travam todo pipeline")
        print("  - Escalavel\n")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_parallel_workflow()
