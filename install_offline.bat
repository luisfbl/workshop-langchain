@echo off
REM Script de instalacao OFFLINE para Windows
REM Use este script quando NAO houver internet disponivel

echo ========================================
echo Workshop LangChain - Instalacao OFFLINE
echo ========================================
echo.

REM Verifica se a pasta packages existe
if not exist packages (
    echo [X] Pasta 'packages' nao encontrada!
    echo.
    echo Voce precisa copiar a pasta 'packages' com os pacotes baixados.
    echo Para criar essa pasta, execute 'download_packages.bat' em uma maquina com internet.
    pause
    exit /b 1
)

REM Verifica Python
echo [*] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python nao encontrado! Por favor, instale Python 3.9+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [+] Python %PYTHON_VERSION% encontrado

REM Remove venv antigo
if exist venv (
    echo [*] Removendo ambiente virtual antigo...
    rmdir /s /q venv
)

REM Cria ambiente virtual
echo [*] Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo [X] Erro ao criar ambiente virtual
    pause
    exit /b 1
)
echo [+] Ambiente virtual criado

REM Ativa ambiente virtual
echo [*] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualiza pip
echo [*] Atualizando pip...
python -m pip install --upgrade pip setuptools wheel --quiet
echo [+] pip atualizado

REM Instala dependencias OFFLINE
echo [*] Instalando dependencias da pasta 'packages'...
pip install --no-index --find-links=packages/ -r requirements.lock.txt

if errorlevel 1 (
    echo [X] Erro ao instalar dependencias
    pause
    exit /b 1
)
echo [+] Dependencias instaladas

REM Verifica instalacao
echo [*] Verificando instalacao...
python verify_install.py

REM Instrucoes finais
echo.
echo ========================================
echo [+] Instalacao OFFLINE concluida!
echo ========================================
echo.
echo Para ativar o ambiente virtual:
echo   venv\Scripts\activate.bat
echo.
echo Para executar o workshop:
echo   python main.py
echo.
pause
