# Reporover

# 🤖 RepoRover: Agentic Software Engineer

RepoRover is an autonomous, multi-agent AI system designed to act as a local software engineer. It can take natural language commands, analyze a local codebase, make surgical file edits, test code in a Docker sandbox, and push the final changes to a remote GitHub repository.

Built entirely with local open-source models (Llama 3) and LangGraph, this project explores the capabilities and limitations of autonomous coding agents.

## 🚀 Key Features

* **Multi-Agent Workflow:** Utilizes a Manager-Worker architecture with specialized agents (Router, Architect, Coder, Publisher) to divide reasoning and execution tasks.
* **Surgical Edits (Diff-based patching):** Bypasses the common "Lazy Writer" limitation of local LLMs by using structural regex insertion and atomic patching instead of full-file rewrites.
* **Docker Sandbox:** Safely executes and tests generated Python scripts in an isolated container environment.
* **Human-in-the-Loop Git Push:** Edits files locally first, allowing for human review before executing remote deployment commands.
* **Codebase RAG:** Uses Retrieval-Augmented Generation to scan the repository structure and contextually identify which files need modification.

## 🛠️ Tech Stack

* **Orchestration:** LangChain & LangGraph (Stateful Agent Workflows)
* **Brain:** Ollama (Llama 3.1 running locally)
* **Version Control:** GitPython
* **Execution Environment:** Docker SDK for Python
* **Embeddings & Retrieval:** CodeRAG (Custom Vector Search)
* **Observability:** LangSmith

## 🧠 Engineering Discoveries: Solving the "Lazy Writer" Problem

While building this agent, I encountered a major bottleneck with local LLMs: **Generation Fatigue**. 

When tasked with editing a 500-line file, the model would plan perfectly, but truncate the code during the rewrite phase (e.g., outputting the first 50 lines and replacing the rest with `// rest of code here`), effectively destroying the file.

**The Solution:** I refactored the agent to act as a **Surgical Architect** rather than a typist:
1.  **Atomic Patching:** Forced the LLM to output only the specific lines of code needed for the fix (Unified Diff style).
2.  **Structural Regex:** Built Python logic to parse the LLM's snippet and inject it precisely into specific tags (like inserting footers directly before `</body>` in HTML) rather than trusting the LLM to rewrite the entire DOM.
3.  **State Management:** By separating the "Planner" (Architect Node) from the "Writer" (Coder Node), the system prevents context-window exhaustion.

## ⚙️ Local Setup & Installation

### 1. Prerequisites
* Python 3.9+
* Docker (running locally for the sandbox)
* Ollama (with `llama3.1` pulled: `ollama run llama3.1`)

### 2. Environment Setup
Clone the repository and create a virtual environment:
```bash
git clone <your-repo-url>
cd RepoRover
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```
3. Install Dependencies
Bash
pip install langchain langchain-ollama langgraph langchain-chroma langchain-huggingface docker GitPython python-dotenv
4. Environment Variables
Create a .env file in the root directory for LangSmith observability (optional but recommended):

Code snippet
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGCHAIN_API_KEY="your-langsmith-api-key"
LANGCHAIN_PROJECT="Agentic-Engineer"
🎮 Usage
Run the main orchestrator script:

Bash
python main.py
Example Commands:
1. Local Script Execution (Docker Sandbox)

👉 Task: Write a python script to calculate the first 50 Fibonacci numbers.
(The Local Coder will write the script, run it inside Docker, and return the output).

2. Repository File Editing (Surgical Mode)

👉 Task: Add a footer to index.html with the text "Maintained by AI".
(The Architect finds index.html, the Coder injects the HTML securely inside the <body> tag).

3. Remote Deployment (Manual Approval)

👉 Task: Push to https://github.com/YourUsername/Your-Repo.git
(The Publisher stages the changes, commits them, and pushes to a new branch on the remote).


ARJUN PATEL 
LinkedIn:- https://www.linkedin.com/in/arjunpatel97259/
