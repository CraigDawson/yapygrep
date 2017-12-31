#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : Wed 27 Dec 2017 08:21:59 PM EST
# Modified: Thu 28 Dec 2017 12:20:35 AM EST

from __future__ import print_function

import better_exceptions
import sys
import os.path
import glob
import regex


def dbg(prefix, item):
    print(prefix + ':', item)


def walkDir(fileSpec, pattern):
    fs = os.path.expanduser(fileSpec)
    dbg('fs/expanduser', fs)

    fs = os.path.expandvars(fs)
    dbg('fs/expandvars', fs)

    if os.path.isdir(fs):
        dbg('fs', 'adding "/**" to dir')
        fs += '/**'
    # Not dir and no wildcard at end then append '**' ???
    #elif not fs.endswith('*'):
    #    fs += '**'

    base = os.path.basename(fs)
    dbg('base', base)

    path = os.path.dirname(fs)
    dbg('path', path)

    for p in glob.iglob(fs, recursive=True):
        if os.path.isfile(p):
            dbg('file', p)
            grepFile(p, pattern)

    dbg('Final fs', fs)


def grepFile(fileName, pattern):
    with open(fileName, 'r') as f:
        try:
            for i, line in enumerate(f):
                if pattern.match(line):
                    print("  ", i, line, end='')
        except UnicodeDecodeError:
            pass

def main():
    try:
        fs = sys.argv[1]
        dbg('fs', fs)

        pattern = regex.compile(r'.*with')
        walkDir(fs, pattern)

    except IndexError:
        sys.exit('Usage: {} filespec'.format(sys.argv[0]))


if __name__ == '__main__':
    main()


# Test vectors:
# ./craigs_homework_2.py ~/lang/py
# ./craigs_homework_2.py ~/lang/py/\*\*/\*.py
