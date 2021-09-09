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

import configparser

import util_fxns as utilf

name = 'media_backup'
logger = utilf.function_logger(logging.DEBUG,
                               logging.DEBUG,
                               function_name=name)


def zip_process(cwd, file_name):
    zip_dir = os.path.join(cwd, file_name)
    zip_file = os.path.join(cwd, file_name.replace('.', '_').replace(' ', '_'))
    return shutil.make_archive(zip_file, 'zip', zip_dir)


def import_configs():
    config = configparser.ConfigParser()
    config.read('project.cfg')
    configs = dict(config.items('media_s3_info'))
    return configs['s3_bucket'], configs['s3_key_path'], configs[
        'local_dir'], configs['local_move_to']


def move_uploaded_file(cwd, file_name, move_to):
    utilf.create_directory([cwd + '/' + move_to], logger)
    os.rename(cwd + '/' + file_name, cwd + '/' + move_to + '/' + file_name)


def main():
    bucket_name, key_path, media_dir, move_to = import_configs()
    files = os.listdir(media_dir)
    remove_files = [
        i for i in files
        if (i[0] == '_') or (i[0] == '.') or ('Untitled' in i) or ('.zip' in i)
    ]
    file_list = [i for i in files if i not in remove_files]
    flag_nozip = False
    for file_name in file_list:
        logger.info(file_name)
        logger.info('compressing')
        
        try:
            path_output = zip_process(media_dir, file_name)
        except NotADirectoryError as e:
            flag_nozip = True
            path_output = os.path.join(media_dir, file_name)
            logger.info(e)
        utilf.upload_to_s3(path_output, bucket_name, key_path, logger)
        logger.info('upload complete')

        if flag_nozip:
            flag_nozip = False
        else:
            move_uploaded_file(media_dir, file_name, move_to)
        move_uploaded_file(media_dir, path_output.split('/')[-1], move_to)

    logger.info('program successful')
    return 0


if __name__ == '__main__':
    main()
