import subprocess
import os

def start_helpers():
    for helper in os.listdir("helpers/helpers"):
        if helper.endswith(".py") or helper.endswith(".pyx"):
            subprocess.Popen(f"python helpers/helpers/{helper}", shell=True)