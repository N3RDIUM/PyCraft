from packages.perlin import *
from core.util import *
from noise import snoise3, snoise4


class Generator:
    def __init__(self):
        self.weather_desc = [
            "temperate",
            "wet",
            "windy",
        ]

    def generate_subchunk(self, position, SEED, blockdata):
        x, y = position

        height_noise = round(lerp(
            smoothstep(snoise3(x / 160, y / 160, SEED)) / 2,
            snoise3(x / 1600, y / 1600, SEED) * 100,
            snoise3(x / 16000, y / 16000, SEED) * 64)
        )
        height_noise_low = -192

        dirt_noise = abs(5 + round(snoise3(x / 16, y / 16, SEED) * 20))

        blockdata[encode_vector((x, height_noise - 1, y))] = "PyCraft:Grass"

        for i in range(height_noise_low, height_noise - 1):
            cave_noise = abs(round(snoise4(x / 16, i/16, y / 16, SEED)))
            if i < height_noise and i > height_noise - dirt_noise:
                if cave_noise < 1/(height_noise - i):
                    blockdata[encode_vector((x, i, y))] = "PyCraft:Dirt"
            else:
                if cave_noise < 2/(height_noise - i):
                    blockdata[encode_vector((x, i, y))] = "PyCraft:Stone"

        blockdata[encode_vector((x, height_noise_low - 1, y))] = "PyCraft:Stone"
