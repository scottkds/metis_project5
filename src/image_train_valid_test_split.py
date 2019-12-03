import os
import shutil
from math import floor
from random import shuffle
import sys


def split(source, dest, split_portion=0.8):
    """Takes a "source" directory with image files in a directories reflecting
    their classes labels, and copies them to the "dest" directory into subdireftories
    named train, valid, and test, and places the files in the directories refelcting
    their classes."""

    dirs = os.listdir(source)

    for dir in dirs:
        # Make new destination train, valid, and test directories:
        for directory in ['train', 'valid', 'test']:
            new_directory = os.path.join(dest, directory, dir)
            if not os.path.exists(new_directory):
                os.makedirs(new_directory)
        # Get files
        files = os.listdir(os.path.join(source, dir))
        shuffle(files)
        n_train = floor(len(files) * split_portion)
        n_valid = ((len(files) - n_train) // 2)
        n_test = len(files) - n_train - n_valid
        print(dir, n_train, n_valid, n_test)
        for idx, file in enumerate(files):
            # print(dir, file)
            if idx < n_train:
                shutil.copy2(os.path.join(source, dir, file), os.path.join(dest, 'train', dir))
            elif idx >= n_train and idx < n_train + n_valid:
                shutil.copy2(os.path.join(source, dir, file), os.path.join(dest, 'valid', dir))
            else:
                shutil.copy2(os.path.join(source, dir, file), os.path.join(dest, 'test', dir))
    return None

if __name__ == '__main__':
    source = sys.argv[1]
    dest = sys.argv[2]
    if len(sys.argv) > 3:
        split_portion = float(sys.argv[3])
        split(source, dest, split_portion)
    else:
        split(source, dest)
