# imports
import logging

# set up logging
logging.basicConfig(level=logging.INFO)


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
