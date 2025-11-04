#!/usr/bin/env python3
"""
Script de verificação de instalação
Verifica se todas as dependências necessárias estão instaladas
"""
import sys
import importlib.metadata

# Lista de pacotes necessários
REQUIRED_PACKAGES = [
    ("langchain", "1.0.0"),
    ("langchain-openai", "1.0.0"),
    ("langchain-core", "1.0.0"),
    ("langgraph", "1.0.0"),
    ("openai", "1.0.0"),
    ("pytest", "7.0.0"),
    ("watchdog", "3.0.0"),
    ("rich", "13.0.0"),
    ("pydantic", "2.0.0"),
    ("requests", "2.28.0"),
]

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print(f"\n[*] Verificando Python...")
    print(f"    Versão: {version.major}.{version.minor}.{version.micro}")

    if version < (3, 9):
        print(f"    [X] Python 3.9+ é necessário (você tem {version.major}.{version.minor})")
        return False

    print(f"    [+] Python OK")
    return True

def check_package(package_name, min_version):
    """Verifica se um pacote está instalado"""
    try:
        version = importlib.metadata.version(package_name)
        print(f"    [+] {package_name:20s} {version}")
        return True
    except importlib.metadata.PackageNotFoundError:
        print(f"    [X] {package_name:20s} NÃO INSTALADO")
        return False

def check_packages():
    """Verifica todos os pacotes necessários"""
    print(f"\n[*] Verificando pacotes Python...")

    all_ok = True
    for package, min_version in REQUIRED_PACKAGES:
        if not check_package(package, min_version):
            all_ok = False

    return all_ok

def check_imports():
    """Testa imports críticos"""
    print(f"\n[*] Testando imports críticos...")

    critical_imports = [
        "langchain",
        "langchain_openai",
        "langchain.agents",
        "langchain.tools",
        "langgraph.graph",
        "openai",
        "pydantic",
        "rich",
    ]

    all_ok = True
    for module in critical_imports:
        try:
            __import__(module)
            print(f"    [+] import {module}")
        except ImportError as e:
            print(f"    [X] import {module} - ERRO: {e}")
            all_ok = False

    return all_ok

def main():
    """Função principal"""
    print("=" * 60)
    print("Workshop LangChain - Verificação de Instalação")
    print("=" * 60)

    # Verifica Python
    python_ok = check_python_version()

    # Verifica pacotes
    packages_ok = check_packages()

    # Testa imports
    imports_ok = check_imports()

    # Resultado final
    print("\n" + "=" * 60)
    if python_ok and packages_ok and imports_ok:
        print("[+] TUDO OK! Instalação bem-sucedida")
        print("=" * 60)
        print("\nVocê está pronto para começar o workshop!")
        print("\nPróximos passos:")
        print("  1. Execute: python main.py")
        print("  2. Faça login ou crie uma conta")
        print("  3. Comece os exercícios!")
        return 0
    else:
        print("[X] PROBLEMAS ENCONTRADOS")
        print("=" * 60)
        print("\nAlgumas dependências não foram instaladas corretamente.")
        print("Tente executar novamente:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
