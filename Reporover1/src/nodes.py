import os
import re
import difflib
from dotenv import load_dotenv
from src.state import AgentState
from src.rag import CodeRAG
from src.tools import DockerTool, FileTool, GitTool
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = OllamaLLM(model="llama3.1")

# --- 1. ROUTER (The Dispatcher) ---
def router_node(state: AgentState):
    query = state["query"].lower()
    
    # Check for PUSH command
    if "push" in query and ("http" in query or "github" in query):
        print("   -> Command detected: PUSH to Remote")
        words = state["query"].split()
        url = next((w for w in words if "http" in w), None)
        return {"mode": "PUSH", "repo_url": url}

    # Check for REPO Edit command
    repo_triggers = ["update", "change", "add", "fix", "readme", "repo", "project", "file", "html", "index", "app"]
    if any(t in query for t in repo_triggers):
        print("   -> Command detected: REPO Edit (Local Save Only)")
        return {"mode": "REPO"}

    return {"mode": "LOCAL"}

# --- 2. LOCAL CODER (Junior Dev) ---
def local_coder_node(state: AgentState):
    print("🏠 Mode: LOCAL. Writing & Running...")
    chain = ChatPromptTemplate.from_template("Write python code for: {query}. Output ONLY code.") | llm
    code = chain.invoke({"query": state["query"]}).replace("```python","").replace("```","").strip()
    
    os.makedirs("solutions", exist_ok=True)
    with open("solutions/solution.py", "w", encoding="utf-8") as f:
        f.write(code)
        
    output = DockerTool().run_python_script("solution.py")
    return {"code": code, "test_output": output}

# --- 3. REPO ARCHITECT (The Planner) ---
def repo_architect_node(state: AgentState):
    print("🏗️ Architect: Analyzing file structure...")
    rag = CodeRAG(repo_path="./workspace")
    file_tool = FileTool()
    
    relevant = rag.search(state["query"])
    
    # Strict prompt to prevent "Chatty Architect" error
    chain = ChatPromptTemplate.from_template("""
    Task: {query}
    Repo Files: {file_tree}
    
    Identify the SINGLE target file to edit.
    Output ONLY the filename (e.g., 'index.html'). NO EXPLANATION.
    """) | llm
    
    raw_output = chain.invoke({
        "query": state["query"], 
        "file_tree": file_tool.list_files()
    }).strip()
    
    # Cleanup logic for chatty LLMs
    clean_file = raw_output.replace("`", "").split()[-1].strip(".,!")
    print(f"   -> Targeted file: {clean_file}")
    
    content = file_tool.read_file(clean_file)
    return {"target_file": clean_file, "file_content": content, "documents": relevant, "mode": "REPO"}

# --- 4. REPO CODER (The Surgical Editor) ---
def repo_coder_node(state: AgentState):
    query = state["query"].lower()
    target_file = state["target_file"]
    file_path = os.path.join("workspace", target_file)
    
    print(f"✍️ Coder: Applying atomic edit to {target_file}...")

    if not os.path.exists(file_path):
        return {"test_output": "❌ Error: File not found."}

    with open(file_path, "r", encoding="utf-8") as f:
        current_content = f.read()

    # STRATEGY 1: HTML Surgical Insert (Best for Footers/Comments)
    if target_file.endswith(".html") and any(k in query for k in ["add", "footer", "append"]):
        print("   -> Strategy: HTML Tag-Specific Insertion")
        chain = ChatPromptTemplate.from_template("Write the HTML snippet for: {query}. Output ONLY code.") | llm
        snippet = chain.invoke({"query": state["query"]}).replace("```html", "").replace("```", "").strip()
        
        pattern = re.compile(r"(</body>)", re.IGNORECASE)
        if pattern.search(current_content):
            new_content = pattern.sub(f"\n{snippet}\n\\1", current_content)
            with open(file_path, "w", encoding="utf-8") as f: f.write(new_content)
            return {"code": snippet, "git_message": f"Injected footer into {target_file}"}

    # STRATEGY 2: Patch/Diff Style (The LinkedIn "Workaround")
    print("   -> Strategy: Atomic Patching")
    chain = ChatPromptTemplate.from_template("""
    Task: {query}
    File: {target_file}
    
    Generate ONLY the specific lines of code needed to fulfill the request. 
    Do not rewrite the whole file. I will append this to the end or merge it.
    """) | llm
    
    patch_code = chain.invoke({"query": state["query"], "target_file": target_file}).replace("```", "").strip()

    # Check for duplicates before appending
    if patch_code[:20] in current_content:
        print("   ⚠️ Change already detected in file. Skipping to prevent loop.")
        return {"code": patch_code, "status": "No changes needed"}

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + patch_code)
    
    return {"code": patch_code, "git_message": f"Patched {target_file}"}

# --- 5. GIT PUBLISHER (Manual Push) ---
def git_publisher_node(state: AgentState):
    print("🚀 Publisher: Configuring Remote & Pushing...")
    url = state.get("repo_url")
    
    if not url:
        return {"test_output": "❌ Error: Provide a URL (e.g., 'Push to http...')"}
        
    git_tool = GitTool()
    try:
        if "origin" in git_tool.repo.remotes:
            git_tool.repo.delete_remote("origin")
        
        git_tool.repo.create_remote("origin", url)
        print(f"   -> Remote 'origin' set to: {url}")
        
        result = git_tool.commit_and_push("Agentic fix: Applied atomic patch")
        return {"test_output": result}
    except Exception as e:
        return {"test_output": f"Error during push: {e}"}
