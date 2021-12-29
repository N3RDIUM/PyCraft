import Classes as pycraft

class Liquid(pycraft.Liquid):
    def __init__(self, parent):
        super().__init__("Water", parent)

        self.texture_still = self.parent.textures["water_still"]
        self.texture_flow = self.parent.textures["water_flow"]
