def add_to_batch(chunk):
    cdef object c = chunk
    for block, _ in c.blocks.items():
        if _ != None:
            chunk.blocks[block].add_to_batch_and_save()
