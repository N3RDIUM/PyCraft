# imports
import ctypes
import pyglet.gl as gl
from logger import *
import os

class Shader_error(Exception):
	"""
	Shader_error

	* Exception for shader errors
	"""
	def __init__(self, message):
		self.message = message

def create_shader(target, source_path):
	"""
	create_shader

	* Creates a shader

	:target: the target to create the shader for
	:source_path: the path to the shader source
	"""
	# read shader source

	source_file = open(source_path, "rb")
	source = source_file.read()
	source_file.close()

	source_length = ctypes.c_int(len(source) + 1)
	source_buffer = ctypes.create_string_buffer(source)

	buffer_pointer = ctypes.cast(
		ctypes.pointer(ctypes.pointer(source_buffer)),
		ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

	# compile shader

	gl.glShaderSource(target, 1, buffer_pointer, ctypes.byref(source_length))
	gl.glCompileShader(target)

	# handle potential errors

	log_length = gl.GLint(0)
	gl.glGetShaderiv(target, gl.GL_INFO_LOG_LENGTH, ctypes.byref(log_length))
	
	log_buffer = ctypes.create_string_buffer(log_length.value)
	gl.glGetShaderInfoLog(target, log_length, None, log_buffer)

	if log_length.value > 1:
		raise Shader_error(str(log_buffer.value))

class Shader:
	"""
	Shader

	* This is the shader class.
	"""
	def __init__(self, vert_path, frag_path):
		"""
		Shader.__init__

		* Creates a shader

		:vert_path: the path to the vertex shader
		:frag_path: the path to the fragment shader
		"""
		self.program = gl.glCreateProgram()

		# create vertex shader

		self.vert_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
		create_shader(self.vert_shader, vert_path)
		gl.glAttachShader(self.program, self.vert_shader)

		# create fragment shader

		self.frag_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
		create_shader(self.frag_shader, frag_path)
		gl.glAttachShader(self.program, self.frag_shader)

		# link program and clean up

		gl.glLinkProgram(self.program)

		gl.glDeleteShader(self.vert_shader)
		gl.glDeleteShader(self.frag_shader)
	
	def __del__(self):
		"""
		Shader.__del__

		* Deletes the shader
		"""
		gl.glDeleteProgram(self.program)
	
	def use(self):
		"""
		use

		* Uses the shader
		"""
		gl.glUseProgram(self.program)

shaders = {}

# function to load shaders
def load_shaders():
	"""
	load_shaders

	* Loads all the shaders from a directory
	"""
	for i in os.listdir("./shaders"):
		if not "." in i:
			try:
				# load the vertex and fragment shader
				log("load_shaders", f"Loading shader: {i}")
				# compile the shaders
				shader = Shader("./shaders/" + i + "/vert.glsl", "./shaders/" + i + "/frag.glsl")
				shaders[i] = shader
			except:
				warn("load_shaders", f"Failed to load shader: {i}")
