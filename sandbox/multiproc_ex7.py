# File to test multiprocessor algorithm
# Has simple dir and file functions

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import current_process, cpu_count
from time import time
import os
import hashlib


def doFiles(files, dir):
    """
    Processes list files
    :param files: list of files to process
    :param dir: directory files are in
    :return: None
    """
    for file in files:
        f = dir + '/' + file
        # print('f - {}'.format(f))
        print('{}  {}'.format(hashlib.md5(open(f, 'rb').read()).hexdigest(), f))


def doDir(dir):
    """
    Processes a directory
    :param dir: single directory to process
    :return: tuple with list of dirs and list of files
    """
    files = []
    dirs = []
    for entry in os.listdir(dir):
        if os.path.isfile(dir + '/' + entry):
            files.append(entry)
        elif os.path.isdir(dir + '/' + entry):
            dirs.append(dir + '/' + entry)
        else:
            print('{} is not a file or directory.'.format(entry))
    return (dirs, files)


def printDirs(dir):
    """
    Test function for doDir()
    :param dir: directory to process
    :return: None
    """
    (dirs, files) = doDir(dir)
    for d in dirs:
        print('d - {}'.format(d))
        printDirs(d)
    for f in files:
        print('f - {}/{}'.format(dir, f))


if __name__ == '__main__':
    # printDirs('.')
    dirs = ['.']
    with ProcessPoolExecutor(max_workers=4) as executor:
        for dir in dirs:
            future = executor.submit(doDir, dir)

            (more_dirs, files) = future.result()
            dirs.extend(more_dirs)

            executor.submit(doFiles, files, dir)