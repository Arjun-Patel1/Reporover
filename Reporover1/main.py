import argparse
import sys
import os
import subprocess
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.agent import RepoRoverAgent
from src.utils.logger import setup_logger
from src.tools.git_tool import GitTool

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="RepoRover: Autonomous Code Repair Agent")
    parser.add_argument("query", type=str, help="The bug report or feature request.")
    parser.add_argument("--url", type=str, help="GitHub URL to clone and fix.")
    parser.add_argument("--push", action="store_true", help="Automatically push the fix to GitHub.")
    
    args = parser.parse_args()
    logger = setup_logger()
    
    # 1. Setup Workspace
    workspace_path = "./workspace"
    git_tool = None
    
    if args.url:
        git_tool = GitTool(workspace_dir=workspace_path)
        try:
            git_tool.clone_repo(args.url)
        except Exception as e:
            logger.error(f"Clone failed: {e}")
            return
    else:
        workspace_path = os.path.abspath("./")

    # 2. Run the Agent
    logger.info(f"🚀 Starting RepoRover on: {workspace_path}")
    
    try:
        agent = RepoRoverAgent(repo_path=workspace_path)
        workflow = agent.build_graph()
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        return

    logger.info("🤖 Agent is analyzing and fixing...")
    
    # --- UPDATED STATE INITIALIZATION ---
    final_state = workflow.invoke({
        "query": args.query,
        "retry_count": 0,
        "max_retries": 3,
        "context": [],
        "code_solution": "",
        "test_output": "",
        "exit_code": -1,
        "error_analysis": "",
        "review_status": "PENDING",
        "plan": "",                 # <--- NEW: Initialize Plan
        "supervisor_feedback": ""   # <--- NEW: Initialize Supervisor
    })

    print("\n" + "="*50)
    print("FINAL REPORT")
    print("="*50)
    
    if final_state["exit_code"] == 0:
        print("✅ SUCCESS: The bug has been fixed.")
        
        # Determine where the code lives
        actual_work_dir = os.path.abspath(workspace_path) if args.url else os.getcwd()
        
        # Save the solution script INSIDE that folder
        solution_script_name = "_apply_fix.py"
        solution_script_path = os.path.join(actual_work_dir, solution_script_name)
        
        with open(solution_script_path, "w", encoding="utf-8") as f:
            f.write(final_state["code_solution"])
            
        print(f"📝 Applying fix in: {actual_work_dir}")
        
        try:
            subprocess.run(
                [sys.executable, solution_script_name], 
                cwd=actual_work_dir,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to apply fix: {e}")
        
        if os.path.exists(solution_script_path):
            os.remove(solution_script_path)

        # 4. AUTO-PUSH TO GITHUB
        if args.push and args.url:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                print("❌ Cannot push: GITHUB_TOKEN not found in .env")
            else:
                print("\n📦 Git Operations:")
                git_tool.configure_user()
                git_tool.create_branch("fix/reporover-auto-patch")
                
                # Commit and Push (Force push to overwrite previous bot attempts)
                git_tool.commit_changes(f"Fix: {args.query}")
                git_tool.push_changes("fix/reporover-auto-patch", token)
        
    else:
        print("❌ FAILURE: Could not fix the bug.")
        print(f"Error Log: {final_state['test_output']}")

if __name__ == "__main__":
    main()