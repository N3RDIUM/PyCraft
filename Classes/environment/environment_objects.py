# imports
from pyglet.gl import *
from opensimplex import OpenSimplex
import random

from pyglet.window.key import N
from logger import *

# Function to load a texture
def load_texture(filename):
    """
    load_texture

    * Loads a texture from a file

    :filename: path of the file to load
    """
    try:
        tex = pyglet.image.load(filename).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)
    except:
        warn("Texture Loader", "Failed to load texture: " + filename)
        return None

# values and noise generators
seed = random.randint(-999999, 999999)
noise = OpenSimplex(seed=seed)

# Single Cloud Class
class Cloud:
    """
    Cloud

    * This is used to draw a single cloud.
    """
    def __init__(self, xz, parent):
        """
        Cloud.__init__

        :x: x position
        :z: z position
        """
        self.pos = xz
        self.size = [16,16]
        self.parent = parent

    def draw(self):
        """
        draw

        * Draws the cloud
        """
        x = self.pos[0] - self.size[0]
        y = self.parent.parent.render_distance / 5 * self.parent.parent.chunk_size
        z = self.pos[1] - self.size[0]

        X = self.pos[0] + self.size[0]
        Z = self.pos[1] + self.size[1]

        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(1, 1, 1)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)))
        glPopMatrix()

class Sun:
    """
    Sun

    * This is used to draw the sun.
    """
    def __init__(self, position):
        """
        Sun.__init__

        :x: x position
        :z: z position
        """
        self.pos = position
        self.size = [10, 10]
        self.texture = load_texture("assets/textures/environment/sun.png")

    def draw(self):
        """
        draw

        * Draws the sun
        """
        x = self.pos[0]
        y = 50
        z = self.pos[1]

        X = x+self.size[0]
        Z = z+self.size[1]

        glPushMatrix()
        glColor3f(1, 1, 0)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, self.texture, ('v3f', (x, y, Z,  X, y, Z,  X, y, z,  x, y, z)))
        glColor3f(1, 1, 1)
        glPopMatrix()
