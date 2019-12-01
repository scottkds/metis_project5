import cv2
import os
import sys
from random import randint
from glob import glob

SRC = os.path.expanduser(sys.argv[1])
DATADIR = os.path.expanduser(sys.argv[2])

print('Image File:', SRC)
print('Data directory:', DATADIR)

def get_files(path):
    if os.path.isfile(os.path.expanduser(path)):
        return [os.path.expanduser(path)]
    else:
        return glob(os.path.join(os.path.expanduser(path), '*.jpg'))
get_files('~/p5/data/images')
get_files('~/p5/mvp.ipynb')

def create_dirs(path, subdir):
    path = os.path.expanduser(path)
    if not os.path.exists(os.path.join(path, subdir)):
        os.makedirs(os.path.join(path, subdir))
    return os.path.join(path, subdir)
create_dirs('~/junk', 'thumbs')

def create_images(source, dest, subdir):
    file_name_gen = (str(i) for i in range(10000000))
    full_dest = create_dirs(dest, subdir)

    # for file in get_files(source):
    #     create_dirs ....................
    for file in get_files(source):
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        height, width = img.shape
        window_height = 40
        window_width = 40
        print(width, height)
        x = 0
        y = 0
        while y < height - window_height:
            while x < width - window_width:
                print((x, y))
                crop_img = img[y:y+window_height, x:x+window_width].copy()
                # Draw a diagonal blue line with thickness of 5 px
                # disp_img = cv2.line(crop_img.copy(),(20,0),(20,40),(0,255,255), 1)
                # disp_img = cv2.line(disp_img,(0,20),(40,20),(0,255,255), 1)
                # cv2.imshow("cropped", disp_img)
                # k = cv2.waitKey(50)
                filename = 'img_{0}_x_{1}_y_{2}_'.format(next(file_name_gen), x + 20, y + 20)
                file = os.path.join(full_dest, filename + '.png')
                print(file)
                cv2.imwrite(file, crop_img)
                cv2.destroyAllWindows()
                disp_img = None
                x += 5
            x = 0
            y += 5

if __name__ == '__main__':
    create_images(SRC, DATADIR, 'thumbs')
