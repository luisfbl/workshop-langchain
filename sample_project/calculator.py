"""
Módulo de calculadora simples
Exemplo de código Python para análise
"""

import math
from typing import Union


def add(a: float, b: float) -> float:
    """Soma dois números.
    
    Args:
        a: Primeiro número
        b: Segundo número
        
    Returns:
        A soma de a e b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtrai dois números."""
    return a - b


def multiply(a: float, b: float) -> float:
    # Multiplica dois números (sem docstring!)
    return a * b


def divide(a: float, b: float) -> Union[float, str]:
    """Divide dois números.
    
    Args:
        a: Numerador
        b: Denominador
        
    Returns:
        Resultado da divisão ou mensagem de erro
    """
    if b == 0:
        return "Erro: divisão por zero"
    return a / b


def power(base: float, exponent: float) -> float:
    return math.pow(base, exponent)


def square_root(n: float) -> Union[float, str]:
    """Calcula a raiz quadrada de um número."""
    if n < 0:
        return "Erro: não é possível calcular raiz de número negativo"
    return math.sqrt(n)


class Calculator:
    """Classe calculadora com histórico de operações."""
    
    def __init__(self):
        """Inicializa a calculadora."""
        self.history = []
    
    def calculate(self, operation: str, a: float, b: float = None) -> float:
        # Executa operação (função sem docstring!)
        result = None
        
        if operation == "add" and b is not None:
            result = add(a, b)
        elif operation == "square_root":
            result = square_root(a)
        
        if result is not None:
            self.history.append(f"{operation}: {result}")
        
        return result
    
    def get_history(self) -> list:
        """Retorna o histórico de operações."""
        return self.history
