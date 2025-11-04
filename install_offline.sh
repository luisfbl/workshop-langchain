#!/bin/bash
# Script de instalação OFFLINE para Linux/Mac
# Use este script quando NÃO houver internet disponível

set -e

echo "========================================"
echo "Workshop LangChain - Instalação OFFLINE"
echo "========================================"
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() { echo -e "${GREEN}[+]${NC} $1"; }
print_error() { echo -e "${RED}[X]${NC} $1"; }
print_info() { echo -e "${YELLOW}[*]${NC} $1"; }

# Verifica se a pasta packages existe
if [ ! -d "packages" ]; then
    print_error "Pasta 'packages' não encontrada!"
    echo ""
    echo "Você precisa copiar a pasta 'packages' com os pacotes baixados."
    echo "Para criar essa pasta, execute 'download_packages.sh' em uma máquina com internet."
    exit 1
fi

# Verifica Python
print_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 não encontrado! Por favor, instale Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION encontrado"

# Remove venv antigo
if [ -d "venv" ]; then
    print_info "Removendo ambiente virtual antigo..."
    rm -rf venv
fi

# Cria ambiente virtual
print_info "Criando ambiente virtual..."
python3 -m venv venv
print_success "Ambiente virtual criado"

# Ativa ambiente virtual
print_info "Ativando ambiente virtual..."
source venv/bin/activate

# Atualiza pip (dos pacotes locais, se disponível)
print_info "Atualizando pip..."
if [ -f "packages/pip-"*.whl ]; then
    pip install --no-index --find-links=packages/ pip setuptools wheel
else
    python -m pip install --upgrade pip setuptools wheel --quiet
fi
print_success "pip atualizado"

# Instala dependências OFFLINE
print_info "Instalando dependências da pasta 'packages'..."
pip install --no-index --find-links=packages/ -r requirements.lock.txt

print_success "Dependências instaladas"

# Verifica instalação
print_info "Verificando instalação..."
python verify_install.py

# Instruções finais
echo ""
echo "========================================"
print_success "Instalação OFFLINE concluída!"
echo "========================================"
echo ""
echo "Para ativar o ambiente virtual:"
echo "  source venv/bin/activate"
echo ""
echo "Para executar o workshop:"
echo "  python main.py"
echo ""
