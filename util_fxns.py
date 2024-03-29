'''
utility functions for general use
Author: William Wright
'''

import os
import inspect
import logging

import boto3
import progressbar

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


def create_directory(folders, logger=None):
    '''create_directory docstring'''
    for folder in folders:
        try:
            os.mkdir(folder)
        except FileExistsError as e:
            if logger:
                logger.info(e)
            else:
                print(e)


def upload_to_s3(path_output, bucket_name, key_path, logger=None):
    '''
    path_output: local dir file path 
    bucket_name: name of s3 bucket 
    key_path: key path + file name = object name
    '''
    file_name = path_output.split('/')[-1]
    object_name = key_path + '/' + file_name
    s3 = boto3.client('s3')
    # statinfo = os.stat(path_output)
    # if logger:
    #     logger.info('uploading file:\t' + file_name)
    #     logger.info('uploading destination:\t' + object_name)

    # up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
    # up_progress.start()

    # def upload_progress(chunk):
    #     up_progress.update(up_progress.currval + chunk)

    s3.upload_file(path_output,
                   bucket_name,
                   object_name)
                   # ,
                   # Callback=upload_progress)
    # up_progress.finish()


def upload_to_s3_v2(local_path: str, bucket_name: str, object_name: str):
    '''
    path_output: local dir file path 
    bucket_name: name of s3 bucket 
    key_path: key path + file name = object name
    '''
    s3 = boto3.client('s3')
    response = s3.upload_file(local_path,
                               bucket_name,
                               object_name)
    return response
