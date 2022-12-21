import sys
import subprocess
import pkg_resources

# make sure pip is installed
try:
    pkg_resources.require("pip")
except pkg_resources.DistributionNotFound:
    print("pip is not installed. Please install pip.")
    sys.exit(1)

required  = {
    "glfw",
    "numpy",
    "pyopengl",
    "pyopengl-accelerate",
    "noise",
    "pillow",
    "pygame",
    "importlib",
    "flask"
} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    subprocess.Popen([sys.executable, '-m', 'pip', 'install', *missing]).wait()

# run git pull
subprocess.Popen(['git', 'pull']).wait()

# run the game
subprocess.Popen(['python', 'main.py']).wait()
