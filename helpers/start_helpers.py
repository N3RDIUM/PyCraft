import subprocess
import os

# Get the number of cores
import multiprocessing
processes = multiprocessing.cpu_count()
print(f"[PyCraft] Using {processes} CPU cores for terrain gen helpers.")

def start_helpers():
    for helper in os.listdir("helpers/helpers"):
        if helper.endswith(".py") or helper.endswith(".pyx") and not "chunk_loader" in helper:
            subprocess.Popen(f"python helpers/helpers/{helper}", shell=True)
        if "chunk_loader" in helper:
            for i in range(processes):
                subprocess.Popen(f"python helpers/helpers/{helper}", shell=True)