#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : Wed 27 Dec 2017 08:21:59 PM EST
# Modified: Thu 25 Jan 2018 12:06:36 AM EST

from __future__ import print_function

import better_exceptions
import sys
import os.path
import glob
import regex

files = 0
matches = 0

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
            buf = grepFile(p, pattern)
            if buf:
                dbg('file', p)
                print("".join(buf))

    dbg('Final fs', fs)
    global files
    global matches
    dbg('Files', files)
    dbg('Matches', matches)


def grepFile(fileName, pattern):
    ''' TODO: save output into buffer and return buffer then in calling
              function, print file name and buffer '''
    global files
    global matches
    buf = []
    with open(fileName, 'r') as f:
        try:
            files += 1
            for i, line in enumerate(f):
                if pattern.search(line):
                    matches += 1
                    #print("  ", i, line, end='')
                    buf.append('    {}:\t{}'.format(i, line))
        except UnicodeDecodeError:
            pass
    return buf

def main():
    try:
        fs = sys.argv[1]
        pat = sys.argv[2]

        dbg('fs', fs)
        dbg('pat', pat)

        pattern = regex.compile(pat)
        walkDir(fs, pattern)

    except IndexError:
        sys.exit('Usage: {} filespec pattern'.format(sys.argv[0]))


if __name__ == '__main__':
    main()


# Test vectors:
# ./craigs_homework_2.py ~/lang/py
# ./craigs_homework_2.py ~/lang/py/\*\*/\*.py
