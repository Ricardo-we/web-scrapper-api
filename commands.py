import subprocess
import os
import sys

VENV_ROOT = os.path.join("venv", "Scripts")
DEACTIVATE_ROOT = os.path.join(VENV_ROOT,  "deactivate.bat")
ACTIVATE_ROOT = os.path.join(VENV_ROOT,  "activate.bat")


def run_virtual_env_command(virtual_env_root=VENV_ROOT):
    try:
        subprocess.run("cmd.exe /k start " + virtual_env_root,)
        print(virtual_env_root)
        return True
    except Exception as e:
        print(e)
        print("FAILED starting venv")
        return False


def main(action=""):
    if action == "start-venv":
        run_virtual_env_command(ACTIVATE_ROOT)
    elif action == "close-env":
        run_virtual_env_command(DEACTIVATE_ROOT)
    elif action == "run-project":
        subprocess.run("uvicorn main:app --reload",)


if __name__ == "__main__":
    main(sys.argv[1])
