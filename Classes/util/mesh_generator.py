# imports
from pyglet.gl import *
import ctypes
import OpenGL.GL as gl

# inbuilt imports
import Classes as pycraft

def delete_duplicates(list):
    """
    delete_duplicates
    
    * Deletes duplicates from a list
    
    :list: the list to delete duplicates from
    """
    _list = []
    for i in range(len(list)):
        if list[i] not in _list:
            _list.append(list[i])
    return _list

class MeshGenerator:
    def __init__(self, chunk):
        self.parent = chunk
        
    def generate_meshes(self):
        """
        generate_meshes
        
        * generates the meshes for the world
        """
        vertices = []
        for i in self.parent.all_blocks:
            arr = [i[0], i[1], i[2],
                i[0], i[1] + 1, i[2],
                i[0] + 1, i[1] + 1, i[2],
                i[0] + 1, i[1], i[2],
                i[0], i[1], i[2] + 1,
                i[0], i[1] + 1, i[2] + 1,
                i[0] + 1, i[1] + 1, i[2] + 1,
                i[0] + 1, i[1], i[2] + 1]

            vertices.extend(arr)
        
        vertices = delete_duplicates(vertices)
        self.parent.mesh["vertices"] = vertices

        indices = []
        for i in range(0, len(vertices), 6):

            indices.extend([i, i + 1, i + 2, i + 2, i + 3, i])
        indices = delete_duplicates(indices)
        self.parent.mesh["indices"] = indices

        texCoords = []
        for i in range(0, len(vertices), 6):
            texCoords.extend([0, 0, 0, 1, 1, 1, 1, 0])
        texCoords = delete_duplicates(texCoords)
        self.parent.mesh["texCoords"] = texCoords
