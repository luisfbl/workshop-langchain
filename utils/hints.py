import time
from typing import Any, Dict, List, Optional, Tuple


HINTS = {
    1: {  # ex01_first_agent.py - Primeiro Agente
        1: (
            " Dica 1 (Conceitual):\n\n"
            "Na API LangChain 1.0+, criar um agente é muito mais simples!\n"
            "Você só precisa de:\n"
            "1. Um LLM (ChatOpenAI)\n"
            "2. Uma lista de tools (pode ser vazia [])\n"
            "3. Chamar create_agent(llm, tools)\n\n"
            "O agente retorna um CompiledStateGraph que você usa com .invoke()\n\n"
            " EASY vs MEDIUM:\n"
            "- EASY: Foco em completar os TODOs com instruções detalhadas\n"
            "- MEDIUM: Implementar do zero com menos orientação\n\n"
            " Documentação:\n"
            "https://docs.langchain.com/oss/python/langchain/agents"
        ),
        2: (
            " Dica 2 (Direcional):\n\n"
            "Para create_llm():\n"
            "- Importe: from langchain_openai import ChatOpenAI\n"
            "- Crie: ChatOpenAI(model='gpt-5-nano', temperature=0)\n"
            "- Retorne o objeto criado\n\n"
            "Para create_basic_agent():\n"
            "- Importe: from langchain.agents import create_agent\n"
            "- Chame create_llm() para obter o LLM\n"
            "- Crie tools = [] (lista vazia neste exercício)\n"
            "- Chame: create_agent(llm, tools)\n"
            "- Retorne o agente\n\n"
            "IMPORTANTE: Não precisa mais de AgentExecutor ou hub.pull()!"
        ),
        3: (
            " Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from langchain.agents import create_agent\n"
            "from langchain_openai import ChatOpenAI\n\n"
            "def create_llm():\n"
            "    # TODO: Crie e retorne ChatOpenAI\n"
            "    return ChatOpenAI(\n"
            "        model='gpt-5-nano',\n"
            "        temperature=0\n"
            "    )\n\n"
            "def create_basic_agent():\n"
            "    # Passo 1: Criar LLM\n"
            "    llm = create_llm()\n"
            "    \n"
            "    # Passo 2: Lista de tools (vazia neste ex)\n"
            "    tools = []\n"
            "    \n"
            "    # Passo 3: Criar agente\n"
            "    agent = create_agent(llm, tools)\n"
            "    \n"
            "    return agent\n"
            "```"
        ),
        4: (
            " Dica 4 (Solução Completa):\n\n"
            "```python\n"
            "from langchain.agents import create_agent\n"
            "from langchain_openai import ChatOpenAI\n\n"
            "def create_llm():\n"
            "    return ChatOpenAI(model='gpt-5-nano', temperature=0)\n\n"
            "def create_basic_agent():\n"
            "    llm = create_llm()\n"
            "    tools = []\n"
            "    agent = create_agent(llm, tools)\n"
            "    return agent\n"
            "```\n\n"
            "Para testar:\n"
            "```python\n"
            "agent = create_basic_agent()\n"
            "result = agent.invoke({\n"
            "    'messages': [{'role': 'user', 'content': 'Olá! Qual é a capital do Brasil?'}]\n"
            "})\n"
            "print(result['messages'][-1].content)\n"
            "```"
        ),
    },

    2: {  # ex02_first_tool.py - Primeira Tool
        1: (
            " Dica 1 (Conceitual):\n\n"
            "Tools são funções Python que o agente pode chamar.\n"
            "Use o decorator @tool para transformar uma função em tool.\n\n"
            "A docstring é CRUCIAL - o LLM lê ela para decidir quando usar a tool!\n"
            "Seja específico sobre QUANDO usar a ferramenta.\n\n"
            " EASY vs MEDIUM:\n"
            "- EASY: Complete a tool list_python_files e retorne string formatada\n"
            "- MEDIUM: Implemente com tratamento de erros robusto\n\n"
            " Documentação:\n"
            "https://python.langchain.com/docs/concepts/tools"
        ),
        2: (
            " Dica 2 (Direcional):\n\n"
            "Para list_python_files:\n"
            "1. Importe: from langchain.tools import tool\n"
            "2. Importe: from pathlib import Path\n"
            "3. Use decorator @tool\n"
            "4. Escreva docstring clara\n"
            "5. Use Path(directory).glob('*.py') para buscar\n"
            "6. Formate resultado: 'Encontrei X arquivos:\\n- file1.py\\n- file2.py'\n\n"
            "Para create_agent_with_tool:\n"
            "1. Crie LLM: ChatOpenAI(model='gpt-5-nano', temperature=0)\n"
            "2. Crie lista tools = [list_python_files]\n"
            "3. Crie agente: create_agent(llm, tools)\n"
            "4. Retorne o agente"
        ),
        3: (
            " Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from pathlib import Path\n"
            "from langchain.tools import tool\n\n"
            "@tool\n"
            "def list_python_files(directory: str) -> str:\n"
            "    \"\"\"Lista todos os arquivos Python (.py) em um diretório.\n"
            "    \n"
            "    Use esta ferramenta quando o usuário pedir para listar,\n"
            "    encontrar, ou ver quais arquivos Python existem em um diretório.\n"
            "    \"\"\"\n"
            "    path = Path(directory)\n"
            "    python_files = list(path.glob('*.py'))\n"
            "    \n"
            "    if not python_files:\n"
            "        return f'Nenhum arquivo Python encontrado em {directory}'\n"
            "    \n"
            "    result = f'Encontrei {len(python_files)} arquivos:\\n'\n"
            "    for f in python_files:\n"
            "        result += f'- {f.name}\\n'\n"
            "    return result\n"
            "```"
        ),
        4: (
            " Dica 4 (Solução Completa):\n\n"
            "```python\n"
            "from langchain.agents import create_agent\n"
            "from langchain.tools import tool\n"
            "from langchain_openai import ChatOpenAI\n"
            "from pathlib import Path\n\n"
            "@tool\n"
            "def list_python_files(directory: str) -> str:\n"
            "    \"\"\"Lista todos os arquivos Python (.py) em um diretório.\n"
            "    \n"
            "    Use quando o usuário pedir para listar, encontrar,\n"
            "    ou ver quais arquivos Python existem.\n"
            "    \"\"\"\n"
            "    path = Path(directory)\n"
            "    python_files = list(path.glob('*.py'))\n"
            "    \n"
            "    if not python_files:\n"
            "        return f'Nenhum arquivo Python encontrado em {directory}'\n"
            "    \n"
            "    result = f'Encontrei {len(python_files)} arquivos:\\n'\n"
            "    for f in python_files:\n"
            "        result += f'- {f.name}\\n'\n"
            "    return result\n\n"
            "def create_agent_with_tool():\n"
            "    llm = ChatOpenAI(model='gpt-5-nano', temperature=0)\n"
            "    tools = [list_python_files]\n"
            "    agent = create_agent(llm, tools)\n"
            "    return agent\n"
            "```"
        ),
    },

    3: {  # ex04_memory.py ou ex03_multiple_tools.py (depende do nível)
        # EASY: ex03_multiple_tools (3 tools), ex04_memory (RunnableWithMessageHistory)
        # MEDIUM: ex03_multiple_tools (3 tools robustas), ex04_memory (SessionStore avançado)
        1: (
            " Dica 1 (Conceitual):\n\n"
            "EASY - ex03_multiple_tools:\n"
            "- Crie 3 tools: list_python_files, read_file, count_lines\n"
            "- O agente vai escolher qual tool usar baseado na pergunta\n\n"
            "EASY - ex04_memory:\n"
            "- Use RunnableWithMessageHistory para gerenciar conversas\n"
            "- Crie store = {} e função get_session_history(session_id)\n"
            "- Cada sessão tem seu próprio histórico de mensagens\n\n"
            "MEDIUM - ex04_memory:\n"
            "- Crie SessionStore com metadados (created_at, last_accessed)\n"
            "- Implemente trimming de mensagens antigas\n"
            "- Adicione estatísticas de uso\n\n"
            " Docs: https://python.langchain.com/docs/concepts/chat_history"
        ),
        2: (
            " Dica 2 (Direcional):\n\n"
            "Para ex03_multiple_tools (EASY):\n"
            "- read_file: use open(file_path, 'r') e retorne conteúdo\n"
            "- count_lines: conte linhas ignorando vazias e comentários\n"
            "- Crie agente com tools = [list_python_files, read_file, count_lines]\n\n"
            "Para ex04_memory (EASY):\n"
            "1. store = {}\n"
            "2. def get_session_history(session_id):\n"
            "       if session_id not in store:\n"
            "           store[session_id] = InMemoryChatMessageHistory()\n"
            "       return store[session_id]\n"
            "3. chat_with_history = RunnableWithMessageHistory(\n"
            "       runnable=llm,\n"
            "       get_session_history=get_session_history,\n"
            "       input_messages_key='input',\n"
            "       history_messages_key='chat_history'\n"
            "   )"
        ),
        3: (
            " Dica 3 (Estrutural):\n\n"
            "ex03_multiple_tools (read_file):\n"
            "```python\n"
            "@tool\n"
            "def read_file(file_path: str) -> str:\n"
            "    \"\"\"Lê e retorna o conteúdo completo de um arquivo.\"\"\"\n"
            "    try:\n"
            "        with open(file_path, 'r', encoding='utf-8') as f:\n"
            "            return f.read()\n"
            "    except FileNotFoundError:\n"
            "        return f'Erro: Arquivo {file_path} não encontrado'\n"
            "```\n\n"
            "ex04_memory (EASY):\n"
            "```python\n"
            "from langchain_core.chat_history import InMemoryChatMessageHistory\n"
            "from langchain_core.runnables.history import RunnableWithMessageHistory\n\n"
            "store = {}\n\n"
            "def get_session_history(session_id: str):\n"
            "    if session_id not in store:\n"
            "        store[session_id] = InMemoryChatMessageHistory()\n"
            "    return store[session_id]\n\n"
            "def create_chat_with_history():\n"
            "    llm = ChatOpenAI(model='gpt-5-nano', temperature=0)\n"
            "    return RunnableWithMessageHistory(\n"
            "        runnable=llm,\n"
            "        get_session_history=get_session_history,\n"
            "        input_messages_key='input',\n"
            "        history_messages_key='chat_history'\n"
            "    )\n"
            "```"
        ),
        4: (
            " Dica 4 (Solução):\n\n"
            "ex03_multiple_tools - count_lines:\n"
            "```python\n"
            "@tool\n"
            "def count_lines(file_path: str) -> str:\n"
            "    \"\"\"Conta linhas de código ignorando vazias e comentários.\"\"\"\n"
            "    try:\n"
            "        with open(file_path, 'r', encoding='utf-8') as f:\n"
            "            lines = f.readlines()\n"
            "        code_lines = 0\n"
            "        for line in lines:\n"
            "            stripped = line.strip()\n"
            "            if stripped and not stripped.startswith('#'):\n"
            "                code_lines += 1\n"
            "        return f'O arquivo tem {code_lines} linhas de código.'\n"
            "    except FileNotFoundError:\n"
            "        return f'Erro: Arquivo não encontrado.'\n"
            "```\n\n"
            "ex04_memory - função chat:\n"
            "```python\n"
            "def chat(chat_with_history, session_id: str, message: str) -> str:\n"
            "    response = chat_with_history.invoke(\n"
            "        {'input': message},\n"
            "        config={'configurable': {'session_id': session_id}}\n"
            "    )\n"
            "    return response.content\n"
            "```"
        ),
    },

    4: {  # ex05_state_management.py - State Management
        1: (
            " Dica 1 (Conceitual):\n\n"
            "State Management é diferente de Memory:\n"
            "- MEMORY: Histórico de conversas (mensagens)\n"
            "- STATE: Dados estruturados que mudam durante um workflow\n\n"
            "EASY - State Management:\n"
            "- Defina AnalysisState com TypedDict\n"
            "- Crie funções que recebem e retornam state\n"
            "- Trackeia arquivos processados, contadores, erros\n\n"
            "MEDIUM - State Management Avançado:\n"
            "- State com métricas de qualidade (complexidade, docstrings)\n"
            "- Pipeline com múltiplas etapas\n"
            "- Sistema de prioridades\n"
            "- Relatórios agregados\n\n"
            " Docs: https://docs.python.org/3/library/typing.html#typing.TypedDict"
        ),
        2: (
            " Dica 2 (Direcional):\n\n"
            "EASY - Estrutura do State:\n"
            "```python\n"
            "class AnalysisState(TypedDict):\n"
            "    files_to_process: list[str]\n"
            "    files_processed: list[str]\n"
            "    current_file: str\n"
            "    total_functions: int\n"
            "    total_lines: int\n"
            "    errors: list[str]\n"
            "```\n\n"
            "Funções principais:\n"
            "1. initialize_state(directory) -> AnalysisState\n"
            "2. process_next_file(state) -> AnalysisState\n"
            "3. get_state_summary(state) -> str\n\n"
            "MEDIUM - Adicione:\n"
            "- calculate_complexity(tree: ast.AST) -> float\n"
            "- calculate_quality_score(metrics) -> float\n"
            "- Sistema de prioridades (high_priority, low_priority)"
        ),
        3: (
            " Dica 3 (Estrutural):\n\n"
            "EASY - process_next_file:\n"
            "```python\n"
            "def process_next_file(state: AnalysisState) -> AnalysisState:\n"
            "    if not state['files_to_process']:\n"
            "        return state\n"
            "    \n"
            "    current = state['files_to_process'][0]\n"
            "    state['current_file'] = current\n"
            "    \n"
            "    try:\n"
            "        with open(current, 'r') as f:\n"
            "            content = f.read()\n"
            "            tree = ast.parse(content)\n"
            "        \n"
            "        # Contar funções\n"
            "        num_functions = sum(1 for node in ast.walk(tree) \n"
            "                           if isinstance(node, ast.FunctionDef))\n"
            "        \n"
            "        # Contar linhas\n"
            "        num_lines = len(content.split('\\n'))\n"
            "        \n"
            "        # Atualizar state\n"
            "        state['total_functions'] += num_functions\n"
            "        state['total_lines'] += num_lines\n"
            "        state['files_processed'].append(current)\n"
            "        state['files_to_process'].pop(0)\n"
            "    \n"
            "    except Exception as e:\n"
            "        state['errors'].append(f'{current}: {str(e)}')\n"
            "        state['files_to_process'].pop(0)\n"
            "    \n"
            "    return state\n"
            "```"
        ),
        4: (
            " Dica 4 (Solução - Loop Principal):\n\n"
            "```python\n"
            "def run_analysis_workflow(directory: str) -> AnalysisState:\n"
            "    # Inicializar\n"
            "    state = initialize_state(directory)\n"
            "    \n"
            "    print(f'Encontrados {len(state[\"files_to_process\"])} arquivos')\n"
            "    \n"
            "    # Processar todos os arquivos\n"
            "    while state['files_to_process']:\n"
            "        state = process_next_file(state)\n"
            "    \n"
            "    # Mostrar resumo\n"
            "    print(get_state_summary(state))\n"
            "    \n"
            "    return state\n"
            "```\n\n"
            "MEDIUM - Pipeline com estágios:\n"
            "```python\n"
            "# Estado inclui: current_stage: 'scan' | 'analyze' | 'report'\n"
            "while state['files_to_scan'] or state['high_priority']:\n"
            "    state = process_file_stage(state)  # Processa um arquivo por vez\n"
            "```"
        ),
    },

    5: {  # ex06_structured_output.py - Saída Estruturada com Pydantic
        1: (
            " Dica 1 (Conceitual):\n\n"
            "Pydantic permite criar dados estruturados e validados.\n"
            "Use BaseModel para definir a estrutura de dados.\n\n"
            "EASY - Pydantic Básico:\n"
            "- Defina FunctionInfo com campos: name, args, has_docstring, docstring\n"
            "- Defina FileAnalysis com funções, linhas, needs_documentation\n"
            "- Use Field(description='...') para documentar campos\n"
            "- Retorne JSON com model.model_dump_json()\n\n"
            "MEDIUM - Pydantic Avançado:\n"
            "- Use @field_validator para validações automáticas\n"
            "- Calcule campos derivados (is_private, documentation_score)\n"
            "- ValidationInfo.data para acessar outros campos\n"
            "- Nested models (FunctionInfo dentro de FileAnalysis)\n\n"
            " Docs: https://docs.pydantic.dev/latest/"
        ),
        2: (
            " Dica 2 (Direcional):\n\n"
            "EASY - Estrutura Básica:\n"
            "```python\n"
            "from pydantic import BaseModel, Field\n\n"
            "class FunctionInfo(BaseModel):\n"
            "    name: str = Field(description='Nome da função')\n"
            "    args: list[str] = Field(description='Lista de argumentos')\n"
            "    has_docstring: bool\n"
            "    docstring: str | None = None\n"
            "```\n\n"
            "MEDIUM - Com Validators:\n"
            "```python\n"
            "from pydantic import field_validator, ValidationInfo\n\n"
            "class FunctionInfo(BaseModel):\n"
            "    name: str\n"
            "    is_private: bool = False\n"
            "    \n"
            "    @field_validator('is_private', mode='before')\n"
            "    @classmethod\n"
            "    def check_private(cls, v, info: ValidationInfo):\n"
            "        name = info.data.get('name', '')\n"
            "        return name.startswith('_') and not name.startswith('__')\n"
            "```"
        ),
        3: (
            " Dica 3 (Estrutural):\n\n"
            "EASY - Tool com Pydantic:\n"
            "```python\n"
            "@tool\n"
            "def analyze_file_structured(file_path: str) -> str:\n"
            "    with open(file_path, 'r') as f:\n"
            "        content = f.read()\n"
            "        tree = ast.parse(content)\n"
            "    \n"
            "    functions = []\n"
            "    for node in ast.walk(tree):\n"
            "        if isinstance(node, ast.FunctionDef):\n"
            "            func_info = FunctionInfo(\n"
            "                name=node.name,\n"
            "                args=[arg.arg for arg in node.args.args],\n"
            "                has_docstring=ast.get_docstring(node) is not None,\n"
            "                docstring=ast.get_docstring(node)\n"
            "            )\n"
            "            functions.append(func_info)\n"
            "    \n"
            "    analysis = FileAnalysis(\n"
            "        file_name=Path(file_path).name,\n"
            "        file_path=file_path,\n"
            "        total_lines=len(content.split('\\n')),\n"
            "        functions=functions,\n"
            "        needs_documentation=any(not f.has_docstring for f in functions)\n"
            "    )\n"
            "    \n"
            "    return analysis.model_dump_json(indent=2)\n"
            "```"
        ),
        4: (
            " Dica 4 (Solução - Validator Avançado):\n\n"
            "MEDIUM - Validator de Documentation Score:\n"
            "```python\n"
            "class FileAnalysis(BaseModel):\n"
            "    file_name: str\n"
            "    functions: list[FunctionInfo]\n"
            "    classes: list[ClassInfo]\n"
            "    documentation_score: float = 0.0\n"
            "    \n"
            "    @field_validator('documentation_score', mode='before')\n"
            "    @classmethod\n"
            "    def calculate_score(cls, v, info: ValidationInfo):\n"
            "        functions = info.data.get('functions', [])\n"
            "        classes = info.data.get('classes', [])\n"
            "        \n"
            "        total_items = len(functions) + len(classes)\n"
            "        if total_items == 0:\n"
            "            return 100.0\n"
            "        \n"
            "        # Conta itens com docstring\n"
            "        with_docs = 0\n"
            "        for func in functions:\n"
            "            if func.has_docstring:\n"
            "                with_docs += 1\n"
            "        for cls in classes:\n"
            "            if cls.has_docstring:\n"
            "                with_docs += 1\n"
            "        \n"
            "        return (with_docs / total_items) * 100\n"
            "```"
        ),
    },

    6: {  # ex07_langgraph_basics.py - Introdução ao LangGraph
        1: (
            " Dica 1 (Conceitual):\n\n"
            "LangGraph permite criar workflows com múltiplos steps (nodes).\n"
            "Cada node recebe o state, processa, e retorna campos atualizados.\n"
            "LangGraph faz merge automático do retorno com o state existente!\n\n"
            " Documentação:\n"
            "https://docs.langchain.com/oss/python/langgraph/overview\n"
            "https://langchain-ai.github.io/langgraph/"
        ),
        2: (
            " Dica 2 (Direcional):\n\n"
            "Para criar um workflow com LangGraph:\n\n"
            "1. Defina o State com TypedDict\n"
            "2. Crie nodes (funções que recebem state e retornam dict)\n"
            "3. workflow = StateGraph(StateType)\n"
            "4. workflow.add_node('name', function)\n"
            "5. workflow.add_edge('node1', 'node2')\n"
            "6. graph = workflow.compile()\n\n"
            " Docs: https://langchain-ai.github.io/langgraph/concepts/low_level/"
        ),
        3: (
            " Dica 3 (Estrutural):\n\n"
            "```python\n"
            "class GeneratedCode(BaseModel):\n"
            "    code: str\n"
            "    explanation: str\n"
            "    test_cases: list[str]\n\n"
            "def generate_and_validate(prompt: str, max_attempts: int = 3):\n"
            "    for attempt in range(max_attempts):\n"
            "        result = structured_llm.invoke(prompt)\n"
            "        try:\n"
            "            ast.parse(result.code)\n"
            "            return result  # Código válido!\n"
            "        except SyntaxError:\n"
            "            # Ajustar prompt e tentar novamente\n"
            "```"
        ),
        4: (
            " Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "def create_code_generator():\n"
            "    llm = ChatOpenAI(model='gpt-4', temperature=0.7)\n"
            "    structured_llm = llm.with_structured_output(GeneratedCode)\n"
            "    \n"
            "    def generate(description: str) -> GeneratedCode:\n"
            "        for i in range(3):\n"
            "            result = structured_llm.invoke(\n"
            "                f'Generate Python code: {description}'\n"
            "            )\n"
            "            try:\n"
            "                ast.parse(result.code)\n"
            "                return result\n"
            "            except SyntaxError as e:\n"
            "                if i == 2:\n"
            "                    raise\n"
            "        return result\n"
            "    return generate\n"
            "```"
        ),
    },

    7: {  # ex08_orchestrator.py - Orquestrador
        1: (
            " Dica 1 (Conceitual):\n\n"
            "Um agente orquestrador coordena múltiplos sub-agentes.\n"
            "Cada sub-agente é especializado em uma tarefa.\n"
            "O orquestrador decide qual agente usar e como combinar resultados.\n\n"
            "Pense em como você dividiria um problema complexo entre especialistas."
        ),
        2: (
            " Dica 2 (Direcional):\n\n"
            "Crie:\n"
            "1. Um agente analisador (análise estática)\n"
            "2. Um agente testador (gera testes)\n"
            "3. Um agente documentador (gera docs)\n"
            "4. Um orquestrador que usa os três acima\n\n"
            "Use create_react_agent para cada sub-agente.\n"
            "O orquestrador pode ter ferramentas que chamam outros agentes!"
        ),
        3: (
            " Dica 3 (Estrutural):\n\n"
            "```python\n"
            "# Criar sub-agentes\n"
            "analyzer_agent = create_analyzer_agent()\n"
            "tester_agent = create_tester_agent()\n"
            "doc_agent = create_doc_agent()\n\n"
            "# Criar ferramentas que usam sub-agentes\n"
            "@tool\n"
            "def analyze_code(code: str) -> str:\n"
            "    return analyzer_agent.invoke({'input': code})\n\n"
            "# Orquestrador usa essas ferramentas\n"
            "orchestrator_tools = [analyze_code, test_code, document_code]\n"
            "```"
        ),
        4: (
            " Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "def create_orchestrator():\n"
            "    # Sub-agentes\n"
            "    analyzer = create_analyzer_agent()\n"
            "    tester = create_tester_agent()\n"
            "    \n"
            "    @tool\n"
            "    def analyze(code: str) -> str:\n"
            "        return analyzer.invoke({'input': code})['output']\n"
            "    \n"
            "    @tool\n"
            "    def test(code: str) -> str:\n"
            "        return tester.invoke({'input': code})['output']\n"
            "    \n"
            "    tools = [analyze, test]\n"
            "    llm = ChatOpenAI(model='gpt-4', temperature=0)\n"
            "    prompt = hub.pull('hwchase17/react')\n"
            "    agent = create_react_agent(llm, tools, prompt)\n"
            "    return AgentExecutor(agent=agent, tools=tools, debug=True)\n"
            "```"
        ),
    },
}

RATE_LIMIT_SECONDS = 60

class HintManager:
    firebase: Any  # FirebaseClient
    user_id: str
    last_hint_time: dict[int, float]

    def __init__(self, firebase_client, user_id: str):
        self.firebase = firebase_client
        self.user_id = user_id
        self.last_hint_time = {}

    def get_next_hint(self, exercise_num: int) -> Tuple[bool, str, int]:
        if not self._check_rate_limit(exercise_num):
            remaining = self._get_remaining_time(exercise_num)
            return False, f"Por favor, aguarde {remaining}s antes de pedir outra dica.", 0

        progress = self.firebase.get_progress(self.user_id)
        hints_used = progress.get("hints_used", {})

        # Firebase pode retornar lista ao invés de dict quando chaves são números consecutivos
        if isinstance(hints_used, list):
            hints_used = {str(i): item for i, item in enumerate(hints_used) if item is not None}

        exercise_hints = hints_used.get(str(exercise_num), [])

        next_level = len(exercise_hints) + 1

        if next_level > 4:
            return False, "Você já usou todas as 4 dicas disponíveis para este exercício.", 4

        if exercise_num not in HINTS:
            return False, f"Dicas não disponíveis para exercício {exercise_num}.", 0

        hint_text = HINTS[exercise_num].get(next_level, "")
        if not hint_text:
            return False, f"Dica nível {next_level} não encontrada.", 0

        self.firebase.add_hint_used(self.user_id, exercise_num, next_level)
        self.last_hint_time[exercise_num] = time.time()

        header = f"\n{'='*60}\n"
        footer = f"\n{'='*60}\n\n"

        if next_level == 4:
            warning = "  ATENÇÃO: Esta é a última dica! Tente resolver por conta própria primeiro.\n\n"
            hint_text = warning + hint_text

        full_hint = header + hint_text + footer

        return True, full_hint, next_level

    def _check_rate_limit(self, exercise_num: int) -> bool:
        if exercise_num not in self.last_hint_time:
            return True

        elapsed = time.time() - self.last_hint_time[exercise_num]
        return elapsed >= RATE_LIMIT_SECONDS

    def _get_remaining_time(self, exercise_num: int) -> int:
        if exercise_num not in self.last_hint_time:
            return 0

        elapsed = time.time() - self.last_hint_time[exercise_num]
        remaining = max(0, int(RATE_LIMIT_SECONDS - elapsed))
        return remaining

    def get_hint_stats(self) -> Dict[int, List[int]]:
        progress = self.firebase.get_progress(self.user_id)
        hints_used = progress.get("hints_used", {})

        # Firebase pode retornar lista ao invés de dict quando chaves são números consecutivos
        if isinstance(hints_used, list):
            hints_used = {str(i): item for i, item in enumerate(hints_used) if item is not None}

        stats = {}
        for ex_str, levels in hints_used.items():
            stats[int(ex_str)] = levels

        return stats

    def format_hint_summary(self, exercise_num: int) -> str:
        stats = self.get_hint_stats()
        hints = stats.get(exercise_num, [])

        if not hints:
            return f"Exercício {exercise_num}: Nenhuma dica usada ainda. Você tem 4 dicas disponíveis."

        used = len(hints)
        remaining = 4 - used

        summary = f"Exercício {exercise_num}:\n"
        summary += f"   Dicas usadas: {used}/4\n"
        summary += f"   Dicas restantes: {remaining}\n"
        summary += f"   Níveis usados: {hints}"

        return summary
