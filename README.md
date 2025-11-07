# LangChain Agents Workshop

Workshop prático para aprender a criar agentes de IA com LangChain e Python.

## Instalação

```bash
# Clone o repositório
git clone https://github.com/luisfbl/workshop-langchain
cd workshop-langchain

# Crie e ative ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
```

## Execução

```bash
# Inicie o workshop
python main.py

# Faça login ou registre-se
# O sistema irá:
# - Avaliar seu nível (fácil/médio)
# - Configurar exercícios apropriados
# - Iniciar o modo interativo

# Comandos disponíveis:
# help     - Ajuda
# status   - Seu progresso
# hint     - Dica do exercício atual
# test     - Roda testes
# run      - Executa exercício
# quit     - Sair
```

## Estrutura

```
exercises/           # Seus exercícios (copiados automaticamente)
  day1/             # Dia 1: Fundamentos
  day2/             # Dia 2: LangGraph
  tests/            # Testes automáticos
sample_project/     # Projeto exemplo para análise
```

## Workflow

1. Edite arquivo do exercício em `exercises/dayX/`
2. Remova `# I AM NOT DONE` quando terminar
3. Salve → testes executam automaticamente
4. Passe nos testes → próximo exercício desbloqueado
