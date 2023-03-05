# import sys
# sys.path.insert(0,'../..')

import os
import importlib
from settings import APPS, APP_ROOT_DIR

def run_seeders():
    for app in APPS:
        try:
            module_root = f"app.{app}"
            module_name = "seeder"
            module_full_path = f"{module_root}.{module_name}"
            seeder = __import__(module_full_path, globals(), locals(), ["seed"],  3)
            seeder.seed()
        except Exception as err:
            print(err)
            print("Module not found")