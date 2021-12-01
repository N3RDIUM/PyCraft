def add_block(type, coords, parent):
    """
    Adds a block to the world at the given coordinates.
    :coords: coordinates to add the block at
    """
    # Add the block to the chunk
    parent.parent.add_block(coords, type, parent)

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

    for index, item in world._all_blocks.items():
        if index[1] == x and index[2] == z:
            # If the block is a block, add it to the list
            blocks.append(item)
    # Now get the highest block
    block = None

    for item in blocks:
        if block is None:
            block = item
        elif block.block_data['pos']['y'] < item.block_data['pos']['y']:
            block = item

    print(block)
    # Return the highest block
    return block

def clear_area(world, size, coords):
    for i in range(size[0]+coords[0]):
        for j in range(size[1]+coords[1]):
            for k in range(coords[2], get_highest_block(world, i, k).block_data['pos']['y']):
                remove_block(world, (i, j, k))