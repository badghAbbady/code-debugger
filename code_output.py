
import virtual_env as vem 
import subprocess
import os



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
            return {
                "success": False,
                "stdout": process.stdout,
                "stderr": process.stderr, 
                "returncode": process.returncode
            }
        else:
            return {
                "success": True,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "returncode": process.returncode
            }

    except Exception as e:
        print(f"unexpected ERROR : {e}")
        return {"success": False, "stderr": str(e)}

