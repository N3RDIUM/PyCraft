import pyglet
import pyglet.gl as gl

class TextureManager:
	def __init__(self, texture_width, texture_height, max_textures):
		self.texture_width = texture_width
		self.texture_height = texture_height

		self.max_textures = max_textures

		self.textures = []

		self.texture_array = gl.GLuint(0)
		gl.glGenTextures(1, self.texture_array)
		gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_array)

		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
		gl.glTexParameteri(gl.GL_TEXTURE_2D_ARRAY, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

		gl.glTexImage3D(
			gl.GL_TEXTURE_2D_ARRAY, 0, gl.GL_RGBA,
			self.texture_width, self.texture_height, self.max_textures,
			0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, None)
	
	def generate_mipmaps(self):
		gl.glGenerateMipmap(gl.GL_TEXTURE_2D_ARRAY)
	
	def add_texture(self, texture):
		if not texture in self.textures:
			image_name = texture.split("/")[-1]
			image_name = image_name.split(".")[0]
			self.textures.append(image_name)

			texture_image = pyglet.image.load(texture).get_image_data()
			gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY, self.texture_array)

			gl.glTexSubImage3D(
				gl.GL_TEXTURE_2D_ARRAY, 0,
				0, 0, self.textures.index(image_name),
				self.texture_width, self.texture_height, 1,
				gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
				texture_image.get_data("RGBA", texture_image.width * 4))