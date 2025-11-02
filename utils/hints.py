import time
from typing import Dict, List, Optional, Tuple

from google.cloud.firestore import Client


HINTS = {
    1: {  # ex01_first_agent.py - Primeiro Agente
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "O decorator @tool transforma uma função Python em uma ferramenta que o agente pode usar.\n"
            "O LLM lê a docstring da tool para entender quando e como usá-la.\n"
            "Pense: o agente precisa listar arquivos Python - que função Python faz isso?"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para listar arquivos Python:\n"
            "1. Use Path(directory_path).glob('*.py') para encontrar arquivos .py\n"
            "2. Retorne uma string formatada com os nomes dos arquivos\n\n"
            "Para criar o agente:\n"
            "1. ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=api_key)\n"
            "2. hub.pull('hwchase17/react') para buscar o prompt\n"
            "3. create_react_agent(llm, tools, prompt)\n"
            "4. AgentExecutor(agent=agent, tools=tools, verbose=True)"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from pathlib import Path\n\n"
            "@tool\n"
            "def list_python_files(directory_path: str) -> str:\n"
            "    path = Path(directory_path)\n"
            "    py_files = list(path.glob('*.py'))\n"
            "    if not py_files:\n"
            "        return f'Nenhum arquivo Python encontrado em {directory_path}'\n"
            "    return '\\n'.join([f.name for f in py_files])\n\n"
            "def create_file_explorer_agent(api_key: str):\n"
            "    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=api_key)\n"
            "    # Continue aqui...\n"
            "```"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "def create_file_explorer_agent(api_key: str) -> AgentExecutor:\n"
            "    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=api_key)\n"
            "    prompt = hub.pull('hwchase17/react')\n"
            "    tools = [list_python_files]\n"
            "    agent = create_react_agent(llm, tools, prompt)\n"
            "    agent_executor = AgentExecutor(\n"
            "        agent=agent,\n"
            "        tools=tools,\n"
            "        verbose=True,\n"
            "        handle_parsing_errors=True\n"
            "    )\n"
            "    return agent_executor\n"
            "```"
        ),
    },

    2: {  # ex02_code_reader.py - Múltiplas Tools - Code Reader
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Um agente pode ter múltiplas ferramentas e escolher qual usar baseado na tarefa.\n"
            "O agente ReAct vai primeiro listar os arquivos, depois ler o conteúdo.\n"
            "Cada ferramenta deve ter uma responsabilidade clara e bem definida."
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para read_file:\n"
            "1. Use Path(file_path).read_text() para ler o arquivo\n"
            "2. Adicione try/except para tratar FileNotFoundError\n"
            "3. Retorne mensagem clara se o arquivo não existir\n\n"
            "O agente precisa ter [list_python_files, read_file] na lista de tools.\n"
            "No nível MEDIUM, adicione também get_code_structure() usando ast.parse()."
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "@tool\n"
            "def read_file(file_path: str) -> str:\n"
            "    try:\n"
            "        content = Path(file_path).read_text()\n"
            "        return content\n"
            "    except FileNotFoundError:\n"
            "        return f'Arquivo não encontrado: {file_path}'\n\n"
            "# Para MEDIUM: análise com AST\n"
            "@tool\n"
            "def get_code_structure(file_path: str) -> str:\n"
            "    import ast\n"
            "    content = Path(file_path).read_text()\n"
            "    tree = ast.parse(content)\n"
            "    # Use ast.walk() para encontrar FunctionDef e ClassDef\n"
            "```"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "def create_code_reader_agent(api_key: str) -> AgentExecutor:\n"
            "    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=api_key)\n"
            "    prompt = hub.pull('hwchase17/react')\n"
            "    \n"
            "    # EASY: 2 tools\n"
            "    tools = [list_python_files, read_file]\n"
            "    \n"
            "    # MEDIUM: 3 tools\n"
            "    # tools = [list_python_files, read_file, get_code_structure]\n"
            "    \n"
            "    agent = create_react_agent(llm, tools, prompt)\n"
            "    return AgentExecutor(agent=agent, tools=tools, verbose=True)\n"
            "```"
        ),
    },

    3: {  # ex03_memory.py - Memory e Context
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Sem memória, cada pergunta ao agente é independente - ele não lembra de nada.\n"
            "ConversationBufferMemory (EASY) guarda TODO o histórico.\n"
            "ConversationBufferWindowMemory (MEDIUM) guarda apenas as últimas K interações.\n"
            "Isso é crucial para conversas que precisam de contexto!"
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Para EASY (ConversationBufferMemory):\n"
            "1. from langchain.memory import ConversationBufferMemory\n"
            "2. memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)\n"
            "3. Passe memory= para o AgentExecutor\n\n"
            "Para MEDIUM (Window Memory):\n"
            "1. from langchain.memory import ConversationBufferWindowMemory\n"
            "2. memory = ConversationBufferWindowMemory(k=3, memory_key='chat_history', return_messages=True)\n"
            "3. k=3 significa que mantém apenas as 3 últimas interações"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from langchain.memory import ConversationBufferMemory\n"
            "# ou para MEDIUM:\n"
            "# from langchain.memory import ConversationBufferWindowMemory\n\n"
            "def create_code_reader_with_memory(api_key: str):\n"
            "    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=api_key)\n"
            "    prompt = hub.pull('hwchase17/react')\n"
            "    tools = [list_python_files, read_file]\n"
            "    \n"
            "    # EASY:\n"
            "    memory = ConversationBufferMemory(\n"
            "        memory_key='chat_history',\n"
            "        return_messages=True\n"
            "    )\n"
            "    \n"
            "    # MEDIUM:\n"
            "    # memory = ConversationBufferWindowMemory(\n"
            "    #     k=3,\n"
            "    #     memory_key='chat_history',\n"
            "    #     return_messages=True\n"
            "    # )\n"
            "    \n"
            "    agent = create_react_agent(llm, tools, prompt)\n"
            "    # Adicione memory= aqui\n"
            "```"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "def create_code_reader_with_memory(api_key: str) -> AgentExecutor:\n"
            "    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=api_key)\n"
            "    prompt = hub.pull('hwchase17/react')\n"
            "    tools = [list_python_files, read_file]\n"
            "    \n"
            "    memory = ConversationBufferMemory(\n"
            "        memory_key='chat_history',\n"
            "        return_messages=True\n"
            "    )\n"
            "    \n"
            "    agent = create_react_agent(llm, tools, prompt)\n"
            "    \n"
            "    return AgentExecutor(\n"
            "        agent=agent,\n"
            "        tools=tools,\n"
            "        memory=memory,  # <<< A diferença está aqui!\n"
            "        verbose=True\n"
            "    )\n"
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
            "        model='gpt-4o-mini',\n"
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

    5: {  # ex05_structured_output.py - Saída Estruturada
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Pydantic permite definir schemas para as respostas do LLM.\n"
            "Em vez de texto livre, você recebe objetos Python tipados.\n"
            "Isso é CRUCIAL para integração com sistemas reais."
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Use with_structured_output() do LangChain:\n"
            "1. Defina uma classe Pydantic com os campos que você quer\n"
            "2. Use model.with_structured_output(SuaClasse)\n"
            "3. O LLM retornará uma instância da sua classe\n\n"
            "Docs: https://python.langchain.com/docs/modules/model_io/output_parsers/"
        ),
        3: (
            "💡 Dica 3 (Estrutural):\n\n"
            "```python\n"
            "from pydantic import BaseModel, Field\n\n"
            "class CodeReview(BaseModel):\n"
            "    score: int = Field(description='Score de 1-10')\n"
            "    issues: list[str] = Field(description='Lista de problemas')\n"
            "    suggestions: list[str]\n\n"
            "llm = ChatOpenAI(model='gpt-4')\n"
            "structured_llm = llm.with_structured_output(CodeReview)\n"
            "```"
        ),
        4: (
            "💡 Dica 4 (Quase Solução):\n\n"
            "```python\n"
            "def create_structured_reviewer():\n"
            "    llm = ChatOpenAI(model='gpt-4', temperature=0)\n"
            "    structured_llm = llm.with_structured_output(CodeReview)\n"
            "    \n"
            "    def review_code(code: str) -> CodeReview:\n"
            "        prompt = f'Review this code:\\n{code}'\n"
            "        return structured_llm.invoke(prompt)\n"
            "    \n"
            "    return review_code\n"
            "```"
        ),
    },

    6: {  # ex06_generator.py - Gerador de Código
        1: (
            "💡 Dica 1 (Conceitual):\n\n"
            "Um agente gerador de código combina:\n"
            "- Saída estruturada (Pydantic)\n"
            "- Validação de código gerado\n"
            "- Iteração até obter código válido\n\n"
            "Pense em como validar se o código gerado é sintaticamente correto."
        ),
        2: (
            "💡 Dica 2 (Direcional):\n\n"
            "Use ast.parse() para validar sintaxe Python.\n"
            "Crie um loop que:\n"
            "1. Gera código com LLM\n"
            "2. Tenta fazer parse com ast.parse()\n"
            "3. Se falhar, pede ao LLM para corrigir\n"
            "4. Repete até obter código válido (max 3 tentativas)"
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
    firebase: Client
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
