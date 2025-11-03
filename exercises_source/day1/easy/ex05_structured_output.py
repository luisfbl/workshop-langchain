"""
Exercício 5 - Output Estruturado com Pydantic (EASY)
=====================================================

OBJETIVO: Fazer o agente retornar dados estruturados ao invés de texto livre.

TEMPO: 15 minutos

O QUE VOCÊ VAI APRENDER:
- O que é Pydantic e por que usar
- Criar models para estruturar dados
- Fazer LLM retornar JSON válido
- Validação automática de dados

CONTEXTO:
Até agora o agente retorna texto livre. Para workflows avançados,
precisamos de DADOS ESTRUTURADOS (JSON) que outras partes do sistema
possam processar facilmente.

IMPORTANTE: Este é o ÚLTIMO exercício básico de agentes!
"""

# I AM NOT DONE

from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.agents import create_agent, tool
from langchain_openai import ChatOpenAI
import ast
import json

# ============================================================================
# PARTE 1: Definir modelos Pydantic
# ============================================================================

class FunctionInfo(BaseModel):
    """Informações sobre uma função Python."""
    name: str = Field(description="Nome da função")
    args: List[str] = Field(description="Lista de argumentos")
    has_docstring: bool = Field(description="Se tem docstring")
    docstring: Optional[str] = Field(default=None, description="Conteúdo da docstring")


class FileAnalysis(BaseModel):
    """Análise estruturada de um arquivo Python."""
    file_name: str = Field(description="Nome do arquivo")
    file_path: str = Field(description="Caminho completo")
    total_lines: int = Field(description="Total de linhas")
    functions: List[FunctionInfo] = Field(description="Lista de funções")
    needs_documentation: bool = Field(description="Se precisa de docs")


# ============================================================================
# TODO 1: Criar tool que retorna JSON estruturado
# ============================================================================

@tool
def analyze_file_structured(file_path: str) -> str:
    """Analisa arquivo Python e retorna JSON estruturado.

    Use quando precisar de análise COMPLETA e ESTRUTURADA de um arquivo.
    Retorna JSON com todas as informações organizadas.

    Args:
        file_path: Caminho do arquivo Python

    Returns:
        JSON string com análise estruturada (modelo FileAnalysis)
    """
    try:
        # TODO 1.1: Ler e parsear arquivo com AST
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)

        # TODO 1.2: Contar linhas
        lines = content.split('\n')
        total_lines = len(lines)

        # TODO 1.3: Extrair funções usando AST
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # TODO: Criar FunctionInfo para cada função
                func_info = FunctionInfo(
                    name=None,  # TODO: node.name
                    args=None,  # TODO: [arg.arg for arg in node.args.args]
                    has_docstring=None,  # TODO: ast.get_docstring(node) is not None
                    docstring=None  # TODO: ast.get_docstring(node)
                )
                functions.append(func_info)

        # TODO 1.4: Criar análise estruturada
        # DICA: Precisa docs se alguma função não tem docstring
        needs_docs = any(not f.has_docstring for f in functions)

        analysis = FileAnalysis(
            file_name=Path(file_path).name,
            file_path=file_path,
            total_lines=total_lines,
            functions=functions,
            needs_documentation=needs_docs
        )

        # TODO 1.5: Retornar como JSON string
        # DICA: Use analysis.model_dump_json(indent=2)
        return None  # TODO: Retornar JSON

    except FileNotFoundError:
        return f"Erro: Arquivo '{file_path}' não encontrado."
    except SyntaxError as e:
        return f"Erro: Sintaxe inválida no arquivo Python - {str(e)}"
    except Exception as e:
        return f"Erro: {str(e)}"


# ============================================================================
# TODO 2: Criar agente que usa a tool estruturada
# ============================================================================

def create_structured_agent():
    """Cria agente com tool de análise estruturada usando LangChain 1.0+."""

    # TODO 2.1: Criar LLM
    llm = None  # TODO: ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # TODO 2.2: Lista de tools
    tools = []  # TODO: [analyze_file_structured]

    # TODO 2.3: Criar agente usando create_agent
    agent = None  # TODO: create_agent(llm, tools)

    return agent


# ============================================================================
# Testes (NÃO MODIFIQUE)
# ============================================================================

def test_structured_output():
    """Testa análise estruturada."""
    try:
        agent = create_structured_agent()

        # Histórico de mensagens para manter contexto
        messages = []

        print("=" * 70)
        print("TESTE 1: Análise estruturada")
        print("=" * 70)

        # Primeira pergunta
        messages.append({
            "role": "user",
            "content": "Analise o arquivo ./sample_project/calculator.py de forma estruturada"
        })

        response = agent.invoke({"messages": messages})
        messages = response['messages']  # Atualiza histórico

        last_msg = messages[-1].content
        print("\nResposta:")
        print(last_msg)

        print("\n" + "=" * 70)
        print("VALIDAÇÃO: Tentando parsear como JSON...")
        print("=" * 70)

        try:
            output = last_msg

            start = output.find('{')
            end = output.rfind('}') + 1

            if start != -1 and end > start:
                json_str = output[start:end]
                data = json.loads(json_str)

                print(f"\n📊 Dados extraídos:")
                print(f"  - Arquivo: {data.get('file_name')}")
                print(f"  - Linhas: {data.get('total_lines')}")
                print(f"  - Funções: {len(data.get('functions', []))}")
                print(f"  - Precisa docs: {data.get('needs_documentation')}")

                print(f"\n📝 Funções encontradas:")
                for func in data.get('functions', []):
                    status = "✓" if func.get('has_docstring') else "✗"
                    print(f"  {status} {func.get('name')}({', '.join(func.get('args', []))})")

            else:
                print("⚠️  JSON não encontrado na resposta")

        except json.JSONDecodeError as e:
            print(f"❌ JSON INVÁLIDO: {e}")

        print("\n" + "=" * 70)
        print("TESTE 2: Pergunta sobre dados estruturados (com histórico)")
        print("=" * 70)

        # Segunda pergunta com contexto
        messages.append({
            "role": "user",
            "content": "Quais funções não têm docstring?"
        })

        response2 = agent.invoke({"messages": messages})
        messages = response2['messages']

        print(f"\nResposta: {messages[-1].content}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_structured_output()
