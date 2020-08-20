#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

cpu = CPU()

cpu.load("/Users/TOrtiz/Documents/git/Computer-Architecture/ls8/examples/stack.ls8")
cpu.run()
