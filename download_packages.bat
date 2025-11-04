@echo off
REM Script para baixar todos os pacotes para instalacao offline (Windows)

echo ========================================
echo Download de Pacotes para Instalacao Offline
echo ========================================
echo.

REM Cria diretorio para pacotes
if not exist packages mkdir packages

echo [*] Baixando pacotes...
pip download -r requirements.lock.txt -d packages/

if errorlevel 1 (
    echo.
    echo [X] Erro ao baixar pacotes
    pause
    exit /b 1
)

echo.
echo [+] Download concluido!
echo.
echo Pasta 'packages' criada com todos os arquivos necessarios.
echo.
echo Para distribuir:
echo   1. Copie esta pasta 'packages' para as maquinas sem internet
echo   2. Copie tambem 'install_offline.bat' (Windows)
echo   3. Execute o script de instalacao offline
echo.

REM Cria arquivo com informacoes
echo Pacotes baixados em: %date% %time% > packages\README.txt
echo Total de arquivos: >> packages\README.txt
dir /b packages\*.whl packages\*.tar.gz 2>nul | find /c /v "" >> packages\README.txt

echo Informacoes da pasta packages:
type packages\README.txt
echo.
pause
