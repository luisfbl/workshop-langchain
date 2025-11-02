"""
Exercicio 4 - State Management Avancado (MEDIUM)
=================================================

OBJETIVO: Criar sistema de state management com metricas de qualidade de codigo
         e pipeline de processamento com multiplas etapas.

TEMPO: 25 minutos

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

from typing import TypedDict, List, Dict, Optional
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
    comment_lines: int
    complexity_score: float  # 0-10
    quality_score: float  # 0-100


class QualityState(TypedDict):
    """State para pipeline de analise de qualidade.

    Este state e mais complexo que o do exercicio EASY!
    """
    # Files to scan
    files_to_scan: List[str]
    files_scanned: List[str]

    # Current processing
    current_file: str
    current_stage: str  # 'scan', 'analyze', 'report'

    # Individual metrics
    file_metrics: Dict[str, FileMetrics]  # filepath -> metrics

    # Aggregated metrics
    total_files: int
    total_lines: int
    total_functions: int
    avg_quality_score: float

    # Priority queue (files sorted by size/importance)
    high_priority: List[str]
    low_priority: List[str]

    # Errors and warnings
    errors: List[str]
    warnings: List[str]


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
    # TODO: Implementar
    # DICA: Conte nodes do tipo: If, For, While, ExceptHandler, With
    # Normalize para 0-10 (ex: min(decisions / 2, 10))

    complexity = 0

    # TODO: Implemente usando ast.walk()

    return min(complexity, 10.0)


def calculate_quality_score(metrics: FileMetrics) -> float:
    """Calcula score de qualidade geral (0-100).

    Considera:
    - Cobertura de docstrings (40%)
    - Baixa complexidade (30%)
    - Razao comentarios/codigo (20%)
    - Tamanho das funcoes (10%)

    Args:
        metrics: Metricas do arquivo

    Returns:
        Score 0-100
    """
    # TODO: Implementar formula de qualidade

    # Docstring coverage
    docstring_coverage = 0
    if metrics.num_functions > 0:
        docstring_coverage = (metrics.functions_with_docstrings / metrics.num_functions) * 40

    # TODO: Calcular outros componentes

    # Complexity (inverse - less is better)
    complexity_score = (10 - metrics.complexity_score) * 3  # 0-30 points

    # TODO: Comment ratio
    comment_ratio = 0

    # TODO: Function size penalty
    size_penalty = 0

    total_score = docstring_coverage + complexity_score + comment_ratio - size_penalty

    return max(0, min(100, total_score))


def analyze_file(file_path: str) -> FileMetrics:
    """Analisa um arquivo e extrai todas as metricas.

    Args:
        file_path: Caminho do arquivo

    Returns:
        FileMetrics com todas as metricas
    """
    # TODO: Implementar analise completa
    # DICA: Use ast.parse, ast.walk, contador de linhas, etc.

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        tree = ast.parse(content)

    # TODO: Conte funcoes, classes, docstrings, comentarios
    num_functions = 0
    num_classes = 0
    functions_with_docstrings = 0
    comment_lines = 0

    for node in ast.walk(tree):
        # TODO: Implemente contagem
        pass

    # TODO: Calcule complexidade
    complexity = calculate_complexity(tree)

    # Criar metrics
    metrics = FileMetrics(
        file_path=file_path,
        lines_of_code=len(lines),
        num_functions=num_functions,
        num_classes=num_classes,
        functions_with_docstrings=functions_with_docstrings,
        comment_lines=comment_lines,
        complexity_score=complexity,
        quality_score=0  # Sera calculado depois
    )

    # Calcular quality score
    metrics.quality_score = calculate_quality_score(metrics)

    return metrics


# ============================================================================
# TODO 3: Pipeline de processamento com State
# ============================================================================

def initialize_quality_state(directory: str) -> QualityState:
    """Inicializa state e classifica arquivos por prioridade."""

    path = Path(directory)
    python_files = [str(f) for f in path.glob("*.py")]

    # TODO: Classificar arquivos por prioridade
    # Arquivos maiores ou com 'main' no nome = high priority
    high_priority = []
    low_priority = []

    for file_path in python_files:
        # TODO: Criterio de prioridade
        # DICA: Tamanho do arquivo, ou nome especial
        pass

    state: QualityState = {
        "files_to_scan": python_files,
        "files_scanned": [],
        "current_file": "",
        "current_stage": "scan",
        "file_metrics": {},
        "total_files": len(python_files),
        "total_lines": 0,
        "total_functions": 0,
        "avg_quality_score": 0.0,
        "high_priority": high_priority,
        "low_priority": low_priority,
        "errors": [],
        "warnings": []
    }

    return state


def process_file_stage(state: QualityState) -> QualityState:
    """Processa arquivo atual: scan -> analyze -> next file.

    Args:
        state: State atual

    Returns:
        State atualizado
    """
    # TODO: Implementar pipeline

    # Se nao ha arquivos, retornar
    if not state["files_to_scan"]:
        state["current_stage"] = "complete"
        return state

    # Pegar proximo arquivo (prioridade: high primeiro)
    if state["high_priority"]:
        current = state["high_priority"].pop(0)
    elif state["low_priority"]:
        current = state["low_priority"].pop(0)
    else:
        current = state["files_to_scan"].pop(0)

    state["current_file"] = current
    state["current_stage"] = "analyzing"

    print(f"\nAnalisando: {Path(current).name}")

    try:
        # TODO: Analisar arquivo
        metrics = analyze_file(current)

        # TODO: Adicionar metricas ao state
        state["file_metrics"][current] = metrics

        # TODO: Atualizar agregados
        state["total_lines"] += metrics.lines_of_code
        state["total_functions"] += metrics.num_functions

        # TODO: Adicionar warnings se qualidade baixa
        if metrics.quality_score < 50:
            state["warnings"].append(
                f"{Path(current).name}: Qualidade baixa ({metrics.quality_score:.1f})"
            )

        # Mover para processados
        state["files_scanned"].append(current)

        print(f"  Qualidade: {metrics.quality_score:.1f}/100")
        print(f"  Complexidade: {metrics.complexity_score:.1f}/10")

    except Exception as e:
        state["errors"].append(f"{current}: {str(e)}")
        print(f"  Erro: {e}")

    state["current_stage"] = "scan"
    return state


def generate_quality_report(state: QualityState) -> str:
    """Gera relatorio detalhado de qualidade.

    Args:
        state: State final

    Returns:
        Relatorio formatado
    """
    # TODO: Implementar relatorio bonito

    # Calcular media de qualidade
    if state["file_metrics"]:
        total_quality = sum(m.quality_score for m in state["file_metrics"].values())
        state["avg_quality_score"] = total_quality / len(state["file_metrics"])

    report = f"""
{'=' * 70}
RELATORIO DE QUALIDADE DE CODIGO
{'=' * 70}

RESUMO GERAL:
  Arquivos analisados: {len(state['files_scanned'])}
  Total de linhas: {state['total_lines']}
  Total de funcoes: {state['total_functions']}
  Score medio de qualidade: {state['avg_quality_score']:.1f}/100

"""

    # TODO: Adicionar secao de arquivos com problemas
    if state["warnings"]:
        report += f"\nAVISOS ({len(state['warnings'])}):\n"
        for warning in state["warnings"]:
            report += f"  - {warning}\n"

    # TODO: Top 3 melhores e piores arquivos
    sorted_files = sorted(
        state["file_metrics"].values(),
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


def run_quality_pipeline(directory: str) -> QualityState:
    """Executa pipeline completo de analise de qualidade.

    Args:
        directory: Diretorio com codigo Python

    Returns:
        State final com todas as metricas
    """
    print("\n=== ANALISE DE QUALIDADE ===\n")

    # TODO: Inicializar
    state = initialize_quality_state(directory)

    print(f"Arquivos: {state['total_files']} (high: {len(state['high_priority'])}, low: {len(state['low_priority'])})\n")

    # TODO: Processar todos os arquivos
    while state["files_to_scan"] or state["high_priority"] or state["low_priority"]:
        state = process_file_stage(state)

    # TODO: Gerar relatorio
    report = generate_quality_report(state)
    print(report)

    return state


# ============================================================================
# Testes (NAO MODIFIQUE)
# ============================================================================

def test_quality_pipeline():
    """Testa pipeline completo."""
    try:
        final_state = run_quality_pipeline("./sample_project")
        return final_state

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_quality_pipeline()
