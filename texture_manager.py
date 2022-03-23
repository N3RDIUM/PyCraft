from OpenGL.GL import *
from PIL import Image

class TextureAtlasGenerator:
    # Texture atlas gen which automatically fits all images into a single texture and forces them to be square.
    def __init__(self, texture_size=32, n_textures = 32):
        self.texture_size = texture_size * n_textures
        self.texture_atlas = Image.new("RGBA", (self.texture_size, self.texture_size), (0, 0, 0, 0))
        self.texture_atlas_data = self.texture_atlas.load()
        self.current_size = 0
        self.current_x = 0
        self.current_y = 0
        self.used = []
    
    def add(self, image):
        # Add image to texture atlas.
        if image.size[0] > self.texture_size or image.size[1] > self.texture_size or image.size  != (32, 32):
            return None
        if self.current_size + image.size[0] > self.texture_size:
            self.current_size = 0
            self.current_x = 0
            self.current_y += self.texture_size
        if self.current_y + image.size[1] > self.texture_size:
            self.current_size = 0
            self.current_x = 0
            self.current_y = 0
        self.used.append((self.current_x, self.current_y, image.size[0], image.size[1]))
        self.texture_atlas.paste(image, (self.current_x, self.current_y))
        self.current_x += image.size[0]
        self.current_size += image.size[0]
        if self.current_x + image.size[0] > self.texture_size:
            self.current_size = 0
            self.current_x = 0
            self.current_y += image.size[1]

    def get_texture_atlas(self):
        # Return texture atlas.
        return self.texture_atlas

    def save(self, path):
        # Save texture atlas to file.
        self.texture_atlas.save(path)
        # show
        self.texture_atlas.show()

    def get_rect(self, index):
        try:
            # Return rect of image at index.
            return self.used[index]
        except:
            return None

class TextureAtlas:
    def __init__(self):
        self.atlas_generator = TextureAtlasGenerator()
        self.textures = []
        self.texture_coords = {}

    def add(self, image, name):
        self.atlas_generator.add(image)
        self.textures.append(image)

        # get texture coordinates
        try:
            _ = self.atlas_generator.get_rect(len(self.textures) - 1)
            x = _[0]
            y = _[1]
            w = _[2]
            h = _[3]
            self.texture_coords[name] = (x/self.atlas_generator.texture_size, y/self.atlas_generator.texture_size,
                                            (x)/self.atlas_generator.texture_size, (y+h)/self.atlas_generator.texture_size,
                                            (x+w)/self.atlas_generator.texture_size, (y+h)/self.atlas_generator.texture_size,
                                            (x+w)/self.atlas_generator.texture_size, (y)/self.atlas_generator.texture_size
                                        )
        except:
            pass

    def save(self, path):
        self.atlas_generator.save(path)

# example usage
if __name__ == "__main__":
    atlas = TextureAtlas()
    # get all images in assets/textures/block
    import os
    for file in os.listdir("assets/textures/block"):
        if file.endswith(".png"):
            image = Image.open("assets/textures/block/" + file)
            atlas.add(image, file.split('.')[0])
    atlas.save("atlas.png")
