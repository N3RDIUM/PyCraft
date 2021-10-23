import pyshaders, os, logging, time
logging.basicConfig(level=logging.DEBUG)

def log(source, message):
    now = time.strftime("%H:%M:%S")
    logging.debug(f"({now}) [{source}]: {message}")

shaders = {}

def load_shaders():
    for i in os.listdir("./shaders"):
        if not "." in i:
            log("load_shaders", f"Loading shader: {i}")
            frag = None
            vert = None
            with open("./shaders/" + i+ "/"+f'{i}.frag', "r") as f:
                frag = f.read()
            with open("./shaders/" + i+ "/"+f'{i}.vert', "r") as f:
                vert = f.read()
            shaders[i] = pyshaders.from_string(frag,vert)
