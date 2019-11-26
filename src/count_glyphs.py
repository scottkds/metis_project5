from glob import glob
import re
from collections import defaultdict

def count_glyphs():
    counts = defaultdict(int)
    glyph = re.compile(r'_([A-Z]\d+)\.')
    names = glob('/Users/scott/p5/data/raw/Preprocessed/**/*.png')
    names = [f.split('/')[-1] for f in names]
    names
    for name in names:
        m = glyph.search(name)
        if m:
            counts[m.group(1)] += 1
    return counts



if __name__ == '__main__':
    counts = count_glyphs()
    total = 0
    i = 1
    for key, val in counts.items():
        if val >= 50:
            print(i, '::', key, '::', val)
            total += val
            i += 1
    print(total)
