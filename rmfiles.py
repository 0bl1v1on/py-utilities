import os
import sys
import argparse

# -----------------------------
# FUNCTIONS
# -----------------------------

def remove_file(file_exts, filename):

    if os.path.isfile(filename) and (os.path.splitext(filename)[1][1:].strip().lower() in file_exts):
        os.remove(filename)
        print("removed: {}".format(filename))
        return True
    return False


def remove_from_dir(file_exts, directory):
    '''Removes all files in the specified directory with the specified filename.
       file_extensions: list, directory: string'''

    count = 0
    en_directory = os.fsencode(directory)
    for en_filename in os.listdir(en_directory):
        filename = os.fsdecode(en_filename)
        if (remove_file(file_exts, os.path.join(directory, filename))):
            count = count + 1
        
    print(" - removed {} files".format(count))


def remove_recursively(file_exts, root_dir):
    '''Recursively searches directories beneath the current directory and removes matching files'''

    for root, dirs, filenames in os.walk(root_dir):
        for directory in dirs:
            full_dir = os.path.join(root, directory)
            remove_from_dir(file_exts, full_dir)

# -----------------------------
# MAIN SCRIPT LOGIC
# -----------------------------

parse = argparse.ArgumentParser(description = 'Removes specified files')

parse.add_argument('-r', help = 'perform recursive removal', action = 'store_true')
parse.add_argument('-ext', '--extensions', dest = 'extensions', nargs = '*', help = 'delete files with these extensions. If specifying multiple extensions searate with spaces.', required = True)

args = parse.parse_args()

if args.r:
    remove_recursively(args.extensions, os.getcwd())
else:
    remove_from_dir(args.extensions, os.getcwd())
        