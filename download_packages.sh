#!/bin/bash
# Script para baixar todos os pacotes para instalação offline
# Execute este script em uma máquina com internet e depois distribua a pasta 'packages'

echo "========================================"
echo "Download de Pacotes para Instalação Offline"
echo "========================================"
echo ""

# Cria diretório para pacotes
mkdir -p packages

echo "[*] Baixando pacotes..."
pip download -r requirements.lock.txt -d packages/

if [ $? -eq 0 ]; then
    echo ""
    echo "[+] Download concluído!"
    echo ""
    echo "Pasta 'packages' criada com todos os arquivos necessários."
    echo ""
    echo "Para distribuir:"
    echo "  1. Copie esta pasta 'packages' para as máquinas sem internet"
    echo "  2. Copie também 'install_offline.sh' (Linux/Mac) ou 'install_offline.bat' (Windows)"
    echo "  3. Execute o script de instalação offline"
    echo ""

    # Cria arquivo com informações
    echo "Pacotes baixados em: $(date)" > packages/README.txt
    echo "Total de arquivos: $(ls packages/*.whl packages/*.tar.gz 2>/dev/null | wc -l)" >> packages/README.txt
    echo "Tamanho total: $(du -sh packages/ | cut -f1)" >> packages/README.txt

    echo "Informações da pasta packages:"
    cat packages/README.txt
else
    echo ""
    echo "[X] Erro ao baixar pacotes"
    exit 1
fi
