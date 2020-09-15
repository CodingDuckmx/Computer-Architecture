#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) == 2:

    program = sys.argv[1]

else:

    program = None
    print('-----------------------------------')
    print('A default program will be executed.')
    print('-----------------------------------')

cpu = CPU()

cpu.load(program)
cpu.run()