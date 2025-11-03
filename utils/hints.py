import time
from typing import Any, Dict, List, Optional, Tuple


HINTS = {
    1: {  # ex01_first_agent.py - Primeiro Agente
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Na API LangChain 1.0+, criar um agente é muito mais simples!\n"
            "Você só precisa de:\n"
            "1. Um LLM (ChatOpenAI)\n"
            "2. Uma lista de tools (pode ser vazia [])\n"
            "3. Chamar create_agent(llm, tools)\n\n"
            "📚 Documentação:\n"
            "https://docs.langchain.com/oss/python/langchain/agents\n"
            "https://docs.langchain.com/oss/python/langchain/quickstart"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para criar o LLM:\n"
            "- ChatOpenAI(model='gpt-5-nano', temperature=0)\n\n"
            "Para criar o agente (API 1.0+):\n"
            "- from langchain.agents import create_agent\n"
            "- tools = []  # lista vazia para este exercício\n"
            "- agent = create_agent(llm, tools)\n\n"
            "IMPORTANTE: Não precisa mais de AgentExecutor ou hub.pull()!\n\n"
            "📚 Docs: https://docs.langchain.com/oss/python/langchain/agents"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from langchain.agents import create_agent\n"
            "from langchain_openai import ChatOpenAI\n\n"
            "def create_llm():\n"
            "    return ChatOpenAI(\n"
            "        model='gpt-5-nano',\n"
            "        temperature=0\n"
            "    )\n\n"
            "def create_basic_agent():\n"
            "    llm = create_llm()\n"
            "    tools = []  # Sem tools neste exercício\n"
            "    agent = create_agent(llm, tools)\n"
            "    return agent\n"
            "```\n\n"
            "📚 Mais sobre agents: https://docs.langchain.com/oss/python/langchain/agents"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "from langchain.agents import create_agent\n"
            "from langchain_openai import ChatOpenAI\n\n"
            "def create_llm():\n"
            "    return ChatOpenAI(model='gpt-5-nano', temperature=0)\n\n"
            "def create_basic_agent():\n"
            "    llm = create_llm()\n"
            "    tools = []\n"
            "    agent = create_agent(llm, tools)\n"
            "    return agent\n\n"
            "# Para testar:\n"
            "# agent = create_basic_agent()\n"
            "# result = agent.invoke({\n"
            "#     'messages': [{'role': 'user', 'content': 'Olá!'}]\n"
            "# })\n"
            "# print(result['messages'][-1].content)\n"
            "```"
        ),
    },

    2: {  # ex02_first_tool.py - Primeira Tool
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Tools são funções Python que o agente pode chamar.\n"
            "Use o decorator @tool para transformar uma função em tool.\n"
            "A docstring é CRUCIAL - o LLM lê ela para saber quando usar a tool!\n\n"
            "📚 Documentação:\n"
            "https://docs.langchain.com/oss/python/langchain-core/tools\n"
            "https://python.langchain.com/docs/concepts/tools"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para criar a tool list_python_files:\n"
            "1. Use @tool decorator (from langchain_core.tools import tool)\n"
            "2. Use Path(directory).glob('*.py') para listar arquivos\n"
            "3. Retorne string formatada com os nomes\n\n"
            "Para criar o agente COM a tool:\n"
            "1. llm = ChatOpenAI(model='gpt-5-nano', temperature=0)\n"
            "2. tools = [list_python_files]  # Agora com a tool!\n"
            "3. agent = create_agent(llm, tools)\n\n"
            "📚 Docs: https://python.langchain.com/docs/concepts/tools"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from pathlib import Path\n"
            "from langchain_core.tools import tool\n\n"
            "@tool\n"
            "def list_python_files(directory: str) -> str:\n"
            "    \"\"\"Lista todos os arquivos Python (.py) em um diretório.\n"
            "    \n"
            "    Use esta ferramenta quando o usuário pedir para listar,\n"
            "    encontrar, ou ver quais arquivos Python existem.\n"
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
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "from langchain.agents import create_agent\n"
            "from langchain_core.tools import tool\n"
            "from langchain_openai import ChatOpenAI\n"
            "from pathlib import Path\n\n"
            "@tool\n"
            "def list_python_files(directory: str) -> str:\n"
            "    \"\"\"Lista todos os arquivos Python em um diretório.\"\"\"\n"
            "    path = Path(directory)\n"
            "    python_files = list(path.glob('*.py'))\n"
            "    if not python_files:\n"
            "        return f'Nenhum arquivo encontrado em {directory}'\n"
            "    return '\\n'.join([f'- {f.name}' for f in python_files])\n\n"
            "def create_agent_with_tool():\n"
            "    llm = ChatOpenAI(model='gpt-5-nano', temperature=0)\n"
            "    tools = [list_python_files]\n"
            "    agent = create_agent(llm, tools)\n"
            "    return agent\n"
            "```"
        ),
    },

    3: {  # ex03_memory.py - Memory e Context
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Na API LangChain 1.0+, memory é gerenciada pelo histórico de messages!\n"
            "Não precisa mais de ConversationBufferMemory.\n\n"
            "Como funciona:\n"
            "- Cada invoke() recebe {'messages': [...]}\n"
            "- Para manter memória, passe o histórico anterior + nova mensagem\n"
            "- O agente retorna {'messages': [...]} com todas as mensagens\n\n"
            "📚 Docs: https://docs.langchain.com/oss/python/langchain/agents"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para manter memória entre chamadas:\n\n"
            "1. Inicie com messages = []\n"
            "2. Para cada pergunta:\n"
            "   - Adicione a pergunta: messages.append({'role': 'user', 'content': '...'})\n"
            "   - Invoque: result = agent.invoke({'messages': messages})\n"
            "   - Atualize histórico: messages = result['messages']\n\n"
            "Dessa forma, o agente sempre vê todo o histórico!\n\n"
            "📚 Docs: https://docs.langchain.com/oss/python/langchain/agents"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "def chat_with_memory(agent, messages_history):\n"
            "    \"\"\"Envia mensagem mantendo histórico.\"\"\"\n"
            "    result = agent.invoke({'messages': messages_history})\n"
            "    return result['messages']\n\n"
            "# Uso:\n"
            "agent = create_agent_with_tools()\n"
            "messages = []\n\n"
            "# Primeira pergunta\n"
            "messages.append({'role': 'user', 'content': 'Analise calculator.py'})\n"
            "messages = chat_with_memory(agent, messages)\n"
            "print(messages[-1].content)\n\n"
            "# Segunda pergunta (com contexto!)\n"
            "messages.append({'role': 'user', 'content': 'Quantas funções ele tem?'})\n"
            "messages = chat_with_memory(agent, messages)\n"
            "print(messages[-1].content)  # Ele sabe qual arquivo!\n"
            "```"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "from langchain.agents import create_agent\n"
            "from langchain_core.tools import tool\n"
            "from langchain_openai import ChatOpenAI\n\n"
            "def create_agent_with_tools():\n"
            "    llm = ChatOpenAI(model='gpt-5-nano', temperature=0)\n"
            "    tools = [list_python_files, read_file, count_lines, get_file_info]\n"
            "    agent = create_agent(llm, tools)\n"
            "    return agent\n\n"
            "def chat_with_memory(agent, messages_history):\n"
            "    result = agent.invoke({'messages': messages_history})\n"
            "    return result['messages']\n\n"
            "# Testando com memória:\n"
            "agent = create_agent_with_tools()\n"
            "messages = []\n\n"
            "messages.append({'role': 'user', 'content': 'Analise ./sample_project/calculator.py'})\n"
            "messages = chat_with_memory(agent, messages)\n\n"
            "messages.append({'role': 'user', 'content': 'Quantas funções ele tem?'})\n"
            "messages = chat_with_memory(agent, messages)  # Contexto preservado!\n"
            "```"
        ),
    },

    4: {  # ex04_code_analyzer.py - Code Analyzer Especializado
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Um agente especializado tem um foco específico e ferramentas adaptadas.\n"
            "Para análise de qualidade de código, você precisa verificar:\n"
            "- Funções sem docstrings\n"
            "- Contagem de linhas de código\n"
            "- (MEDIUM) Type hints faltando\n"
            "- (MEDIUM) Complexidade ciclomática\n\n"
            "O módulo 'ast' é essencial para análise estática de Python!"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para EASY:\n"
            "1. check_docstrings(): Use ast.parse() + ast.walk() para encontrar FunctionDef\n"
            "2. Para cada função, use ast.get_docstring(node) para verificar se tem docstring\n"
            "3. count_lines(): Leia o arquivo e conte linhas (filtre vazias e comentários)\n\n"
            "Para MEDIUM:\n"
            "1. check_docstrings_and_types(): Verifique também node.returns e node.args\n"
            "2. calculate_complexity(): Conte if, for, while, except (+1 para cada)"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "import ast\n\n"
            "@tool\n"
            "def check_docstrings(file_path: str) -> str:\n"
            "    content = Path(file_path).read_text()\n"
            "    tree = ast.parse(content)\n"
            "    \n"
            "    functions_without_docs = []\n"
            "    for node in ast.walk(tree):\n"
            "        if isinstance(node, ast.FunctionDef):\n"
            "            if ast.get_docstring(node) is None:\n"
            "                functions_without_docs.append(node.name)\n"
            "    \n"
            "    if not functions_without_docs:\n"
            "        return 'Todas as funções têm docstrings!'\n"
            "    return f'Funções sem docstring: {functions_without_docs}'\n\n"
            "@tool\n"
            "def count_lines(file_path: str) -> str:\n"
            "    lines = Path(file_path).read_text().splitlines()\n"
            "    total = len(lines)\n"
            "    code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]\n"
            "    return f'Total: {total} linhas, Código: {len(code_lines)} linhas'\n"
            "```"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "def create_code_quality_analyzer(api_key: str) -> AgentExecutor:\n"
            "    # System message especializado\n"
            "    system_message = '''Você é um especialista em análise de qualidade de código Python.\n"
            "    Analise código e forneça feedback sobre docstrings, linhas de código, e sugestões.'''\n"
            "    \n"
            "    llm = ChatOpenAI(\n"
            "        model='gpt-5-nano',\n"
            "        temperature=0,\n"
            "        api_key=api_key\n"
            "    )\n"
            "    \n"
            "    prompt = hub.pull('hwchase17/react')\n"
            "    tools = [check_docstrings, count_lines]  # MEDIUM: +calculate_complexity\n"
            "    \n"
            "    agent = create_react_agent(llm, tools, prompt)\n"
            "    return AgentExecutor(agent=agent, tools=tools, verbose=True)\n"
            "```"
        ),
    },

    5: {  # ex05_structured_output.py - Saída Estruturada com Pydantic V2
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Pydantic V2 tem validators para validar e transformar dados automaticamente.\n"
            "Use @field_validator para criar validações customizadas.\n"
            "IMPORTANTE: Na V2, use ValidationInfo.data para acessar outros campos!\n\n"
            "📚 Documentação:\n"
            "https://docs.pydantic.dev/latest/concepts/validators/\n"
            "https://docs.pydantic.dev/latest/migration/"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para criar validators no Pydantic V2:\n\n"
            "1. from pydantic import field_validator\n"
            "2. from pydantic_core import ValidationInfo\n"
            "3. @field_validator('field_name', mode='before')\n"
            "4. Use @classmethod na função\n"
            "5. Use info.data.get('other_field') para acessar outros campos\n\n"
            "📚 Docs: https://docs.pydantic.dev/latest/concepts/validators/"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from pydantic import BaseModel, Field, field_validator\n"
            "from pydantic_core import ValidationInfo\n\n"
            "class FunctionInfo(BaseModel):\n"
            "    name: str\n"
            "    is_private: bool = False\n"
            "    \n"
            "    @field_validator('is_private', mode='before')\n"
            "    @classmethod\n"
            "    def check_private(cls, v, info: ValidationInfo):\n"
            "        # Acessar outros campos via info.data\n"
            "        name = info.data.get('name', '')\n"
            "        # Função é privada se começa com _ mas não com __\n"
            "        return name.startswith('_') and not name.startswith('__')\n"
            "```\n\n"
            "📚 Docs: https://docs.pydantic.dev/latest/concepts/validators/"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "from pydantic import BaseModel, Field, field_validator\n"
            "from pydantic_core import ValidationInfo\n\n"
            "class FileAnalysis(BaseModel):\n"
            "    file_name: str\n"
            "    functions: List[FunctionInfo]\n"
            "    classes: List[ClassInfo]\n"
            "    documentation_score: float = 0.0\n"
            "    \n"
            "    @field_validator('documentation_score', mode='before')\n"
            "    @classmethod\n"
            "    def calculate_score(cls, v, info: ValidationInfo):\n"
            "        functions = info.data.get('functions', [])\n"
            "        classes = info.data.get('classes', [])\n"
            "        \n"
            "        total = len(functions) + len(classes)\n"
            "        if total == 0:\n"
            "            return 100.0\n"
            "        \n"
            "        with_docs = sum(1 for f in functions if f.has_docstring)\n"
            "        with_docs += sum(1 for c in classes if c.has_docstring)\n"
            "        \n"
            "        return (with_docs / total) * 100\n"
            "```"
        ),
    },

    6: {  # ex06_langgraph_basics.py - Introdução ao LangGraph
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "LangGraph permite criar workflows com múltiplos steps (nodes).\n"
            "Cada node recebe o state, processa, e retorna campos atualizados.\n"
            "LangGraph faz merge automático do retorno com o state existente!\n\n"
            "📚 Documentação:\n"
            "https://docs.langchain.com/oss/python/langgraph/overview\n"
            "https://langchain-ai.github.io/langgraph/"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para criar um workflow com LangGraph:\n\n"
            "1. Defina o State com TypedDict\n"
            "2. Crie nodes (funções que recebem state e retornam dict)\n"
            "3. workflow = StateGraph(StateType)\n"
            "4. workflow.add_node('name', function)\n"
            "5. workflow.add_edge('node1', 'node2')\n"
            "6. graph = workflow.compile()\n\n"
            "📚 Docs: https://langchain-ai.github.io/langgraph/concepts/low_level/"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
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
            "💡 Dica 4 (Quase Solução):\n\n"
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

    7: {  # ex07_orchestrator.py - Orquestrador
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Um agente orquestrador coordena múltiplos sub-agentes.\n"
            "Cada sub-agente é especializado em uma tarefa.\n"
            "O orquestrador decide qual agente usar e como combinar resultados.\n\n"
            "Pense em como você dividiria um problema complexo entre especialistas."
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Crie:\n"
            "1. Um agente analisador (análise estática)\n"
            "2. Um agente testador (gera testes)\n"
            "3. Um agente documentador (gera docs)\n"
            "4. Um orquestrador que usa os três acima\n\n"
            "Use create_react_agent para cada sub-agente.\n"
            "O orquestrador pode ter ferramentas que chamam outros agentes!"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
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
            "💡 Dica 4 (Quase Solução):\n\n"
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
            "    return AgentExecutor(agent=agent, tools=tools, verbose=True)\n"
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
            warning = "⚠️  ATENÇÃO: Esta é a última dica! Tente resolver por conta própria primeiro.\n\n"
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
