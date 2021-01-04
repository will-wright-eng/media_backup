''' main.py docstring

Author: William Wright
Date: 2021-01-03
'''

import os
import sys
import threading
import shutil

import logging
import inspect

import progressbar
import boto3
import configparser

import util_fxns as utilf

logger = utilf.function_logger(logging.DEBUG,
                               logging.DEBUG,
                               function_name='media_backup')


def zip_process(cwd, file_name):
    zip_dir = os.path.join(cwd, file_name)
    zip_file = os.path.join(cwd, file_name.replace('.', '_').replace(' ', '_'))
    return shutil.make_archive(zip_file, 'zip', zip_dir)


def import_configs():
    config = configparser.ConfigParser()
    config.read('project.cfg')
    config_s3 = dict(config.items('s3_info'))
    config_dir = dict(config.items('dir_info'))
    return config_s3['bucket'], config_s3['key_path'], config_dir[
        'media_dir'], config_dir['move_to']


def upload_to_s3(path_output, bucket_name, key_path):
    '''upload_to_s3 docstring'''
    file_name = path_output.split('/')[-1]
    object_name = key_path + '/' + file_name
    s3 = boto3.client('s3')
    statinfo = os.stat(path_output)
    logger.info('uploading file:\t' + file_name)
    logger.info('uploading destination:\t' + object_name)

    up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
    up_progress.start()

    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)

    s3.upload_file(path_output,
                   bucket_name,
                   object_name,
                   Callback=upload_progress)
    up_progress.finish()


def move_uploaded_file(cwd, file_name, move_to):
    utilf.create_directory([move_to], logger)
    os.rename(cwd + '/' + file_name, cwd + '/' + move_to + '/' + file_name)


def main():
    bucket_name, key_path, media_dir, move_to = import_configs()
    files = os.listdir(media_dir)
    remove_files = [
        i for i in files
        if (i[0] == '_') or (i[0] == '.') or ('Untitled' in i) or ('.zip' in i)
    ]
    file_list = [i for i in files if i not in remove_files][:10]

    for file_name in file_list:
        logger.info(file_name)
        logger.info('compressing')
        path_output = zip_process(media_dir, file_name)

        upload_to_s3(path_output, bucket_name, key_path)
        logger.info('upload complete')
        move_uploaded_file(media_dir, file_name, move_to)
        move_uploaded_file(media_dir, path_output.split('/')[-1], move_to)

    logger.info('program successful')
    return 0


if __name__ == '__main__':
    main()
