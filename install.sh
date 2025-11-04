#!/bin/bash
# Script de instalação automatizada para Linux/Mac
# Instalação do Workshop LangChain

set -e  # Para na primeira falha

echo "========================================"
echo "Workshop LangChain - Instalação"
echo "========================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para mensagens
print_success() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[X]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[*]${NC} $1"
}

# 1. Verifica Python
print_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 não encontrado! Por favor, instale Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python $PYTHON_VERSION encontrado"

# Verifica versão mínima (3.9)
if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 9) else 1)'; then
    print_error "Python 3.9+ é necessário (encontrado: $PYTHON_VERSION)"
    exit 1
fi

# 2. Remove venv antigo se existir
if [ -d "venv" ]; then
    print_info "Removendo ambiente virtual antigo..."
    rm -rf venv
fi

# 3. Cria ambiente virtual
print_info "Criando ambiente virtual..."
python3 -m venv venv
print_success "Ambiente virtual criado"

# 4. Ativa ambiente virtual
print_info "Ativando ambiente virtual..."
source venv/bin/activate

# 5. Atualiza pip
print_info "Atualizando pip..."
python -m pip install --upgrade pip setuptools wheel --quiet
print_success "pip atualizado"

# 6. Instala dependências
print_info "Instalando dependências (isso pode demorar alguns minutos)..."
if [ -f "requirements.lock.txt" ]; then
    print_info "Usando requirements.lock.txt (versões fixas)"
    pip install -r requirements.lock.txt --quiet
else
    print_info "Usando requirements.txt"
    pip install -r requirements.txt --quiet
fi
print_success "Dependências instaladas"

# 7. Verifica instalação
print_info "Verificando instalação..."
python verify_install.py

# 8. Instruções finais
echo ""
echo "========================================"
print_success "Instalação concluída!"
echo "========================================"
echo ""
echo "Para ativar o ambiente virtual:"
echo "  source venv/bin/activate"
echo ""
echo "Para executar o workshop:"
echo "  python main.py"
echo ""
