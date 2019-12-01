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

def count_glyphs(parent_dir):
    """Counts the hieroglyph images in the parent_dir folder. Returns a dictionary
    with the glyph names as keys and the counts as values."""
    counts = defaultdict(int)
    file_names = defaultdict(list)
    path = os.path.expanduser(parent_dir)
    print(path)
    glyph = re.compile(r'_([A-Z]\d+)\.')
    files = glob(path + '/**/*.png')
    for f in files:
        glyph_name = glyph.search(f)
        if glyph_name:
            counts[glyph_name.group(1)] += 1
            file_names[glyph_name.group(1)].append(f)
        else:
            counts['unknown'] += 1
            file_names['unknown'].append(f)
    return (counts, file_names)
list(count_glyphs('~/p5/data/raw/Preprocessed')[0].items())[:5]

def setup_dirs(parent_dir):
    """Creates train, test, and valid subdirectories in the parent_dir directory"""
    path = os.path.expanduser(parent_dir)
    dirs = ['train', 'test', 'valid', 'enhance']
    if path[-1] != '/':
        dirs = [path + '/' + name for name in dirs]
    else:
        dirs = [path + name for name in dirs]
    for dir in dirs:
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
        except:
            raise
    return True
setup_dirs('~/p5/test')

def check_slashes(path):
    if path[-1] == '/':
        return path
    else:
        return path + '/'

def split_glyphs(source, dest, split=0.8, min_count=50):
    dest = check_slashes(os.path.expanduser(dest))
    source = check_slashes(os.path.expanduser(source))
    try:
        setup_dirs(dest)
    except:
        raise
    glyph_counts, glyph_files = count_glyphs(source)
    print(list(glyph_files.keys())[:8])
    for glyph, cnt in glyph_counts.items():
        if cnt >= min_count:
            n_glyphs = cnt
            n_train = floor(n_glyphs * split)
            n_test = (n_glyphs - n_train) // 2
            n_valid = n_glyphs - n_train - n_test
            files = glyph_files[glyph]
            shuffle(files)
            for idx, file in enumerate(files):
                if idx < n_train:
                    if glyph != 'unknown':
                        shutil.copy2(file, dest + 'train/known/')
                    else:
                        shutil.copy2(file, dest + 'train/unknown')
                elif idx >= n_train and idx < n_train + n_test:
                    if glyph != 'unknown':
                        shutil.copy2(file, dest + 'test/known/')
                    else:
                        shutil.copy2(file, dest + 'test/unknown')
                else:
                    if glyph != 'unknown':
                        shutil.copy2(file, dest + 'valid/known/')
                    else:
                        shutil.copy2(file, dest + 'valid/unknown')
    return True
split_glyphs('~/p5/data/raw/Preprocessed', '~/p5/binary_glyphs')


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

def count_and_sort_glyphs(train_dir, test_dir, valid_dir, split=0.8, min_count=10, min_to_enhance=5):
    """Copies train and test data to appropriate directories"""
    check_paths('~/p5')
    counts = defaultdict(int)
    file_paths = defaultdict(list)
    glyph = re.compile(r'_([A-Z]\d+)\.')
    names = glob('/Users/scott/p5/data/raw/Preprocessed/**/*.png')
    enhance = os.path.expanduser('~/p5/data/interim/enhance')
    if not os.path.exists(enhance):
        os.makedirs(enhance)
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
        if n_glyphs >= min_count:
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
        elif n_glyphs < min_count and n_glyphs >= min_to_enhance:
            glyph_dir = create_dir(enhance, key)
            for idx, file in enumerate(val):
                shutil.copy2(file, glyph_dir)
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
        if val >= 5 and val < 10:
            print(i, '::', key, '::', val)
            total += val
            i += 1
      print(total)
