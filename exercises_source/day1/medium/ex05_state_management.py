"""
Exercicio 4 - State Management Avançado (MEDIUM)
=================================================

OBJETIVO: Criar sistema de state management com metricas de qualidade de codigo
         e pipeline de processamento com multiplas etapas.

TEMPO: 20 minutos

O QUE VOCE VAI IMPLEMENTAR:
- State complexo com metricas de qualidade
- Pipeline com 3 etapas: scan -> analyze -> report
- Sistema de prioridades para arquivos
- Agregacao de metricas

DESAFIO:
Diferente do exercicio EASY, voce vai implementar um state mais sofisticado
que alem de contar funcoes, vai calcular metricas de qualidade:
- Complexidade ciclomatica aproximada
- Cobertura de docstrings
- Razao codigo/comentarios
- Score de qualidade geral
"""

# I AM NOT DONE

from typing import TypedDict
from pathlib import Path
from dataclasses import dataclass
import ast

# ============================================================================
# TODO 1: Definir estruturas de dados
# ============================================================================

@dataclass
class FileMetrics:
    """Metricas de um arquivo individual."""
    file_path: str
    lines_of_code: int
    num_functions: int
    num_classes: int
    functions_with_docstrings: int
    complexity_score: float  # 0-10 (simplificado)
    quality_score: float  # 0-100


class _AnalysisStateRequired(TypedDict):
    """Campos obrigatorios do state."""

    files_to_process: list[str]
    files_processed: list[str]
    current_file: str
    total_lines: int
    total_functions: int
    errors: list[str]


class AnalysisState(_AnalysisStateRequired, total=False):
    """State completo do pipeline."""

    file_metrics: dict[str, FileMetrics]
    total_files: int
    avg_quality_score: float
    warnings: list[str]


# ============================================================================
# TODO 2: Funcoes de analise de codigo
# ============================================================================

def calculate_complexity(tree: ast.AST) -> float:
    """Calcula complexidade ciclomatica aproximada.

    Conta decisoes (if, for, while, except, etc).

    Args:
        tree: AST do codigo

    Returns:
        Score de complexidade (0-10)
    """
    decision_nodes = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.ExceptHandler,
        ast.With,
        ast.AsyncWith,
    )
    decisions = sum(1 for node in ast.walk(tree) if isinstance(node, decision_nodes))

    # Cada duas decisoes equivalem a 1 ponto na escala 0-10
    normalized = decisions / 2.0
    return min(normalized, 10.0)


def calculate_quality_score(metrics: FileMetrics) -> float:
    """Calcula score de qualidade geral (0-100).

    Considera:
    - Cobertura de docstrings (60%)
    - Baixa complexidade (40%)

    Args:
        metrics: Metricas do arquivo

    Returns:
        Score 0-100
    """
    # Docstring coverage (60 pontos)
    docstring_score = 0
    if metrics.num_functions + metrics.num_classes > 0:
        total_items = metrics.num_functions + metrics.num_classes
        docstring_score = (metrics.functions_with_docstrings / total_items) * 60

    # Complexity (40 pontos - inverse: less is better)
    complexity_points = max(0.0, (10.0 - metrics.complexity_score) * 4)

    total_score = docstring_score + complexity_points

    return max(0, min(100, total_score))


def analyze_file(file_path: str) -> FileMetrics:
    """Analisa um arquivo e extrai todas as metricas.

    Args:
        file_path: Caminho do arquivo

    Returns:
        FileMetrics com todas as metricas
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        tree = ast.parse(content)

    num_functions = 0
    num_classes = 0
    functions_with_docstrings = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            num_functions += 1
            if ast.get_docstring(node):
                functions_with_docstrings += 1
        elif isinstance(node, ast.ClassDef):
            num_classes += 1
            if ast.get_docstring(node):
                functions_with_docstrings += 1

    complexity = calculate_complexity(tree)

    # Criar metrics
    metrics = FileMetrics(
        file_path=file_path,
        lines_of_code=len(lines),
        num_functions=num_functions,
        num_classes=num_classes,
        functions_with_docstrings=functions_with_docstrings,
        complexity_score=complexity,
        quality_score=0
    )

    metrics.quality_score = calculate_quality_score(metrics)

    return metrics


# ============================================================================
# TODO 3: Pipeline de processamento com State
# ============================================================================

def initialize_state(directory: str) -> AnalysisState:
    """Inicializa state com lista de arquivos Python."""

    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Diretorio nao encontrado: {directory}")

    prioritized_files: list[tuple[int, str]] = []
    for file_path in path.rglob("*.py"):
        if file_path.is_file():
            size = file_path.stat().st_size
            prioritized_files.append((-size, str(file_path.resolve())))

    python_files = [file for _, file in sorted(prioritized_files)]

    state: AnalysisState = {
        "files_to_process": python_files,
        "files_processed": [],
        "current_file": "",
        "file_metrics": {},
        "total_files": len(python_files) if python_files else 0,
        "total_lines": 0,
        "total_functions": 0,
        "avg_quality_score": 0.0,
        "errors": [],
        "warnings": []
    }

    return state


def process_next_file(state: AnalysisState) -> AnalysisState:
    """Processa proximo arquivo e atualiza state.

    Args:
        state: State atual

    Returns:
        State atualizado
    """
    if not state["files_to_process"]:
        return state
    state.setdefault("file_metrics", {})
    state.setdefault("warnings", [])
    state.setdefault("avg_quality_score", 0.0)
    state.setdefault("total_files", len(state["files_processed"]) + len(state["files_to_process"]))

    current = state["files_to_process"][0]
    state["current_file"] = current

    print(f"\nAnalisando: {Path(current).name}")

    try:
        metrics = analyze_file(current)

        state["file_metrics"][current] = metrics
        state["total_lines"] += metrics.lines_of_code
        state["total_functions"] += metrics.num_functions

        if metrics.quality_score < 50:
            state["warnings"].append(f"{Path(current).name}: Qualidade baixa")

        state["files_processed"].append(current)
        state["files_to_process"].pop(0)

        total_quality = sum(m.quality_score for m in state["file_metrics"].values())
        processed = len(state["file_metrics"])
        state["avg_quality_score"] = total_quality / processed if processed else 0.0

        print(f"  Qualidade: {metrics.quality_score:.1f}/100")
        print(f"  Complexidade: {metrics.complexity_score:.1f}/10")

    except Exception as e:
        state["errors"].append(f"{current}: {str(e)}")
        state["files_to_process"].pop(0)
        print(f"  Erro: {e}")

    return state


def generate_quality_report(state: AnalysisState) -> str:
    """Gera relatorio detalhado de qualidade.

    Args:
        state: State final

    Returns:
        Relatorio formatado
    """
    # Calcular media de qualidade
    file_metrics = state.get("file_metrics", {})
    if file_metrics:
        total_quality = sum(m.quality_score for m in file_metrics.values())
        state["avg_quality_score"] = total_quality / len(file_metrics)
    else:
        state.setdefault("avg_quality_score", 0.0)

    report = f"""
{'=' * 70}
RELATORIO DE QUALIDADE DE CODIGO
{'=' * 70}

RESUMO GERAL:
  Arquivos analisados: {len(state['files_processed'])}
  Total de linhas: {state['total_lines']}
  Total de funcoes: {state['total_functions']}
  Score medio de qualidade: {state['avg_quality_score']:.1f}/100

"""

    warnings = state.get("warnings", [])
    if warnings:
        report += f"\nAVISOS ({len(warnings)}):\n"
        for warning in warnings:
            report += f"  - {warning}\n"

    sorted_files = sorted(
        file_metrics.values(),
        key=lambda m: m.quality_score,
        reverse=True
    )

    if sorted_files:
        report += "\nTOP 3 MELHORES:\n"
        for metrics in sorted_files[:3]:
            report += f"  {Path(metrics.file_path).name}: {metrics.quality_score:.1f}\n"

        report += "\nTOP 3 QUE PRECISAM ATENCAO:\n"
        for metrics in sorted_files[-3:]:
            report += f"  {Path(metrics.file_path).name}: {metrics.quality_score:.1f}\n"

    if state["errors"]:
        report += f"\nERROS ({len(state['errors'])}):\n"
        for error in state["errors"]:
            report += f"  - {error}\n"

    report += "\n" + "=" * 70

    return report


def get_state_summary(state: AnalysisState) -> str:
    """Retorna resumo amigavel do state corrente."""

    processed = len(state.get("files_processed", []))
    pending = len(state.get("files_to_process", []))
    avg_quality = state.get("avg_quality_score", 0.0)

    summary = [
        "RESUMO DO STATE",
        "======================",
        f"Arquivos processados: {processed}",
        f"Arquivos pendentes: {pending}",
        f"Total de funcoes: {state.get('total_functions', 0)}",
        f"Total de linhas: {state.get('total_lines', 0)}",
        f"Score medio: {avg_quality:.1f}/100",
        f"Erros: {len(state.get('errors', []))}",
    ]

    current = state.get("current_file", "")
    if current:
        summary.append(f"Processando agora: {Path(current).name}")

    warnings = state.get("warnings", [])
    if warnings:
        summary.append("\nAvisos:")
        summary.extend(f"  - {warning}" for warning in warnings)

    errors = state.get("errors", [])
    if errors:
        summary.append("\nErros:")
        summary.extend(f"  - {error}" for error in errors)

    return "\n".join(summary)


def run_analysis_workflow(directory: str) -> AnalysisState:
    """Executa pipeline completo de analise de qualidade.

    Args:
        directory: Diretorio com codigo Python

    Returns:
        State final com todas as metricas
    """
    print("\n=== ANALISE DE QUALIDADE ===\n")

    state = initialize_state(directory)

    print(f"Arquivos encontrados: {state['total_files']}\n")

    while state["files_to_process"]:
        state = process_next_file(state)

    # Gerar relatorio
    report = generate_quality_report(state)
    print(report)
    print()
    print(get_state_summary(state))

    return state


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_quality_pipeline():
    """Testa pipeline completo."""
    try:
        final_state = run_analysis_workflow("./sample_project")
        return final_state

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    _ = test_quality_pipeline()
