import os
from os.path import join, getsize, isfile, split

import argparse


DIRPATH = '.'
SIZE_WIDTH = 15
STD_WIDTH = 5


# -----------------------------
# FUNCTIONS
# -----------------------------


def get_disp_size(bytesize):
    if bytesize < 1000:
        return ' {:7.3f} B'.format(bytesize)
    elif bytesize < 1000000:
        return ' {:7.3f} KB'.format(bytesize/1000)
    elif bytesize < 1000000000:
        return ' {:7.3f} MB'.format(bytesize/1000000)
    else:
        return ' {:7.3f} GB'.format(bytesize/1000000000)


# -----------------------------
# MAIN SCRIPT LOGIC
# -----------------------------


parse = argparse.ArgumentParser(description='Lists files in directories')

parse.add_argument('-r', help='perform recursive search', action='store_true')
parse.add_argument('-s', help='display sizes', action='store_true')

args = parse.parse_args()

# Extract arguments
recursive = args.r
show_size = args.s

print()

if recursive:
    for root, dirs, files in os.walk(DIRPATH):
        if show_size:
            print(''.ljust(SIZE_WIDTH) + root)
        else:
            print(''.ljust(STD_WIDTH) + root)

        for name in files:
            head, tail = split(root)
            if show_size:
                size = getsize(join(root, name))
                disp_size = get_disp_size(size).ljust(SIZE_WIDTH)
                print(disp_size + ''.ljust(len(head) + 1) + name)
            else:
                print(''.ljust(len(head) + 1) + name)
        
else:
    for name in os.listdir(DIRPATH):
        if show_size:
            absname = join(DIRPATH, name)
            if isfile(absname):
                disp_size = get_disp_size(getsize(join(DIRPATH, name))).ljust(SIZE_WIDTH)
                print(disp_size + name)
            else:
                print(''.ljust(SIZE_WIDTH - 2) + '• ' + name)
        else:
            print(''.ljust(STD_WIDTH) + name)

print()