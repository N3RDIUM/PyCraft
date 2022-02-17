import Classes as pycraft

class Structure(pycraft.StructureBase):
    def __init__(self, parent, position):
        """
        Tree

        * Tree structure

        :structure_data: data of the structure
        :parent: parent chunk
        """
        super().__init__(parent)

        import random

        self.name = "BirchTree"
        self.position = {"x": position[0], "y": position[1], "z": position[2]}
        self.height = random.randint(7, 10)
        self.leaf_height = random.randint(4,self.height)
        self.side_heights = []
        for i in range (self.leaf_height, self.height):
            self.side_heights.append(random.randint(3, 5))

    def generate(self, *args, **kwargs):
        """
        generate

        * Generates the tree

        :return: None
        """
        if self.generated:
            return
        self._generate_tree()
        self._confirm_generate()

    def _generate_tree(self):
        """
        _generate_tree

        * Generates the tree

        :return: None
        """
        current_sideheight = 0
        for i in range(self.height):
            self.game.add_block("BirchLog", [self.position["x"], self.position["y"] + i, self.position["z"]], self.chunk)
            if i >= self.leaf_height:
                for j in range(-self.side_heights[current_sideheight], self.side_heights[current_sideheight]+1):
                    for k in range(-self.side_heights[current_sideheight], self.side_heights[current_sideheight]+1):
                        if [j,k] != [0,0] or i == self.height - 1:
                            self.game.add_block("BirchLeaves", [self.position["x"]+j, self.position["y"] + i, self.position["z"]+k], self.chunk)
                current_sideheight += 1
    
