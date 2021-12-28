# imports
from ratcave import Shader
from logger import *
import os

shaders = {}

# function to load shaders
def load_shaders():
	"""
	load_shaders

	* Loads all the shaders from a directory
	"""
	for i in os.listdir("./shaders"):
		if "." not in i:
			try:
				# load the vertex and fragment shader
				log("load_shaders", f"Loading shader: {i}")

				# Read the files
				with open(f"./shaders/{i}/vertex.glsl", "r") as vertex_file:
					vertex_shader = vertex_file.read()
				
				with open(f"./shaders/{i}/fragment.glsl", "r") as fragment_file:
					fragment_shader = fragment_file.read()

				# compile the shaders
				shader = Shader(vertex_shader, fragment_shader)
				shaders[i] = shader
			except:
				warn("load_shaders", f"Failed to load shader: {i}")
