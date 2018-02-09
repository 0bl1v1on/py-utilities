import argparse
import os
import sys

from os.path import isfile, join, splitext


# -----------------------------
# FUNCTIONS
# -----------------------------


def remove_file(file_exts, filename):
    '''Provided a list of file extensions and a file, returns whether the file ends in one of the extensions.'''

    if isfile(filename) and (splitext(filename)[1][1:].strip().lower() in file_exts):
        os.remove(filename)
        print("removed: {}".format(filename))
        return True
    return False


def remove_from_dir(file_exts, directory):
    '''Removes all files in the specified directory with the specified filename.
       file_extensions: list, directory: string'''

    count = 0
    for filename in os.listdir(directory):
        if remove_file(file_exts, join(directory, filename)):
            count = count + 1

    print(" - removed {} files".format(count))


def remove_recursively(file_exts, root_dir):
    '''Recursively searches directories beneath the current directory and removes matching files'''

    for root, dirs, filenames in os.walk(root_dir):
        for directory in dirs:
            full_dir = join(root, directory)
            remove_from_dir(file_exts, full_dir)


# -----------------------------
# MAIN SCRIPT LOGIC
# -----------------------------


parse = argparse.ArgumentParser(description='Removes specified files')

parse.add_argument('-r', help='perform recursive removal', action='store_true')
parse.add_argument('-ext', '--extensions', dest='extensions', nargs='*', help='delete files with these extensions. If specifying multiple extensions searate with spaces.', required=True)

args = parse.parse_args()

# Clean arguments
exts = []
for ext in args.extensions:
    exts.append(ext.lower())

print('\nArguments:')
print(' - recursive: {}'.format(args.r))
print(' - extensions: {}'.format(exts))

print('\nBegin...')

if args.r:
    remove_recursively(exts, os.getcwd())
else:
    remove_from_dir(exts, os.getcwd())

print('End\n')