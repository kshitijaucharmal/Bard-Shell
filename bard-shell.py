#!/bin/python3

import re
from bardapi import Bard
from requests import options
from options import Parser
import os
import sys
import toml

# Initialize options
p = Parser()
(options, args) = p.add_options()
parser = p.parser

# Modes possible
all_modes = ['content', 'conversation_id', 'response_id', 'factualityQueries', 'textQuery', 'choices', 'links', 'images', 'code']

# Get stdin output
if not sys.stdin.isatty():
    stdin = sys.stdin.read()
    sys.stdin.flush()
    pass
else:
    stdin = ''
    print('No Stdin')

# Method to check if given modes are Available
def check_mode(mode):
    e = mode in all_modes
    if not e:
        print(f'Error: {e} is not in Available Modes\n')
        parser.print_help()
        exit()
    return e

# Get all modes
modes = options.modes.split(',')
# Check if these modes exist
for m in modes:
    check_mode(m)

def generate_prompt():
    info = ''

    # Get os info from neofetch
    info = 'OS Information: '

    # Get neofetch info
    with os.popen('neofetch --off --color_blocks off') as process:
        info += process.read() + '\n'
    # Get pwd info
    info += 'Present Working Directory:\n' + os.getcwd() + '\n'

    # Prompt to give bard all the info it might need
    info += '''Instructions:\nTake my system Information into consideration before giving outputs.
If the command output is not empty, use it as the input to perform operations.
Do what the Prompt says with the input.\n\n'''

    # If There is no stdin pass the prompt as normal
    if stdin == '':
        p = 'Prompt:\n' + options.prompt
    else:
        p = 'Command Output:\n' + stdin + '\nPrompt:\n' + options.prompt + '\n'

    print('Getting Bard Response..')

    prompt = str(info) + str(p)
    print(prompt)
    return prompt

# Function to execute code
def code_exec(code):
    if not code:
        print('Code is null')
        return

    # This is not working, just running the script for now
    # yn = input('[E]dit,[R]un,[A]bort: ')
    yn = 'r'
    yn = yn.lower() if len(yn) > 0 else 'e'

    # File to store code
    filename = '/tmp/bard_code'

    # Search for code in content
    print(re.search('```.\S', code))

    # Abort
    if yn == 'a':
        return

    # Edit
    elif yn == 'e':
        with open(filename, 'w') as f:
            f.write(code)
        os.system(f'nvim {filename}')
        return

    # Execute code
    elif yn == 'r':
        with open(filename, 'w') as f:
            f.write(code)

        os.system(f'chmod +x {filename} && sh {filename}')

# Bard works here
# ----------------------------------------------------------------------------------------------------------
# Get token
config = toml.load(os.path.expanduser('~') + '/.config/bardshell/bard.toml')
token = config['user']['token']

# Give the token to bard
bard = Bard(token=token)

# Get Response for the prompt
final_prompt = generate_prompt()
response = bard.get_answer(final_prompt)
# ----------------------------------------------------------------------------------------------------------

# If code exists
code_exists = False
for key in modes:
    # And user asking for code
    if key == 'code':
        code_exists = True
    print(key.title(), end=': \n')
    print(response[key], end='\n\n')
    pass

# Run code-exec if asked for code
if code_exists:
    code_exec(response['code'])
