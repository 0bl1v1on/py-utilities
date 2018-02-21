'''Exports rescaled icons at various resolutions for Android and iOS apps.'''

import os
from os import path

# https://pypi.python.org/pypi/python-resize-image
from PIL import Image
from resizeimage import resizeimage


__image__ = 'image.png'


# ----------------------------------
# FUNCTIONS
# ----------------------------------


def ensure_dir(directory):

    if not os.path.exists(directory):
        os.makedirs(directory)

def export(subdir, filename, size):

    ensure_dir(subdir)

    fd_img = open(__image__, 'r')
    img = Image.open(fd_img)

    img = resizeimage.resize('contain', img, [size, size])
    img.save(path.join(subdir, filename), img.format)

    fd_img.close()

def export_android():

    subdir = 'Android'

    default = path.join(subdir, 'drawable')
    hdpi = path.join(subdir, 'drawable-hdpi')
    mdpi = path.join(subdir, 'drawable-mdpi')
    xhdpi = path.join(subdir, 'drawable-xhdpi')
    xxhdpi = path.join(subdir, 'drawable-xxhdpi')
    xxxhdpi = path.join(subdir, 'drawable-xxxhdpi')

    export(default, 'icon.png', 72)
    export(hdpi, 'icon.png', 72)
    export(mdpi, 'icon.png', 48)
    export(xhdpi, 'icon.png', 96)
    export(xxhdpi, 'icon.png', 144)
    export(xxxhdpi, 'icon.png', 192)

    export(subdir, 'Google Play Store.png', 192)

def export_ios():

    subdir = 'iOS'

    export(subdir, 'Icon-20.png', 20)
    export(subdir, 'Icon-20@2x.png', 40)
    export(subdir, 'Icon-20@3x.png', 60)
    
    export(subdir, 'Icon-20.png', 29)
    export(subdir, 'Icon-29@2x.png', 58)
    export(subdir, 'Icon-29@3x.png', 87)
    
    export(subdir, 'Icon-40.png', 40)
    export(subdir, 'Icon-40@2x.png', 80)
    export(subdir, 'Icon-40@3x.png', 120)

    export(subdir, 'Icon-50.png', 50)
    export(subdir, 'Icon-50@2x.png', 100)

    export(subdir, 'Icon-57.png', 57)
    export(subdir, 'Icon-57@2x.png', 114)

    export(subdir, 'Icon-60@2x.png', 120)
    export(subdir, 'Icon-60@3x.png', 180)

    export(subdir, 'Icon-72.png', 72)
    export(subdir, 'Icon-72@2x.png', 144)

    export(subdir, 'Icon-76.png', 76)
    export(subdir, 'Icon-76@2x.png', 152)

    export(subdir, 'Icon-167.png', 167)

    export(subdir, 'iTunesArtwork.png', 512)
    export(subdir, 'iTunesArtwork@2x.png', 1024)


# ----------------------------------
# MAIN LOGIC
# ----------------------------------


print('\nBegin exporting...')

export_android()
export_ios()

print('Complete!\n')

