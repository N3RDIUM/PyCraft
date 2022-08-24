from packages.perlin import *
from core.util import *

class DesertGenerator:
    def __init__(self):
        pass

    def generate_filament(self, x, y, NOISE):
        blockdata = {}

        height_noise = abs(round(lerp(smoothstep(NOISE.noise2(x / 160, y / 160)) / 2, NOISE.noise2(x / 1600, y / 1600) * 100, NOISE.noise2(x / 16, y / 16) * 64)))
        height_noise_low = -(abs(256 + round(NOISE.noise2(x / 16, y / 16) * 10)))

        sand_noise = abs(4 + round(NOISE.noise2(x / 16, y / 16) * 20))

        blockdata[encode_position((x, height_noise - 1, y))] = 2

        for i in range(height_noise_low, height_noise - 1):
            cave_noise = abs(round(NOISE.noise3(x / 16, i/16, y / 16) * 10))
            if i < height_noise and i > height_noise - sand_noise:
                blockdata[encode_position((x, i, y))] = 2
            else:
                if cave_noise < 4:
                    blockdata[encode_position((x, i, y))] = 3
        
        return blockdata
