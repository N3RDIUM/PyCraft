import Classes.util.structure_util as util

class StructureBase:
    def __init__(self, structure_data, parent):
        """
        StructureBase

        * Base class for all structures

        :structure_data: data of the structure
        :parent: parent chunk
        """
        self.structure_data = {
            "structure_pos": structure_data["structure_pos"],
            "parent": parent,
        }
        self.chunk = parent
        self.generated = False
        self.util = util

    def _confirm_generate(self):
        """
        generate

        * Generates the structure

        :return: None
        """
        self.generated = True

all_structures = {}

class birch_tree(StructureBase):
    def __init__(self, structure_data, parent):
        """
        Tree

        * Tree structure

        :structure_data: data of the structure
        :parent: parent chunk
        """
        super().__init__(structure_data, parent)

        import random

        self.structure_data["structure_type"] = "tree"
        self.structure_data["structure_name"] = "birch_tree"
        self.height = random.randint(5,6)
        self.leaf_height = random.randint(2,3)
        self.side = random.randint(1,2)

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
        for i in range(self.height):
            self.util.add_block("birch_log", [self.structure_data["structure_pos"]["x"], self.structure_data["structure_pos"]["y"] + i, self.structure_data["structure_pos"]["z"]], self.chunk)
            if i >= self.leaf_height:
                for j in range(-self.side, self.side+1):
                    for k in range(-self.side, self.side+1):
                        if [j,k] != [0,0] or i == self.height - 1:
                            self.util.add_block("birch_leaves", [self.structure_data["structure_pos"]["x"]+j, self.structure_data["structure_pos"]["y"] + i, self.structure_data["structure_pos"]["z"]+k], self.chunk)

all_structures["birch_tree"] = birch_tree
