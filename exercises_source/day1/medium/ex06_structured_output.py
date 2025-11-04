"""
Exercício 5 - Pydantic Avançado e Validações (MEDIUM)
======================================================

OBJETIVO: Dominar Pydantic para dados estruturados robustos.

TEMPO: 15 minutos

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
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import ast
import json

# ============================================================================
# TODO 1: Definir Models Pydantic Robustos
# ============================================================================

class FunctionInfo(BaseModel):
    """Informações detalhadas de uma função.

    TODO 1.1: Defina os campos necessários:
    - nome da função (string)
    - lista de argumentos (List[str])
    - se tem docstring (bool)
    - conteúdo da docstring (Optional[str], pode ser None)
    - número da linha onde está definida (int)
    - se é função privada, começa com _ mas não __ (bool, default=False)

    DICA: Use Field() com description para cada campo
    """
    # TODO: Adicione os campos aqui
    pass

    @field_validator('is_private', mode='before')
    @classmethod
    def check_private(cls, v, info: ValidationInfo):
        """Valida se função é privada baseado no nome.

        TODO 1.2: Implemente validação de função privada.

        Lógica:
        - Função é privada se nome começa com _ mas NÃO com __
        - Exemplos: _helper (privada), __init__ (não é privada), public (não é privada)

        DICA: Acessar outros campos via info.data.get('name', '')
        """
        name = info.data.get('name', '')
        # TODO: Retornar True se privada, False caso contrário
        pass


class ClassInfo(BaseModel):
    """Informações sobre uma classe.

    TODO 1.3: Defina os campos necessários:
    - nome da classe (string)
    - se tem docstring (bool)
    - conteúdo da docstring (Optional[str])
    - lista de nomes dos métodos (List[str])
    - número da linha de definição (int)
    """
    # TODO: Adicione os campos aqui
    pass


class FileAnalysis(BaseModel):
    """Análise completa e validada de um arquivo Python.

    TODO 1.4: Defina os campos necessários:
    - nome do arquivo (string)
    - caminho completo (string)
    - total de linhas (int)
    - linhas de código (int) - linhas não vazias e não comentário
    - lista de funções (List[FunctionInfo])
    - lista de classes (List[ClassInfo])
    - se precisa de documentação (bool)
    - score de documentação 0-100 (float)
    """
    # TODO: Adicione os campos aqui
    pass

    @field_validator('documentation_score', mode='before')
    @classmethod
    def calculate_score(cls, v, info: ValidationInfo):
        """Calcula score de documentação automaticamente.

        TODO 1.5: Implemente cálculo do score.

        Lógica:
        - Se não tem funções NEM classes: retornar 100.0
        - Caso contrário: calcular porcentagem de itens com docstring
        - Score = (itens_com_docs / total_itens) * 100

        DICA:
        - functions = info.data.get('functions', [])
        - classes = info.data.get('classes', [])
        - Conte quantos têm has_docstring == True
        """
        functions = info.data.get('functions', [])
        classes = info.data.get('classes', [])

        # TODO: Implemente o cálculo
        pass


# ============================================================================
# TODO 2: Criar tool de análise completa
# ============================================================================

@tool
def analyze_file_complete(file_path: str) -> str:
    """Analisa arquivo Python completamente e retorna JSON estruturado.

    TODO 2.1: Complete a docstring descrevendo o que a tool faz.

    Esta tool deve:
    - Analisar arquivo Python com AST
    - Extrair funções (com linha, args, docstring, se é privada)
    - Extrair classes (com métodos e docstring)
    - Calcular linhas de código
    - Retornar FileAnalysis como JSON
    """
    try:
        # TODO 2.2: Ler e parsear arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)

        # TODO 2.3: Contar linhas (total e código)
        lines = content.split('\n')
        total_lines = len(lines)

        # TODO: Contar linhas de código (não vazias e não são só comentários)
        # DICA: line.strip() and not line.strip().startswith('#')
        code_lines = 0

        # TODO 2.4: Extrair funções com TODOS os detalhes
        functions = []
        # TODO: Use ast.walk + isinstance(node, ast.FunctionDef)
        # Preencha TODOS os campos de FunctionInfo que você definiu:
        # - name: node.name
        # - args: [arg.arg for arg in node.args.args]
        # - has_docstring: ast.get_docstring(node) is not None
        # - docstring: ast.get_docstring(node)
        # - line_number: node.lineno
        # - is_private: será calculado pelo validator

        # TODO 2.5: Extrair classes com métodos
        classes = []
        # TODO: Use ast.walk + isinstance(node, ast.ClassDef)
        # Para cada classe, extraia:
        # - name: node.name
        # - has_docstring: ast.get_docstring(node) is not None
        # - docstring: ast.get_docstring(node)
        # - methods: [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
        # - line_number: node.lineno

        # TODO 2.6: Criar FileAnalysis
        # DICA: Os validators vão calcular automaticamente:
        # - is_private em cada FunctionInfo
        # - documentation_score em FileAnalysis
        analysis = None  # TODO: Criar FileAnalysis com todos os campos

        # TODO 2.7: Retornar como JSON
        # DICA: analysis.model_dump_json(indent=2)
        return None

    except Exception as e:
        return f"Erro: {str(e)}"


# ============================================================================
# TODO 3: DESAFIO OPCIONAL - Validação de qualidade
# ============================================================================

class CodeQuality(BaseModel):
    """DESAFIO EXTRA: Model para avaliar qualidade do código.

    TODO 3.1 (OPCIONAL): Defina os campos:
    - file_path (string)
    - documentation_score (float de 0-100)
    - complexity_score (float de 0-100) - baseado em nº funções/classes
    - overall_grade (string) - nota final "A", "B", "C", "D" ou "F"

    DICA: Use Field(ge=0, le=100) para limitar valores entre 0 e 100
    """
    # TODO: Adicione os campos aqui
    pass

    @field_validator('overall_grade', mode='before')
    @classmethod
    def calculate_grade(cls, v, info: ValidationInfo):
        """Calcula nota final baseado nos scores.

        TODO 3.2 (OPCIONAL): Implemente cálculo da nota.

        Lógica:
        - Calcule média de documentation_score e complexity_score
        - A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: <60
        """
        # TODO: Implementar
        pass


# ============================================================================
# TODO 4: Criar agente completo
# ============================================================================

def create_structured_agent():
    """Cria agente com tool de análise estruturada.

    TODO 4.1: Implemente o agente com:
    - ChatOpenAI (gpt-5-nano)
    - Tool analyze_file_complete
    - create_agent()
    """
    # TODO: Implementar
    pass


# ============================================================================
# Teste local (use para testar seu código)
# Use o comando `run` para executar o teste
# ============================================================================

def test_structured_output():
    try:
        agent = create_structured_agent()

        print("=" * 70)
        print("TESTE 1: Análise completa estruturada")
        print("=" * 70)
        response = agent.invoke({
            "messages": [{"role": "user", "content": "Analise completamente o arquivo ./sample_project/calculator.py"}]
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
            r = agent.invoke({
                "messages": [{"role": "user", "content": q}]
            })
            print(f"Resposta: {r['output']}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_structured_output()
