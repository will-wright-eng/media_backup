'''
utility functions for general use
Author: William Wright
'''

import inspect
import logging


def function_logger(file_level, console_level=None, function_name=None):
    '''function_logger docstring'''
    if function_name == None:
        function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)
    logger.setLevel(logging.DEBUG)  #By default, logs all messages

    if console_level != None:
        ch = logging.StreamHandler()  #StreamHandler logs to console
        ch.setLevel(console_level)
        ch_format = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    fh = logging.FileHandler("{0}.log".format(function_name))
    fh.setLevel(file_level)
    fh_format = logging.Formatter(
        '%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)
    return logger


def create_directory(folders):
    '''create_directory docstring'''
    for folder in folders:
        try:
            os.mkdir(folder)
        except FileExistsError as e:
            print(e)
