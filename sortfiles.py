import argparse
import datetime
import os
import shutil
import sys

from os.path import dirname, exists, isfile, join, splitext


__staging_gnd__ = 'staging'
__dest_dir__ = ''


# -----------------------------
# FUNCTIONS
# -----------------------------


def get_filename(directory, modified, fileno, ext):
    '''Generates a filename using the provided paramters'''
    moddatetime = modified.strftime('%Y%m%d_%H%M%S')
    if fileno > 1:
        outname = '{}_{}{}'.format(moddatetime, fileno, ext)
    else:
        outname = '{}{}'.format(moddatetime, ext)

    return join(directory, modified.strftime('%Y'), str(outname))

def ensure_path(filepath):
    '''Ensures that the destination directy exists, creating it if necessary.'''
    directory = dirname(filepath)
    if not exists(directory):
        os.makedirs(directory)
        print('----- Creating directory: {} -----'.format(directory))

def sort_file(filepath):
    '''Names and moves the specified file into a sorted location'''
    statbuf = os.stat(filepath)
    modified = datetime.datetime.fromtimestamp(statbuf.st_mtime)
    
    fileno = 1
    name, ext = splitext(filepath)

    fullname = get_filename(__dest_dir__, modified, fileno, ext)
    ensure_path(fullname)

    # Ensure that we won't have conflicting filenames
    if exists(fullname):
        while exists(get_filename(__dest_dir__, modified, fileno, ext)):
            fileno += 1
        fullname = get_filename(__dest_dir__, modified, fileno, ext)

    # Output modified time + original filepath 
    print('{}\t{}'.format(str(modified).ljust(26), filepath))

    # Use copy2 to maintain metadata
    shutil.copy2(filepath, fullname)

def sort(directory):
    '''Sorts all files within the specified directory'''
    for filename in os.listdir(directory):
        fullpath = join(directory, filename)
        if isfile(fullpath):
            sort_file(fullpath)

def sort_recursively(directory):
    '''Sorts all files within the specified directory, recursively traversing any subfolders'''
    for root, directories, filenames in os.walk(directory):
        for dir in directories:
            fulldir = join(root, dir)
            for filename in os.listdir(fulldir):
                fullpath = join(fulldir, filename)
                if isfile(fullpath):
                    sort_file(fullpath)

def run(directory, recursive):
    if recursive:
        sort_recursively(directory)
    else:
        sort(directory)


# -----------------------------
# MAIN SCRIPT LOGIC
# -----------------------------


desc = 'Organises and names files into a chronological format.'
usag = '''Simply calling with no arguments will perform non-recursive sorting of the current directory, sorting into a subfolder of the current directory.
       Add additional arguments to customise behaviour.'''

parse = argparse.ArgumentParser(description=desc, usage=usag)

parse.add_argument('-r', help='perform recursive sorting', action='store_true')
parse.add_argument('-s', '--sources', dest='sources', nargs='*', help='list of specific source folders to sort', required=False)
parse.add_argument('-d', '--destination', dest='dest', help='the destination folder into which files will be sorted', required=False)

args = parse.parse_args()

# Set up args
__dest_dir__ = args.dest if args.dest else join(os.getcwd(), __staging_gnd__)
sources = args.sources
recursive = args.r

# Helpful output
print('\nArguments:')
print(' - recursive: ' + str(recursive))
print(' - destination: ' + __dest_dir__)
if sources:
    print(' - sources:')
    for folder in sources:
        print('     ' + folder)

print('\nBegin...')

# Process each source dir if specified,
# otherwise use the current dir.
if sources:
    for folder in sources:
        run(folder, recursive)
else:
    run(os.getcwd(), recursive)

print('End\n')






# LASTLY: Retain meta data