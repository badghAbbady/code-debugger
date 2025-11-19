
import virtual_env as vem 
import subprocess
import os

VENV_DIR = ".target_venv" 
REQUIREMENTS_PATH = "requirements.txt" 
TARGET_SCRIPT = "buggy_script.py"

def run_target_script(script_path: str):

    try:
        command = ["python",script_path]
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        if process.returncode != 0:
            print("--> Error Captured. Error code :", process.returncode)
            return {
                "success": False,
                "stdout": process.stdout,
                "stderr": process.stderr, 
                "returncode": process.returncode
            }
        else:
            print("--> Success. The script has been executed without problems")
            return {
                "success": True,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "returncode": process.returncode
            }

    except Exception as e:
        print(f"unexpected ERROR : {e}")
        return {"success": False, "stderr": str(e)}

