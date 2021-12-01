def add_block(world, type, coords):
    """
    Adds a block to the world at the given coordinates.
    :coords: coordinates to add the block at
    """
    # Get the suitable chunk coords and check if the chunk is loaded and exists
    chunk_coords = [round(coords[0]/world.CHUNK_DIST), round(coords[2]/world.CHUNK_DIST)]
    if world.chunk_exists(chunk_coords):
        # Get the chunk
        chunk = world.get_chunk(chunk_coords)
        # Add the block to the chunk
        chunk.add_block(type, {'pos': {'x': coords[0], 'y': coords[1], 'z': coords[2]}}, coords)

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
    # First get all the blocks at the given coordinates
    blocks = []

    for i in world._all_blocks:
        if i.block_data['pos']['x'] == x and i.block_data['pos']['z'] == z:
            # If the block is a block, add it to the list
            blocks.append(i)

    # Now sort the list by the y coordinate
    blocks.sort(key=lambda x: x.block_data['pos']['y'])

    # Return the highest block
    return blocks[-1]

def clear_area(world, size, coords):
    for i in range(size[0]+coords[0]):
        for j in range(size[1]+coords[1]):
            for k in range(coords[2], get_highest_block(world, i, k).block_data['pos']['y']):
                remove_block(world, (i, j, k))
