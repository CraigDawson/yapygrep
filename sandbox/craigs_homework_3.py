#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Created : Wed 04 Apr 2018 08:49:43 PM EDT
# Modified: Wed 04 Apr 2018 09:16:22 PM EDT

import better_exceptions
import json
import pprint


types = {

    'py' : ['py'],
    'c' : ['c', 'h'],
    'cpp' : ['cpp', 'cc', 'cxx', 'm', 'hpp', 'hh', 'h', 'hxx']
}

fileName = 'types.json'
with open(fileName, 'w') as f:
    json.dump(types, f, indent=4, separators=(',', ': '))

with open(fileName, 'r') as f:
    tests = json.load(f)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(tests)
