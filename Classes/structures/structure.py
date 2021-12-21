import Classes as pycraft

class StructureBase:
    """
    StructureBase

    * Base class for all structures
    """
    def __init__(self, parent):
        """
        StructureBase.__init__

        :structure_data: data of the structure
        :parent: parent chunk
        """
        self.name = None
        self.chunk = parent
        self.generated = False
        self.game = pycraft

    def _confirm_generate(self):
        """
        generate

        * Generates the structure

        :return: None
        """
        self.generated = True

def load_structures(world):
    """
    load_structures

    * Loads all structures
    """
    import os
    import importlib

    _ = {}

    for file in os.listdir("Classes/structures/structures"):
        if file.endswith(".py") and file != "__init__.py":
            _[file[:-3].split('.py')[0]] = importlib.import_module("Classes.structures.structures." + file[:-3]).Structure
    return _
