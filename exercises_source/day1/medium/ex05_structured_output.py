"""
Exercício 5 - Pydantic Avançado e Validações (MEDIUM)
======================================================

OBJETIVO: Dominar Pydantic para dados estruturados robustos.

TEMPO: 20 minutos

O QUE VOCÊ VAI APRENDER:
- Pydantic models com validações
- Validators customizados
- Nested models (models dentro de models)
- Calcular campos derivados

CONTEXTO:
Vamos criar uma análise estruturada COMPLETA e ROBUSTA com Pydantic,
incluindo validações, scores calculados e estruturas aninhadas.
"""

# I AM NOT DONE

from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_core import ValidationInfo
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import ast
import json

# ============================================================================
# PARTE 1: Models Pydantic Robustos
# ============================================================================

class FunctionInfo(BaseModel):
    """Informações detalhadas de uma função."""
    name: str = Field(description="Nome da função")
    args: List[str] = Field(description="Argumentos da função")
    has_docstring: bool = Field(description="Se tem docstring")
    docstring: Optional[str] = Field(default=None, description="Conteúdo da docstring")
    line_number: int = Field(description="Linha onde está definida")
    is_private: bool = Field(default=False, description="Se é função privada (_func)")

    @field_validator('is_private', mode='before')
    @classmethod
    def check_private(cls, v, info: ValidationInfo):
        """TODO: Valida se função é privada baseado no nome."""
        # DICA: Função é privada se nome começa com _ mas não com __
        # Acessar outros campos via info.data
        name = info.data.get('name', '')
        # TODO: Retornar True se privada, False caso contrário
        pass


class ClassInfo(BaseModel):
    """Informações sobre uma classe."""
    name: str = Field(description="Nome da classe")
    has_docstring: bool = Field(description="Se tem docstring")
    docstring: Optional[str] = Field(default=None, description="Docstring")
    methods: List[str] = Field(description="Lista de métodos")
    line_number: int = Field(description="Linha de definição")


class FileAnalysis(BaseModel):
    """Análise completa e validada de um arquivo Python."""
    file_name: str = Field(description="Nome do arquivo")
    file_path: str = Field(description="Caminho completo")
    total_lines: int = Field(description="Total de linhas")
    code_lines: int = Field(description="Linhas de código")
    functions: List[FunctionInfo] = Field(description="Funções encontradas")
    classes: List[ClassInfo] = Field(description="Classes encontradas")
    needs_documentation: bool = Field(description="Se precisa de docs")
    documentation_score: float = Field(description="Score de 0-100")

    @field_validator('documentation_score', mode='before')
    @classmethod
    def calculate_score(cls, v, info: ValidationInfo):
        """
        TODO: Calcula score de documentação.

        Lógica:
        - Se não tem funções/classes: 100 (não precisa docs)
        - Caso contrário: (funções_com_docs / total) * 100
        """
        functions = info.data.get('functions', [])
        classes = info.data.get('classes', [])

        # TODO: Implemente o cálculo
        pass


# ============================================================================
# TODO 1: Criar tool de análise completa
# ============================================================================

@tool
def analyze_file_complete(file_path: str) -> str:
    """
    TODO: Docstring completa.

    Esta tool deve:
    - Analisar arquivo Python com AST
    - Extrair funções, classes, linhas
    - Retornar FileAnalysis como JSON
    """
    try:
        # TODO 1.1: Ler e parsear
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)

        # TODO 1.2: Contar linhas (total e código)
        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = 0  # TODO: Contar linhas não-vazias e não-comentário

        # TODO 1.3: Extrair funções com todos os detalhes
        functions = []
        # TODO: Use ast.walk + isinstance(node, ast.FunctionDef)
        # Preencha TODOS os campos de FunctionInfo

        # TODO 1.4: Extrair classes com métodos
        classes = []
        # TODO: Use ast.walk + isinstance(node, ast.ClassDef)
        # Extraia métodos de cada classe

        # TODO 1.5: Criar FileAnalysis (validators vão calcular automaticamente)
        analysis = FileAnalysis(
            file_name=Path(file_path).name,
            file_path=file_path,
            total_lines=total_lines,
            code_lines=code_lines,
            functions=functions,
            classes=classes,
            needs_documentation=False  # Será calculado automaticamente
        )

        return analysis.model_dump_json(indent=2)

    except Exception as e:
        return f"Erro: {str(e)}"


# ============================================================================
# TODO 2: DESAFIO - Validação de qualidade
# ============================================================================

class CodeQuality(BaseModel):
    """DESAFIO EXTRA: Model para avaliar qualidade do código."""
    file_path: str
    documentation_score: float = Field(ge=0, le=100)
    complexity_score: float = Field(ge=0, le=100, description="Baseado em nº de funções/classes")
    overall_grade: str = Field(description="A, B, C, D ou F")

    @field_validator('overall_grade', mode='before')
    @classmethod
    def calculate_grade(cls, v, info: ValidationInfo):
        """TODO: Calcular nota baseado nos scores."""
        # A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: <60
        pass


# ============================================================================
# TODO 3: Criar agente completo
# ============================================================================

def create_structured_agent():
    """
    TODO: Crie o agente completo com:
    - ChatOpenAI
    - ConversationBufferMemory
    - Tool analyze_file_complete
    - verbose=True
    """
    pass


# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_structured_output():
    try:
        agent = create_structured_agent()

        print("=" * 70)
        print("TESTE 1: Análise completa estruturada")
        print("=" * 70)
        response = agent.invoke({
            "input": "Analise completamente o arquivo ./sample_project/calculator.py"
        })

        print(f"\nResposta:\n{response['output']}\n")

        # Validar JSON
        print("=" * 70)
        print("VALIDAÇÃO DE ESTRUTURA")
        print("=" * 70)

        try:
            output = response['output']
            start = output.find('{')
            end = output.rfind('}') + 1
            json_str = output[start:end]
            data = json.loads(json_str)

            # Validar com Pydantic
            validated = FileAnalysis(**data)

            print(f"\n📊 Análise:")
            print(f"  Arquivo: {validated.file_name}")
            print(f"  Linhas: {validated.total_lines}")
            print(f"  Código: {validated.code_lines}")
            print(f"  Funções: {len(validated.functions)}")
            print(f"  Classes: {len(validated.classes)}")
            print(f"  Score de docs: {validated.documentation_score:.1f}%")
            print(f"  Precisa docs: {'Sim' if validated.needs_documentation else 'Não'}")

            print(f"\nDetalhes das funções:")
            for func in validated.functions:
                privacy = "🔒" if func.is_private else "🔓"
                docs = "✓" if func.has_docstring else "✗"
                print(f"  {privacy} {docs} {func.name} (linha {func.line_number})")

        except Exception as e:
            print(f"❌ Erro na validação: {e}")

        print("\n" + "=" * 70)
        print("TESTE 2: Perguntas sobre dados estruturados")
        print("=" * 70)

        questions = [
            "Qual o score de documentação?",
            "Quais funções são privadas?",
            "Quantas funções não têm docstring?"
        ]

        for q in questions:
            print(f"\nPergunta: {q}")
            r = agent.invoke({"input": q})
            print(f"Resposta: {r['output']}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_structured_output()
