#!/bin/python3

from options import Parser
from shell import BardShell

parser = Parser()
shell = BardShell(parser)

# Get Stdin
shell.get_stdin()

