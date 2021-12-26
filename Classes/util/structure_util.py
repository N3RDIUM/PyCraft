# imports
import opensimplex

# Inbuilt imports
import Classes as pycraft

def add_block(type, coords, chunk):
    """
    Adds a block to the world at the given coordinates.

    :type: type of block to add
    :coords: coordinates to add the block at
    :chunk: chunk to add the block to
    """
    # Add the block to the chunk
    chunk.add_preloaded_block(type, coords)

def remove_block(world, coords):
    """
    Removes a block from the world at the given coordinates.
    :coords: coordinates to remove the block at
    """
    # Remove the block from the world
    world.remove_block(coords)

def get_highest_block(world, x, z):
    """
    Gets the highest block at the given x,z coordinates.
    :x: x coordinate
    :z: z coordinate

    :return: highest block at the given coordinates
    """
    return round(pycraft.lerp(world._noise.noise2d(x/10, z/10) * 2, world._noise.noise2d(x/100, z/100) * 10, world._noise.noise2d(x/500, z/500) * 50))

def clear_area(world, size, coords):
    for i in range(coords[0] - size[0], coords[0] + size[0]):
        for j in range(coords[1] - size[1], coords[1] + size[1]):
            for k in range(coords[2], get_highest_block(world, i, j)):
                remove_block(world, (i, k, j))
