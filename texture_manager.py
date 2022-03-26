from OpenGL.GL import *
from PIL import Image

class TextureAtlasGenerator:
    def __init__(self, texture_size=32, n_textures = 100):
        self.texture_size = texture_size * n_textures
        self.n_textures = n_textures
        self.texture_atlas = Image.new("RGBA", (self.texture_size, self.texture_size), (0, 0, 0, 0))
        self.texture_atlas_data = self.texture_atlas.load()
        self.current_side = 0
        self.current_x = 0
        self.current_y = 0
        self.used = []
    
    def add(self, image):
        # Add image to texture atlas.
        if image.size[0] > self.texture_size or image.size[1] > self.texture_size:
            raise Exception("Image is too large for texture atlas.")

        if self.current_x + image.size[0] > self.texture_size:
            self.current_x = 0
            self.current_y += image.size[1]
            self.current_side += 1
        
        if self.current_y + image.size[1] > self.texture_size:
            raise Exception("Texture atlas is full.")

        self.texture_atlas.paste(image, (self.current_x, self.current_y))
        self.used.append((self.current_side, self.current_x, self.current_y, image.size[0], image.size[1]))
        self.current_x += image.size[0]
        return self.current_side, self.current_x, self.current_y, image.size[0], image.size[1]

    def get_texture_atlas(self):
        return self.texture_atlas

    def save(self, path):
        self.texture_atlas.save(path)

    def get_rect(self, index):
        side, x, y, w, h = self.used[index]
        return side, x, y, w, h

class TextureAtlas:
    def __init__(self):
        self.atlas_generator = TextureAtlasGenerator()
        self.textures = []
        self.texture_coords = {}
        self.save_path = None

    def add(self, image, name):
        self.atlas_generator.add(image)
        self.textures.append(image)

        # get texture coordinates
        _ = self.atlas_generator.get_rect(len(self.textures) - 1)
        x = _[1]
        y = -_[2]
        w = _[3]
        h = _[4]
        # TexCoords for OpenGL
        self.texture_coords[name] = (
            x / self.atlas_generator.texture_size,
            y / self.atlas_generator.texture_size,

            (x + w) / self.atlas_generator.texture_size,
            y / self.atlas_generator.texture_size,

            (x + w) / self.atlas_generator.texture_size,
            (y - h) / self.atlas_generator.texture_size,

            x / self.atlas_generator.texture_size,
            (y - h) / self.atlas_generator.texture_size
        )

    def save(self, path):
        self.atlas_generator.save(path)
        self.save_path = path

    def add_from_folder(self, path):
        import os
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                image = Image.open(path + filename)
                self.add(image, filename)

    def bind(self):
        import pygame
        texSurface = pygame.image.load(self.save_path)
        texData = pygame.image.tostring(texSurface, "RGBA", 1)
        width = texSurface.get_width()
        height = texSurface.get_height()
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 
                0, GL_RGBA, GL_UNSIGNED_BYTE, texData)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        return texid

# example usage
if __name__ == "__main__":
    atlas = TextureAtlas()
    atlas.add_from_folder("assets/textures/block")
    atlas.save("atlas.png")
    print(atlas.texture_coords)
