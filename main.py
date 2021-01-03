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

import function_logger as fl

logger = fl.function_logger(logging.DEBUG,
                            logging.DEBUG,
                            function_name='media_backup')

def zip_process(cwd,filename):
    zip_dir = os.path.join(cwd, filename)
    zip_file = os.path.join(cwd, filename.replace('.','_').replace(' ','_'))
    path_output = shutil.make_archive(zip_file, 'zip', zip_dir)
    return path_output

def import_configs():
    config = configparser.ConfigParser()
    config.read('project.cfg')
    bucket_name = config['s3_info']['bucket']
    key_name = config['s3_info']['key_path']
    media_dir = config['s3_info']['media_dir']
    return bucket_name, key_name, media_dir

def upload_to_s3(file_name, bucket_name, key_name):
    key = key_name + '/' + file_name
    s3 = boto3.client('s3')
    statinfo = os.stat(file_name)
    up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
    up_progress.start()
    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)
    s3.upload_file(file_name, bucket_name, key, Callback=upload_progress)
    up_progress.finish()

def move_uploaded_file(cwd,filename):
    # move files
    # make directory if it doesn't exist
    folder_moveto = '_uploaded_to_s3'
    os.rename(cwd+'/'+filename,cwd+'/'+folder_moveto+'/'+filename)

def main():
	bucket_name, key_name, media_dir = import_configs()
	files = os.listdir(media_dir)
	remove_files = [i for i in files if (i[0]=='_') or (i[0]=='.') or ('Untitled' in i) or ('.zip' in i)]
	file_list = [i for i in files if i not in remove_files][:5]

	for file_name in file_list:
		logger.info(file_name)
		logger.info('compressing')
		path_output = zip_process(media_dir, file_name)
		logger.info('start upload of '+path_output)
		upload_to_s3(path_output, bucket_name, key_name)
		logger.info('upload complete')
		move_uploaded_file(media_dir, file_name)
		move_uploaded_file(media_dir, path_output)

	logger.info('program successful')
	return 0

if __name__ == '__main__':
	main()