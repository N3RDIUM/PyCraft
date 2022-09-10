from packages.perlin import *
from core.util import *

class Generator:
    def __init__(self):
        pass

    def generate_subchunk(self, position, NOISE, blockdata):
        x, y = position

        height_noise = abs(round(lerp(smoothstep(NOISE.noise2(x / 160, y / 160)) / 2, NOISE.noise2(x / 1600, y / 1600) * 100, NOISE.noise2(x / 16, y / 16) * 64)))
        height_noise_low = -(abs(256 + round(NOISE.noise2(x / 16, y / 16) * 10)))

        dirt_noise = abs(5 + round(NOISE.noise2(x / 16, y / 16) * 20))

        blockdata[encode_position((x, height_noise - 1, y))] = "PyCraft:Stone"

        for i in range(height_noise_low, height_noise - 1):
            cave_noise = abs(round(NOISE.noise3(x / 16, i/16, y / 16)))
            if i < height_noise and i > height_noise - dirt_noise:
                if cave_noise < 1/(height_noise - i):
                    blockdata[encode_position((x, i, y))] = "PyCraft:Stone"
            else:
                if cave_noise < 2/(height_noise - i):
                    blockdata[encode_position((x, i, y))] = "PyCraft:Stone"
        
        return blockdata
