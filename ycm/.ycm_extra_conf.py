#!/usr/bin/python3

import os
from os import path

def is_headerfile(filename):
    """True if filename has an acceptable header file extension"""
    _,ext = path.splitext(filename)
    header_extensions = {'.h',   # C
                         '.hh',  # C++
                         '.hpp',
                         '.hxx'}
    
    return True if ext in header_extensions else False


def get_header_dirs(project_root, *names):
    """Get list of directories to containing header files.

    The caller can specify an arbitrary number of directory names
    for consideration. The function will then ONLY consider the
    specified directories. Otherwise, if no directory is specified,
    this function will scan every single directory, recursively,
    and record each directory that contains header files (see
    is_headerfile() above).
    """
    names_ = set(names)   # faster lookup
    dirset = set()        # keep paths unique

    for root, dirs, files in os.walk(project_root, False):

        # only consider directories specified by caller
        if names and path.basename(root) in names:
            dirset.add(path.abspath(root))
        # otherwise, add all directories that have header files
        elif not names:
            for file in files:
                if is_headerfile(file):
                    dirset.add(path.abspath(root))

    return list(dirset)


def get_flags_for_file(filename):
    """Return a list of compiler flags depending on the filename extension.

    C files are normally compiled with different flags from C++ files, for example.
    This function tries to be smart and figure out whether the file is a C or C++
    file and return an appropriate list of compiler flags. If the extension is not
    that of a C or C++ file (or another language this function has a list of flags for),
    an empty list is returned.
    """
    _,ext = path.splitext(filename)
    
    # convert the many C++ acceptable extensions to '.cxx'
    cxx_ext = '.cxx'
    cxx_extensions = {'.cxx', '.cpp', '.cc'}
    if ext in cxx_extensions:
        ext = cxx_ext

    flags = {
        '.c' : [
            '-xc',
            '-g',
            '-Wall',
            '-Wextra',
            '-Werror',
            '-std=c11',
            '-pedantic',
            '-fstrict-aliasing',
            '-Wcast-align=strict',
            '-O3'
            ],
        '.cxx' : [
            '-xc++',
            '-g',
            '-Wall',
            '-Wextra',
            '-Werror',
            '-std=c++11',
            '-pedantic',
            '-fstrict-aliasing',
            'Wcast-align=strict',
            '-O3'
            ]
        }

    return flags.get(ext, [])


def FlagsForFile(filename, *args, **kwargs):
    """YCM calls this hook to get a list of compilation flags for a given file"""

    # this file MUST be in the root of a (e.g. git) project!
    PROJECT_ROOT = path.abspath(path.dirname(__file__))
    includes = ["-I" + d for d in get_header_dirs(PROJECT_ROOT)]
    flags = get_flags_for_file(filename)
    flags += includes

    return { 'flags': flags, 'do_cache': True }


if __name__ == '__main__':
    import sys
    if (len(sys.argv) != 2):
        print(f"USAGE: {sys.argv[0]} <filename>, where filename is a file to get compilation flags for.")
        sys.exit(1)
    print(FlagsForFile(sys.argv[1]))
