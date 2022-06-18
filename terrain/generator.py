import opensimplex

class Generator:
    def __init__(self):
        self.noise = opensimplex.OpenSimplex(seed = 1024)

    def generate(self, chunk, position, storage):
        x, y = position

        for i in range(x - 8, x + 8):
            for j in range(y - 8, y + 8):
                noise = round(self.noise.noise2(i / 16, j / 16) * 10)
                noise_sand  = (self.noise.noise2(-i / 16, -j / 16) * 10) - 5
                if not noise_sand > 0:
                    chunk.add_generated((i, noise, j), "grass", storage)
                else:
                    chunk.add_generated((i, noise, j), "sand", storage)

                for k in range(noise - 8, noise):
                    chunk.add_generated((i, k, j), "dirt", storage)