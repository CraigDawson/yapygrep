#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : Wed 27 Dec 2017 08:21:59 PM EST
# Modified: Thu 28 Dec 2017 12:20:35 AM EST

from __future__ import print_function

import better_exceptions
import sys
import os.path
import glob


def dbg(prefix, item):
    print(prefix + ':', item)


def main():
    try:
        fs = sys.argv[1]
        dbg('fs', fs)

        fs = os.path.expanduser(fs)
        dbg('fs/expanduser', fs)

        fs = os.path.expandvars(fs)
        dbg('fs/expandvars', fs)

        if os.path.isdir(fs):
            dbg('fs', 'adding "/**" to dir')
            fs += '/**'
        # Not dir and no wildcard at end then append '**' ???
        elif not fs.endswith('*'):
            fs += '**'

        base = os.path.basename(fs)
        dbg('base', base)

        path = os.path.dirname(fs)
        dbg('path', path)

        for p in glob.iglob(fs, recursive=True):
            if os.path.isfile(p):
                dbg('file', p)

        dbg('Final fs', fs)

    except IndexError:
        sys.exit('Usage: {} filespec'.format(sys.argv[0]))


if __name__ == '__main__':
    main()

# Test vectors:
#./craigs_homework.py '$HOME/*/py'
#./craigs_homework.py '$HOME/*/py/*.t?t'
#./craigs_homework.py '~'
#./craigs_homework.py ..
