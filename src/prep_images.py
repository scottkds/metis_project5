from glob import glob
import re
from collections import defaultdict
import os
import os.path
from math import floor
from random import shuffle
import shutil

# Random  tests
floor(0.8)
floor(1.2)
floor(3.5)
os.path.expanduser('~')

def create_dir(path, name):
    path = os.path.expanduser(path)
    if path[-1] != '/':
        path += '/'
        full_path = path + name
    else:
        full_path = path + name
    if not os.path.exists(full_path):
        try:
            os.makedirs(full_path)
        except:
            print('Nope to {} !'.format(full_path))
            raise
            return False
    return full_path

def count_and_sort_glyphs(train_dir, test_dir, valid_dir, split=0.8, min_count=10):
    """Copies train and test data to appropriate directories"""
    check_paths('~/p5')
    counts = defaultdict(int)
    file_paths = defaultdict(list)
    glyph = re.compile(r'_([A-Z]\d+)\.')
    names = glob('/Users/scott/p5/data/raw/Preprocessed/**/*.png')
    shuffle(names)
    for name in names:
        file_name = name.split('/')[-1]
        m = glyph.search(file_name)
        if m:
            counts[m.group(1)] += 1
            file_paths[m.group(1)].append(name)
        else:
            counts['unknown'] += 1
            file_paths['unknown'].append(name)
    del file_paths['unknown']
    for key, val in file_paths.items():
        n_glyphs = counts[key]
        n_train = floor(n_glyphs * split)
        n_test = (n_glyphs - n_train) // 2
        n_valid = n_glyphs - n_train - n_test
        if n_glyphs > min_count:
            train_glyph = create_dir(train_dir, key)
            test_glyph = create_dir(test_dir, key)
            valid_glyph = create_dir(valid_dir, key)
            for idx, file in enumerate(val):
                if idx < n_train:
                    shutil.copy2(file, train_glyph)
                elif idx >= n_train and idx < n_train + n_test:
                    shutil.copy2(file, test_glyph)
                else:
                    shutil.copy2(file, valid_glyph)
    return counts

def check_paths(project_path):
    """Checks project paths for train and test data. Creates those paths if they
    don't exist."""
    full_path = os.path.expanduser(project_path)
    train = full_path + '/data/interim/train'
    test = full_path + '/data/interim/test'
    valid = full_path + '/data/interim/valid'
    if not os.path.exists(train):
        try:
            os.makedirs(train)
        except:
            print('Nope to train data!')
            raise
            return False
    if not os.path.exists(test):
        try:
            os.makedirs(test)
        except:
            print('Nope to test data!')
            raise
            return False
    if not os.path.exists(valid):
        try:
            os.makedirs(valid)
        except:
            print('Nope to train data!')
            raise
            return False
    return (train, test, valid)
check_paths('~/p5')


!pwd

if __name__ == '__main__':
    train_dir, test_dir, valid_dir = check_paths('~/p5')
    counts = count_and_sort_glyphs(train_dir, test_dir, valid_dir)
    total = 0
    i = 1
    print(type(counts))
    for key, val in counts.items():
        if val >= 20:
            print(i, '::', key, '::', val)
            total += val
            i += 1
    print(total)
