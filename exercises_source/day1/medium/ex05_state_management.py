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
    complexity_score: float  # 0-10 (simplificado)
    quality_score: float  # 0-100


class QualityState(TypedDict):
    # Files to scan
    files_to_scan: list[str]
    files_scanned: list[str]

    # Current processing
    current_file: str

    # Individual metrics
    file_metrics: dict[str, FileMetrics]  # filepath -> metrics

    # Aggregated metrics
    total_files: int
    total_lines: int
    total_functions: int
    avg_quality_score: float

    # Errors and warnings
    errors: list[str]
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
    # TODO: Implementar
    # DICA: Conte nodes do tipo: If, For, While, ExceptHandler, With
    # Normalize para 0-10 (ex: min(decisions / 2, 10))

    complexity = 0

    # TODO: Implemente usando ast.walk()

    return min(complexity, 10.0)


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
    # TODO: Implementar formula de qualidade simplificada

    # Docstring coverage (60 pontos)
    docstring_score = 0
    if metrics.num_functions + metrics.num_classes > 0:
        total_items = metrics.num_functions + metrics.num_classes
        docstring_score = (metrics.functions_with_docstrings / total_items) * 60

    # Complexity (40 pontos - inverse: less is better)
    # TODO: Calcule complexity_points = (10 - metrics.complexity_score) * 4
    complexity_points = 0

    total_score = docstring_score + complexity_points

    return max(0, min(100, total_score))


def analyze_file(file_path: str) -> FileMetrics:
    """Analisa um arquivo e extrai todas as metricas.

    Args:
        file_path: Caminho do arquivo

    Returns:
        FileMetrics com todas as metricas
    """
    # TODO: Implementar analise completa

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        tree = ast.parse(content)

    # TODO: Conte funcoes, classes e docstrings usando ast.walk()
    num_functions = 0
    num_classes = 0
    functions_with_docstrings = 0

    # TODO: Implemente loop para contar
    # for node in ast.walk(tree):
    #     if isinstance(node, ast.FunctionDef):
    #         num_functions += 1
    #         if ast.get_docstring(node):
    #             functions_with_docstrings += 1
    #     elif isinstance(node, ast.ClassDef):
    #         num_classes += 1

    # TODO: Calcule complexidade chamando calculate_complexity(tree)
    complexity = 0  # TODO: calculate_complexity(tree)

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

    # TODO: Calcule quality score usando calculate_quality_score(metrics)
    metrics.quality_score = 0  # TODO: calculate_quality_score(metrics)

    return metrics


# ============================================================================
# TODO 3: Pipeline de processamento com State
# ============================================================================

def initialize_quality_state(directory: str) -> QualityState:
    """Inicializa state com lista de arquivos Python."""

    # TODO: Buscar arquivos Python no diretorio
    path = Path(directory)
    python_files = None  # TODO: [str(f) for f in path.glob("*.py")]

    # TODO: Criar state inicial
    state: QualityState = {
        "files_to_scan": python_files,
        "files_scanned": [],
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


def process_next_file(state: QualityState) -> QualityState:
    """Processa proximo arquivo e atualiza state.

    Args:
        state: State atual

    Returns:
        State atualizado
    """
    # TODO: Verificar se ha arquivos para processar
    if not state["files_to_scan"]:
        return state

    # TODO: Pegar proximo arquivo
    current = state["files_to_scan"][0]
    state["current_file"] = current

    print(f"\nAnalisando: {Path(current).name}")

    try:
        # TODO: Analisar arquivo chamando analyze_file()
        metrics = None  # TODO: analyze_file(current)

        # TODO: Adicionar metricas ao state
        # state["file_metrics"][current] = metrics

        # TODO: Atualizar agregados (total_lines, total_functions)
        # state["total_lines"] += metrics.lines_of_code
        # state["total_functions"] += metrics.num_functions

        # TODO: Adicionar warning se qualidade < 50
        # if metrics.quality_score < 50:
        #     state["warnings"].append(f"{Path(current).name}: Qualidade baixa")

        # TODO: Mover arquivo para scanned e remover de to_scan
        # state["files_scanned"].append(current)
        # state["files_to_scan"].pop(0)

        print(f"  Qualidade: {metrics.quality_score:.1f}/100")
        print(f"  Complexidade: {metrics.complexity_score:.1f}/10")

    except Exception as e:
        # TODO: Tratar erro
        # state["errors"].append(f"{current}: {str(e)}")
        # state["files_to_scan"].pop(0)
        print(f"  Erro: {e}")

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

    # TODO: Inicializar state
    state = None  # TODO: initialize_quality_state(directory)

    print(f"Arquivos encontrados: {state['total_files']}\n")

    # TODO: Processar todos os arquivos usando loop while
    # while state["files_to_scan"]:
    #     state = process_next_file(state)

    # Gerar relatorio
    report = generate_quality_report(state)
    print(report)

    return state


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
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
    _ = test_quality_pipeline()
