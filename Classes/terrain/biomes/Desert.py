# inbuilt imports
import Classes as pycraft

class Biome(pycraft.Biome):
    def __init__(self, parent):
        super().__init__("Desert", parent)
        self.sea_level = int(self.noise.noise2(self.parent.seed, self.parent.seed)) * 10

    def generate(self, coords, chunk):
        noise_sand = abs(round(pycraft.lerp(self.noise.noise2(coords[0]/10, coords[1]/10) * 2, self.noise.noise2(coords[0]/100, coords[1]/100) * 10, self.noise.noise2(coords[0]/500, coords[1]/500) * 50)))
        noise_stone = 26+abs(round(self.noise.noise2(coords[0]/5000, coords[1]/5000) * 500))

        chunk.add_preloaded_block("Bedrock", (coords[0], noise_sand-noise_stone, coords[1]))
        for i in range(noise_sand-noise_stone, noise_sand):
            if not abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.2 and abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.1:
                chunk.add_preloaded_block("Stone", (coords[0], i, coords[1]))
            elif not abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.1 and abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.05:
                chunk.add_preloaded_block("CoalOre", (coords[0], i, coords[1]))
            elif not abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.05 and abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.01:
                chunk.add_preloaded_block("IronOre", (coords[0], i, coords[1]))
            elif not abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.01 and abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.005:
                chunk.add_preloaded_block("GoldOre", (coords[0], i, coords[1]))
            elif not abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.005 and abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.001:
                chunk.add_preloaded_block("DiamondOre", (coords[0], i, coords[1]))
            elif not abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) > 0.2 and abs(self.noise.noise3(coords[0]/10, i/10, coords[1]/10)) < 0.8:
                chunk.parent.add_liquid((coords[0], i, coords[1]),  "Lava")
        chunk.add_preloaded_block("Sand", (coords[0], noise_sand, coords[1]))
