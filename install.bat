@echo off
REM Script de instalação automatizada para Windows
REM Instalação do Workshop LangChain

echo ========================================
echo Workshop LangChain - Instalacao
echo ========================================
echo.

REM 1. Verifica Python
echo [*] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python nao encontrado! Por favor, instale Python 3.9+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [+] Python %PYTHON_VERSION% encontrado

REM 2. Remove venv antigo se existir
if exist venv (
    echo [*] Removendo ambiente virtual antigo...
    rmdir /s /q venv
)

REM 3. Cria ambiente virtual
echo [*] Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo [X] Erro ao criar ambiente virtual
    pause
    exit /b 1
)
echo [+] Ambiente virtual criado

REM 4. Ativa ambiente virtual
echo [*] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM 5. Atualiza pip
echo [*] Atualizando pip...
python -m pip install --upgrade pip setuptools wheel --quiet
echo [+] pip atualizado

REM 6. Instala dependências
echo [*] Instalando dependencias (isso pode demorar alguns minutos)...
if exist requirements.lock.txt (
    echo [*] Usando requirements.lock.txt (versoes fixas)
    pip install -r requirements.lock.txt --quiet
) else (
    echo [*] Usando requirements.txt
    pip install -r requirements.txt --quiet
)
if errorlevel 1 (
    echo [X] Erro ao instalar dependencias
    pause
    exit /b 1
)
echo [+] Dependencias instaladas

REM 7. Verifica instalação
echo [*] Verificando instalacao...
python verify_install.py

REM 8. Instruções finais
echo.
echo ========================================
echo [+] Instalacao concluida!
echo ========================================
echo.
echo Para ativar o ambiente virtual:
echo   venv\Scripts\activate.bat
echo.
echo Para executar o workshop:
echo   python main.py
echo.
pause
