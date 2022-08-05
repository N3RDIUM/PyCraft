# imports
import logging

# set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def log(source, message):
    """
    log

    * Logs a message

    :source: the source of the message
    :message: the message to log
    """
    info(source, message)


def info(source, message):
    """
    info

    * Logs an info message

    :source: the source of the message
    :message: the message to log
    """
    logging.info(f'(info) [{source}]: {message}')


def warn(source, message):
    """
    warn

    * Logs a warning message

    :source: the source of the message
    :message: the message to log
    """
    logging.warning(f'(warning) [{source}]: {message}')


def error(source, message):
    """
    error

    * Logs an error message

    :source: the source of the message
    :message: the message to log
    """
    logging.error(f'(error) [{source}]: {message}')


def critical(source, message):
    """
    critical

    * Logs a critical message

    :source: the source of the message
    :message: the message to log
    """
    logging.critical(f'(critical) [{source}]: {message}')

def log_vertex_addition(data, bytes, vertex_length, texcoord_length, left_to_add):
    """
    vertex_addition

    * Logs an addition of vertex data to the VBO from the thread

    :data: a tuple of the vertex data
    :bytes: the number of bytes of the data
    """
    info('TerrainRenderer', f"Vertices@{bytes[0]} TexCoords@{bytes[1]} | vertex data: {vertex_length} bytes | texcoord data: {texcoord_length} bytes | Scheduled: {left_to_add}")
