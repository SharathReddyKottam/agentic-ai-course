# Agentic AI System Design Course

## 📚 Module 1: Environment Setup & Agent Fundamentals

Welcome to the Agentic AI System Design course! This guide walks you through setting up your development environment and understanding the core concepts of agentic AI systems.

---

## 🎯 Learning Objectives

By the end of this module, you will:

1. Set up a professional Python development environment with Poetry
2. Configure LangChain, LangGraph, and OpenAI integration
3. Understand how agents reason and act (ReAct loop)
4. Build and run your first working agent
5. Learn to use tools and extend agent capabilities

---

## 📋 Part 1: Prerequisites & Environment Setup

### What You'll Need

Before we begin, ensure your system has:

- **Python 3.11 or 3.12** — The runtime for our applications
- **Git** — For version control and collaboration
- **An OpenAI API key** — To access GPT-4o mini model
- **A code editor** — VS Code or Cursor recommended

### Verify Your Setup

Check Python version:
```bash
python3 --version
# Expected output: Python 3.11.x or 3.12.x
```

Check Git installation:
```bash
git --version
# Expected output: git version 2.x.x or higher
```

If either is missing, download from:
- Python: https://www.python.org/downloads/
- Git: https://git-scm.com/

### Get Your OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-`)
4. Store it safely — you'll use it next

⚠️ **Important:** Never share your API key publicly. Treat it like a password.

---

## 🚀 Part 2: Project Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/SharathReddyKottam/agentic-ai-course.git
cd agentic-ai-course
```

This creates a local copy of the course materials on your machine.

### Step 2: Install Poetry

Poetry is a Python package manager that creates isolated environments for your projects. Think of it as a virtual bubble where your project's dependencies live separately from your system Python.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify installation:
```bash
poetry --version
# Expected: Poetry (version 2.4.x or higher)
```

If the command isn't found, add Poetry to your PATH:

**For macOS/Linux (add to `~/.zshrc` or `~/.bash_profile`):**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then restart your terminal.

### Step 3: Install Project Dependencies

Poetry reads the `pyproject.toml` file to understand what your project needs, then installs everything in an isolated environment.

```bash
poetry install
```

This installs:
- **LangChain** — Framework for building LLM applications
- **LangGraph** — State management and workflow orchestration
- **langchain-openai** — OpenAI model integration
- **python-dotenv** — Environment variable management

### Step 4: Configure Your OpenAI API Key

Create a `.env` file in your project root:

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-key-here
EOF
```

Replace `sk-your-actual-key-here` with your actual OpenAI key.

**File location:** `agentic-ai-course/.env`

**Why `.env`?** This file stores sensitive information locally. It's already added to `.gitignore`, which means Git will never track it. This prevents your API key from accidentally being pushed to GitHub.

### Step 5: Verify Your Setup

Run the setup verification script:

```bash
poetry run python verify_setup.py
```

**Expected output:**
```
✓ API key loaded: sk-proj-...

✅ Setup verified! Agent response:

Hello, Alex! Welcome to the Agentic AI System Design course.

The sum of 128 and 256 is 384.

--- Message trace (shows the ReAct loop steps) ---
  [HumanMessage   ] Please greet me — my name is Alex. Also, what is 128 + 256?
  [AIMessage      ]
  [ToolMessage    ] Hello, Alex! Welcome to the Agentic AI System Design course.
  [ToolMessage    ] The sum of 128.0 and 256.0 is 384.0
  [AIMessage      ] Hello, Alex! Welcome to the Agentic AI System Design course...
```

If you see this, **congratulations!** Your environment is ready. 🎉

---

## 💡 Part 3: Understanding the Core Concepts

### What is an Agent?

An **agent** is a software system powered by an LLM that can:

- **Perceive** the world through user input and tool results
- **Reason** about problems and plan solutions
- **Act** by calling tools or functions
- **Learn** from feedback and adapt its behavior

**Real-world analogy:** Think of a travel agent. You tell them where you want to go, and they:
1. Reason about the best route
2. Act by checking flights, hotels, and transportation
3. Observe the results
4. Present you with options

An AI agent works similarly, but with code.

### The ReAct Loop (Reasoning + Acting)

The foundation of agentic AI is the **ReAct pattern**, which creates a continuous loop:

```
1. REASON: "The user asked for a greeting and a calculation."
2. ACT: Call tool greet_user("Alex") and tool add_numbers(128, 256)
3. OBSERVE: Get results back
4. REASON: "I have both pieces of information."
5. RESPOND: "Hello, Alex!... The sum is 384."
```

You can see this loop in action in the message trace from `verify_setup.py`.

### Key Components

#### 1. **Language Model (LLM)**
The "brain" of the agent. In this course, we use GPT-4o mini from OpenAI.
- Reads user queries
- Plans which tools to use
- Synthesizes tool results into a response

#### 2. **Tools**
Functions that the agent can call to gather information or take action.
- Must have a clear name and description
- Accept inputs (parameters)
- Return outputs (results)

Example tools:
```python
@tool
def add_numbers(a: float, b: float) -> str:
    """Add two numbers together."""
    return f"Result: {a + b}"

@tool
def search_web(query: str) -> str:
    """Search the internet for information."""
    # Would call a search API
    return search_results

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    # Would integrate with email service
    return "Email sent successfully"
```

#### 3. **Memory**
Keeps track of the conversation history so the agent maintains context across multiple interactions.

#### 4. **Executor**
The runtime that orchestrates the reasoning and acting loop, managing tool calls and responses.

---

## 🔍 Part 4: Dissecting verify_setup.py

Let's walk through the verification script line-by-line to understand how everything works together.

### Loading Dependencies and API Key

```python
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

# Load OPENAI_API_KEY from .env
load_dotenv()

# Debug: print if key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    exit(1)
else:
    print(f"✓ API key loaded: {api_key[:10]}...")
```

**What's happening:**
1. Import required libraries
2. `load_dotenv()` reads the `.env` file and loads environment variables
3. `os.getenv("OPENAI_API_KEY")` retrieves the key
4. Print confirmation (showing only first 10 characters for security)

### Defining Tools

```python
@tool
def add_numbers(a: float, b: float) -> str:
    """Add two numbers together and return the result."""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def greet_user(name: str) -> str:
    """Greet a user by their name."""
    return f"Hello, {name}! Welcome to the Agentic AI System Design course."
```

**What's happening:**
1. `@tool` decorator tells LangChain "this function is a tool the agent can use"
2. The docstring (triple quotes) is critical — the LLM reads this to understand what the tool does
3. The function signature (parameters and return type) tells the LLM what inputs it needs

**Why docstrings matter:**
The LLM can't see your code logic. It only sees:
```
Tool: greet_user
Description: Greet a user by their name.
Parameters: name (string)
Returns: string
```

Based on this, it decides whether and when to call the tool.

### Creating the Agent

```python
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[add_numbers, greet_user],
    system_prompt="You are a helpful assistant. Use the tools available to you.",
)
```

**What's happening:**
1. `model="openai:gpt-4o-mini"` — Use OpenAI's GPT-4o mini model (fast and cheap)
2. `tools=[add_numbers, greet_user]` — Register available tools
3. `system_prompt` — Give the LLM instructions on how to behave

The agent now knows:
- Which model to use for reasoning
- Which tools are available
- How to behave toward the user

### Running the Agent (The ReAct Loop)

```python
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Please greet me — my name is Alex. Also, what is 128 + 256?"
    }]
})
```

**What happens internally:**

1. **LLM Reasoning:** GPT-4o mini reads: "User wants a greeting with name 'Alex' and a sum calculation."

2. **Tool Selection:** LLM decides to call both `greet_user` and `add_numbers`

3. **Tool Execution:** 
   - Calls `greet_user("Alex")` → Returns "Hello, Alex! Welcome..."
   - Calls `add_numbers(128, 256)` → Returns "The sum is 384"

4. **Synthesis:** LLM combines tool results into a coherent response

5. **Output:** Returns the complete message

### Displaying the Results

```python
print("\n✅ Setup verified! Agent response:\n")
print(result["messages"][-1].content)

print("\n--- Message trace (shows the ReAct loop steps) ---")
for msg in result["messages"]:
    print(f"  [{type(msg).__name__:15s}] {str(msg.content)[:80]}")
```

**What's happening:**
1. `result["messages"][-1]` gets the last message (the agent's final response)
2. `.content` extracts the text
3. Loop through all messages to show the entire reasoning process

---

## 📊 Part 5: Project Structure & File Organization

### Understanding the Layout

```
agentic-ai-course/
├── .env                           # Your OpenAI API key (SECRET - not in Git)
├── .gitignore                     # Tells Git which files to ignore
├── .git/                          # Git version control metadata
├── README.md                      # Project documentation
├── pyproject.toml                 # Project configuration & dependencies
├── poetry.lock                    # Locked dependency versions
├── verify_setup.py                # Setup verification script
├── src/
│   └── agentic_ai_course/
│       └── __init__.py            # Makes this a Python package
└── tests/
    └── __init__.py                # Test package marker
```

### Key Files Explained

#### `.env` (Environment Variables)
**Purpose:** Store sensitive configuration
**Content:**
```
OPENAI_API_KEY=sk-proj-...
```
**Important:** Never commit to Git. Already in `.gitignore`.

#### `.gitignore` (Git Configuration)
**Purpose:** Tell Git which files to ignore
**Content:**
```
.env
.venv/
__pycache__/
*.pyc
*.pyo
.pytest_cache/
*.egg-info/
.DS_Store
.ipynb_checkpoints/
```

#### `pyproject.toml` (Project Configuration)
**Purpose:** Define project metadata and dependencies
**Content includes:**
- Project name, version, description
- Python version requirement: `>=3.11,<4.0.0`
- Dependencies: LangChain, LangGraph, etc.

**Example:**
```toml
[project]
name = "agentic-ai-course"
version = "0.1.0"
requires-python = ">=3.11,<4.0.0"
dependencies = [
    "langchain>=1.4.0",
    "langchain-openai>=1.6.2",
    "langgraph>=1.2.11",
    "python-dotenv>=1.2.3",
]
```

#### `poetry.lock` (Dependency Lock File)
**Purpose:** Ensure everyone uses the exact same versions
**Why it matters:** If you don't lock versions, different machines might install different versions, causing "works on my machine" problems.

**Example content:**
```
[[package]]
name = "langchain"
version = "1.4.0"
description = "Building applications with LLMs"
```

#### `verify_setup.py` (Verification Script)
**Purpose:** Test that all components work together
**When to run:** After setup, or to debug issues

---

## 🎓 Part 6: Key Concepts Deep Dive

### Tools: The Agent's Hands and Eyes

Tools are the mechanism by which agents interact with the world. Without tools, an agent can only talk. With tools, it can act.

**Tool Requirements:**
1. **Name** — How the LLM refers to the tool
2. **Description** — What the tool does (the LLM reads this)
3. **Parameters** — What inputs the tool needs
4. **Return value** — What the tool outputs

**Tool example in detail:**

```python
@tool
def calculate_tax(amount: float, tax_rate: float = 0.08) -> str:
    """Calculate sales tax on an amount.
    
    Args:
        amount: The purchase amount in dollars
        tax_rate: The tax rate as a decimal (default 8%)
    
    Returns:
        A string with the tax calculation result
    """
    tax = amount * tax_rate
    total = amount + tax
    return f"Amount: ${amount:.2f} | Tax: ${tax:.2f} | Total: ${total:.2f}"
```

When registered with an agent, the LLM sees:
```
Tool: calculate_tax
Purpose: Calculate sales tax on an amount.
Inputs: amount (number), tax_rate (number, optional, default 0.08)
Output: formatted string with breakdown
```

The LLM can then use this tool when the user asks "What's the total if I buy something for $50?"

### The Difference Between LangChain and LangGraph

**LangChain:** Framework for building LLM applications
- Simple chains (input → LLM → output)
- Agent loops with tools
- Memory management
- Good for: Chatbots, Q&A systems, simple agents

**LangGraph:** Framework for building stateful workflows
- Complex decision trees
- Conditional logic ("if X, do Y; else Z")
- Multiple agents working together
- Human-in-the-loop approvals
- Good for: Workflow automation, multi-step processes, complex decision-making

**In this course:**
- Module 1-3: LangChain (building agents)
- Module 4+: LangGraph (building complex workflows)

### Understanding API Costs

OpenAI charges per token (roughly 4 characters = 1 token).

**GPT-4o mini pricing (as of this course):**
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

**Estimation:**
- 1,000 tokens ≈ 500 words
- A typical query + response ≈ 100-500 tokens
- Cost per query ≈ $0.000005 - $0.00005 (negligible for learning)

**Monitor your usage:**
1. Check balance: https://platform.openai.com/account/billing/overview
2. Set usage limits to prevent surprises
3. Review spending: https://platform.openai.com/account/usage/overview

---

## 🛠️ Part 7: Common Workflows

### Running Python Code with Poetry

Every time you run Python code in this project, use Poetry:

```bash
poetry run python script_name.py
```

**Why?** This ensures you're using the isolated Poetry environment with all dependencies installed, not your system Python.

### Adding New Dependencies

```bash
poetry add package-name
```

Example:
```bash
poetry add requests  # For HTTP requests
poetry add pandas    # For data manipulation
```

Poetry will:
1. Download the package
2. Update `pyproject.toml`
3. Update `poetry.lock` with exact versions
4. Commit these changes to your repository

### Checking What's Installed

```bash
poetry show
```

Lists all installed packages and versions.

### Updating All Dependencies

```bash
poetry update
```

Upgrades all packages to their latest compatible versions and updates `poetry.lock`.

---

## ✅ Part 8: Knowledge Check

Before moving to Module 2, verify you understand:

1. **Environment Setup** — What each file does and why
2. **The ReAct Loop** — Reason → Act → Observe cycle
3. **Tools** — How agents use tools to interact with the world
4. **API Keys** — Why they're sensitive and how to protect them
5. **Poetry** — Why we use it and how to add dependencies

---

## 🎯 Summary

In this module, you:

✅ Set up a professional Python development environment with Poetry
✅ Configured LangChain, LangGraph, and OpenAI integration
✅ Understood the ReAct loop and how agents reason
✅ Learned about tools and how agents use them
✅ Built and verified your first working agent
✅ Learned to read and understand agent behavior

**You now have a solid foundation for building agentic AI systems.**

---

## 🚀 Next Steps

In Module 2, we'll:
- Build agents with multiple tools
- Create custom tools that call APIs
- Implement error handling and logging
- Deploy your agent as a service

See you in the next module!

---

## 📞 Support

If you encounter issues:

1. **Check the troubleshooting guide** — Covers common errors
2. **Review the logs** — Run `poetry run python verify_setup.py` with verbose output
3. **Consult documentation** — https://python.langchain.com/

---

**Happy learning! Let's build intelligent agents.** 🤖