#!/bin/python3

from options import Parser
from shell import BardShell

parser = Parser()
shell = BardShell(parser)

# Setup token
shell.setup_token()

# Get Stdin
shell.get_stdin()

# Setup Modes
shell.setup_modes()

# Get Response from bard
shell.get_response()

# Show the response
shell.show_response()
