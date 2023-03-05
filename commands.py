from importlib import import_module

import subprocess
import os
import sys
from src.utils.commands.run_seeders import run_seeders

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


def print_commands():
    list_pref = "[-]"
    separator = ":"
    print(f"{list_pref} run-project{separator} Starts development server")
    print(f"{list_pref} start-venv{separator} Starts python virtual env and opens a cmd")

# def run_tests():
#     try:
#         import_module()
#     except Exception as err:
#         print(err)


def main(action=""):
    if action == "start-venv":
        run_virtual_env_command(ACTIVATE_ROOT)
    elif action == "close-env":
        run_virtual_env_command(DEACTIVATE_ROOT)
    elif action == "run-project":
        subprocess.run("uvicorn main:app --reload",)
    elif action == "run-seeders":
        run_seeders()
    elif action == "-h":
        print_commands()


if __name__ == "__main__":
    main(sys.argv[1])
