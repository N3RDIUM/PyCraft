# inbuilt imports
import Classes as pycraft

class Biome(pycraft.Biome):
    def __init__(self, parent):
        super().__init__("Jungle", parent)
        self.sea_level = int(self.noise.noise2(self.parent.seed, self.parent.seed)) * 1000

    def generate(self, coords, chunk):
        noise_grass = round(pycraft.lerp(self.noise.noise2(coords[0]/10, coords[1]/10) * 2, self.noise.noise2(coords[0]/100, coords[1]/100) * 10, self.noise.noise2(coords[0]/500, coords[1]/500) * 50))
        noise_dirt = 1+abs(round(pycraft.lerp(self.noise.noise2(coords[0]/10, coords[1]/10) * 2, self.noise.noise2(coords[0]/100, coords[1]/100) * 7, self.noise.noise2(coords[0]/500, coords[1]/500) * 5)))                
        noise_stone = 26+round(self.noise.noise2(coords[0]/5000, coords[1]/5000) * 500)

        if noise_grass < self.sea_level:
            for i in range(self.sea_level, noise_grass):
                chunk.parent.add_liquid((coords[0], i, coords[1]),  "Water")

        chunk.add_preloaded_block("Bedrock", (coords[0], noise_grass-noise_dirt-noise_stone, coords[1]))
        for i in range(noise_grass-noise_dirt-noise_stone, noise_grass-noise_dirt):
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
        for i in range(noise_grass-noise_dirt, noise_grass):
            chunk.add_preloaded_block("Dirt", (coords[0], i, coords[1]))
        chunk.add_preloaded_block("Grass", (coords[0], noise_grass, coords[1]))

        if abs(self.noise.noise2(coords[0] / 1000, coords[1] / 1000)) * 10 < 0.4 and abs(self.noise.noise2(coords[0] / 1000, coords[1] / 1000)) * 10 > 0.5:
            self.parent.make_structure((coords[0], noise_grass, coords[1]), "BirchTree", chunk)
        elif abs(self.noise.noise2(coords[0] / 1000, coords[1] / 1000)) * 10 < 0.5:
            self.parent.make_structure((coords[0], noise_grass, coords[1]), "OakTree", chunk)
