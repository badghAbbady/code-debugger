
import os
import subprocess
import venv

def create_and_install_venv(venv_path , requirements_file) :
    if not os.path.exists(venv_path) :
        try:
            venv.create(venv_path,with_pip=True,symlinks=True)
        except Exception as e:
            print(f"Error while creating venv {e}")
    else :
        print("venv déjà crée")


    python_executable = os.path.join(venv_path, "bin", "python")

    if os.path.exists(requirements_file) :
        try :
            command = [python_executable,"-m","pip","install","-r",requirements_file]
            process = subprocess.run(command,capture_output=True,text=True,check=True)
        except subprocess.CalledProcessError as e :
            print(f"--> Error while installing dependencies : {e.stderr}")
        except FileNotFoundError:
            print(f"--> Coudln't find python executable : {python_executable}")
            return None
    else :
        print("--> no requirements file found")

    return python_executable
        





