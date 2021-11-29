import logging
logging.basicConfig(level=logging.INFO)


def log(source, message):
    logging.info(f'(info) [{source}]: {message}')


def info(source, message):
    logging.info(f'(info) [{source}]: {message}')


def warn(source, message):
    logging.warning(f'(warning) [{source}]: {message}')


def error(source, message):
    logging.error(f'(error) [{source}]: {message}')


def critical(source, message):
    logging.critical(f'(critical) [{source}]: {message}')
