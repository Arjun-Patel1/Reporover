import docker
import os
import tarfile
import io
import time

class DockerTool:
    def __init__(self, repo_path="./", image_name="reporover-sandbox"):
        self.client = docker.from_env()
        self.image_name = image_name
        # Ensure we have absolute path to avoid mounting issues
        self.repo_path = os.path.abspath(repo_path)
        self._build_image()

    def _build_image(self):
        """Checks if the sandbox image exists; builds if missing."""
        print(f"Checking for Docker image: {self.image_name}...")
        try:
            self.client.images.get(self.image_name)
        except docker.errors.ImageNotFound:
            print("Image not found. Building...")
            # Assuming Dockerfile is in the project root (2 levels up from src/tools)
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
            self.client.images.build(path=base_path, tag=self.image_name)
            print("Build complete.")

    def run_code(self, code_snippet: str):
        """
        Runs the code snippet in a container with a SAFETY TIMEOUT.
        """
        script_name = "_reporover_test.py"
        container = None
        
        try:
            # 1. Start a fresh container
            # We mount the repo_path to /app so the script can see the repo files
            container = self.client.containers.run(
                self.image_name,
                command="tail -f /dev/null",  # Keep alive command
                detach=True,
                working_dir="/app",
                volumes={
                    self.repo_path: {'bind': '/app', 'mode': 'rw'}
                }
            )

            # 2. Upload the python script into the container
            # We use tarfile to put the string directly into the container as a file
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                code_bytes = code_snippet.encode('utf-8')
                tar_info = tarfile.TarInfo(name=script_name)
                tar_info.size = len(code_bytes)
                tar_info.mtime = time.time()
                tar.addfile(tar_info, io.BytesIO(code_bytes))
            tar_stream.seek(0)
            
            container.put_archive('/app', tar_stream)

            # 3. EXECUTE WITH TIMEOUT
            # We use the Linux 'timeout' command. 
            # If it runs > 15 seconds, it kills the python process.
            # 124 is the standard exit code for timeout.
            cmd = f"timeout 15s python3 {script_name}"
            
            exec_result = container.exec_run(cmd)
            
            output = exec_result.output.decode("utf-8")
            exit_code = exec_result.exit_code

            # 4. Handle Timeout Specifically
            if exit_code == 124:
                return {
                    "exit_code": 1, 
                    "output": "TIMEOUT_ERROR: The script took longer than 15 seconds. Check for infinite loops (while True) or waiting for input()."
                }

            return {
                "exit_code": exit_code,
                "output": output
            }

        except Exception as e:
            return {
                "exit_code": 1,
                "output": f"Docker execution failed: {str(e)}"
            }
            
        finally:
            # 5. Cleanup: Kill container and remove temp file
            if container:
                try:
                    container.kill()
                    container.remove()
                except:
                    pass
            
            # Clean up the local file if it was somehow created in the volume mount
            local_test_file = os.path.join(self.repo_path, script_name)
            if os.path.exists(local_test_file):
                try:
                    os.remove(local_test_file)
                except:
                    pass