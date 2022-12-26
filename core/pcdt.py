# imports
import zlib


def pcdt_decompress(data):
    """
    Decompresses a PCDT chunk.

    BTW, PCDT stands for "PyCraft Data".
    """
    return zlib.decompress(data)


def pcdt_compress(data):
    """
    Compresses a PCDT chunk.

    BTW, PCDT stands for "PyCraft Data".
    """
    return zlib.compress(data)


def open_pcdt(filename):
    """
    Opens a PCDT file.

    BTW, PCDT stands for "PyCraft Data".
    """
    with open(filename, "rb") as f:  # Open the file
        return pcdt_decompress(f.read())


def save_pcdt(filename, data):
    """
    Saves a PCDT file.

    BTW, PCDT stands for "PyCraft Data".
    """
    with open(filename, "wb") as f:  # Open the file
        f.write(pcdt_compress(data))
