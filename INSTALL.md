# Guia de Instalação - Workshop LangChain

Este guia fornece várias opções de instalação otimizadas para workshops com múltiplas máquinas.

## Opções de Instalação

### Opção 1: Instalação Automática (COM INTERNET) ⚡ MAIS RÁPIDO

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
install.bat
```

Isso irá:
- ✓ Verificar Python 3.9+
- ✓ Criar ambiente virtual
- ✓ Instalar todas as dependências
- ✓ Verificar instalação

---

### Opção 2: Instalação Offline (SEM INTERNET) 📦 PARA 40 MÁQUINAS

**Passo 1: Preparação (em 1 máquina COM internet)**

Linux/Mac:
```bash
chmod +x download_packages.sh
./download_packages.sh
```

Windows:
```cmd
download_packages.bat
```

Isso irá criar uma pasta `packages/` com todos os arquivos necessários (~300MB).

**Passo 2: Distribuição**

1. Copie para um pendrive ou compartilhamento de rede:
   - A pasta `packages/`
   - O arquivo `install_offline.sh` (Linux/Mac) ou `install_offline.bat` (Windows)
   - O arquivo `requirements.lock.txt`
   - O arquivo `verify_install.py`

2. Distribua para as 40 máquinas

**Passo 3: Instalação (em cada máquina SEM internet)**

Linux/Mac:
```bash
chmod +x install_offline.sh
./install_offline.sh
```

Windows:
```cmd
install_offline.bat
```

---

### Opção 3: Instalação Manual

Se preferir controle total:

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate.bat

# 3. Atualizar pip
python -m pip install --upgrade pip

# 4. Instalar dependências
pip install -r requirements.lock.txt

# 5. Verificar instalação
python verify_install.py
```

---

## Requisitos do Sistema

- **Python**: 3.9 ou superior
- **Sistema Operacional**: Windows 10+, Linux, ou macOS
- **Espaço em disco**: ~500MB para dependências
- **RAM**: 4GB mínimo (8GB recomendado)
- **Internet**: Apenas para Opção 1

---

## Verificação de Instalação

Após qualquer instalação, execute:

```bash
python verify_install.py
```

Você deve ver:
```
========================================
Workshop LangChain - Verificação de Instalação
========================================

[*] Verificando Python...
    [+] Python OK

[*] Verificando pacotes Python...
    [+] langchain          1.0.3
    [+] langchain-openai   1.0.2
    [+] langgraph          1.0.2
    ...

[+] TUDO OK! Instalação bem-sucedida
```

---

## Solução de Problemas

### Erro: "Python não encontrado"
**Solução**: Instale Python 3.9+ de https://python.org

### Erro: "pip não reconhecido"
**Solução**:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Erro: "Permission denied" (Linux/Mac)
**Solução**:
```bash
chmod +x install.sh
```

### Erro: Dependências não instalam
**Solução**: Use a instalação offline (Opção 2)

### Erro: Versões conflitantes
**Solução**: Use `requirements.lock.txt` em vez de `requirements.txt`

---

## Estratégia para 40 Máquinas

### Recomendação: Instalação Offline

1. **Preparação (1x)**:
   - Execute `download_packages.sh` em 1 máquina com internet
   - Tempo: ~5-10 minutos

2. **Distribuição**:
   - Copie a pasta `packages/` para compartilhamento de rede ou pendrives
   - Tempo: Variável

3. **Instalação (40x em paralelo)**:
   - Cada aluno executa `install_offline.bat` ou `install_offline.sh`
   - Tempo por máquina: ~2-3 minutos
   - **Tempo total: ~5 minutos** (se todos instalarem simultaneamente)

### Alternativa: Clonagem

1. Configure 1 máquina completamente
2. Clone o disco ou crie imagem
3. Restaure nas 40 máquinas
4. **Tempo total: Depende da infraestrutura**

---

## Próximos Passos

Após instalação bem-sucedida:

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat # Windows

# Executar o workshop
python main.py
```

---

## Suporte

Se encontrar problemas durante a instalação:

1. Execute `python verify_install.py` para diagnóstico
2. Verifique os logs de erro
3. Tente a instalação offline se a online falhar
4. Para workshops, considere ter a pasta `packages/` como backup

---

## Arquivos de Instalação

- `install.sh` / `install.bat` - Instalação automática online
- `install_offline.sh` / `install_offline.bat` - Instalação offline
- `download_packages.sh` / `download_packages.bat` - Download para offline
- `verify_install.py` - Verificação de instalação
- `requirements.txt` - Dependências (versões flexíveis)
- `requirements.lock.txt` - Dependências (versões fixas)
