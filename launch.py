# imports
import os
import sys

# pull updates
os.system("git pull")

# install requirements
os.system(f"{sys.executable} -m pip install -U pip")
os.system(f"{sys.executable} -m pip install -r requirements.txt")

# run main.py with the same python executable
os.system(f"{sys.executable} main.py")
