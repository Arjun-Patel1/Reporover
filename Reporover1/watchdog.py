import time
import os
import sys
import subprocess
import requests  # <--- FIXED: Added missing import
from dotenv import load_dotenv

# Add src to path so we can import our tools
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.tools.git_tool import GitTool

load_dotenv()

# --- CONFIGURATION ---
REPO_NAME = "Arjun-Patel1/Weather-Dashboard"  # Your Repo Name
TRIGGER_LABEL = "reporover"                   # The label to watch for
# ---------------------

def main():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN not found in .env")
        return

    git_tool = GitTool()
    print(f"👀 RepoRover Watchdog active!")
    print(f"   Watching: https://github.com/{REPO_NAME}")
    print(f"   Waiting for issues with label: '{TRIGGER_LABEL}'...")

    # Keep track of issues we've already processed so we don't loop forever
    processed_issues = set()

    while True:
        try:
            # 1. Get Issues from GitHub
            issues = git_tool.get_issues(REPO_NAME, token, TRIGGER_LABEL)
            
            for issue in issues:
                issue_number = issue["number"]
                
                # Skip if we already handled this in this session
                if issue_number in processed_issues:
                    continue
                
                print(f"\n🔔 FOUND NEW ISSUE #{issue_number}: {issue['title']}")
                
                # 2. Acknowledge the issue (Comment on GitHub)
                print("   -> Posting 'Analyzing' comment...")
                git_tool.post_comment(REPO_NAME, issue_number, token, "🤖 **RepoRover is on the case!**\n\nI am analyzing your request and initializing the agent squad. Stand by...")
                
                # 3. Construct the Command for the Agent
                # We combine Title + Body to give the agent full context
                prompt = f"Issue: {issue['title']}. Details: {issue['body']}"
                repo_url = f"https://github.com/{REPO_NAME}.git"
                
                # 4. Trigger the Main Agent (Subprocess)
                print(f"   -> Launching Agent process...")
                cmd = [
                    sys.executable, "main.py",
                    "--url", repo_url,
                    "--push",   # Auto-push the fix
                    prompt
                ]
                
                # Run the agent and capture the output
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # 5. Report Back to GitHub
                if result.returncode == 0:
                    print("✅ Agent finished successfully.")
                    
                    # Create the success message
                    response_msg = (
                        f"✅ **Fix Deployed!**\n\n"
                        f"I have successfully patched the code. \n"
                        f"You can view the changes here: [Compare Branch](https://github.com/{REPO_NAME}/compare/fix/reporover-auto-patch)\n\n"
                        f"**Next Steps:**\n"
                        f"1. Review the code.\n"
                        f"2. Create a Pull Request to merge `fix/reporover-auto-patch` into main."
                    )
                    git_tool.post_comment(REPO_NAME, issue_number, token, response_msg)
                    
                    # Optional: Remove the label so we don't process it again?
                    # For now, we just add to processed set.
                    
                else:
                    print("❌ Agent failed.")
                    # Grab the last 1000 characters of the log for debugging
                    error_log = result.stdout[-1000:] if result.stdout else result.stderr
                    
                    response_msg = (
                        f"❌ **Attempt Failed**\n\n"
                        f"I tried to fix the issue but encountered an error.\n\n"
                        f"**Logs:**\n```\n{error_log}\n```"
                    )
                    git_tool.post_comment(REPO_NAME, issue_number, token, response_msg)

                # Mark as done
                processed_issues.add(issue_number)

            # Sleep before checking again to avoid rate limits
            time.sleep(30) 

        except KeyboardInterrupt:
            print("\n👋 Watchdog stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Watchdog Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()