import opensimplex

class Generator:
    def __init__(self):
        self.noise = opensimplex.OpenSimplex(seed = 1024)

    def generate(self, chunk, position):
        x, y = (position[0] // 16, position[1] // 16)

        for i in range(x - 8, x + 8):
            for j in range(y - 8, y + 8):
                noise = round(self.noise.noise2(i / 16, j / 16) * 10)
                chunk.add_generated((i, noise, j), "grass_block")

                # 10 block thick layer of dirt
                for k in range(noise - 10, noise):
                    chunk.add_generated((i, k, j), "dirt")
