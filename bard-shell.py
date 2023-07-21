#!/bin/python3

import re
from bardapi import Bard
from requests import options
from options import Parser
import os
import sys

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

modes = options.modes.split(',')
for m in modes:
    check_mode(m)

def generate_prompt():
    info = ''
    # if options.shell:
    info = 'OS Information: '
    with os.popen('neofetch --off --color_blocks off') as process:
        info += process.read() + '\n'
    info += '''Take my system Information into consideration before giving outputs.
If the command output is not empty, use it as the input to perform operations.
Do what the Prompt says with the input.\n\n'''

    if stdin == '':
        p = 'Prompt:\n' + options.prompt
    else:
        p = 'Command Output:\n' + stdin + '\nPrompt:\n' + options.prompt + '\n'

    print('Getting Bard Response..')

    prompt = str(info) + str(p)
    print(prompt)
    return prompt

# Get token
token = 'XwhHybTuH8jrTIIShLF1Ye_lhk1F-XxncqdhD7ftrqgegWPHF5XcSz3sIFnGJD7etQRXXg.'
print('Initialzing..')
bard = Bard(token=token)

def code_exec(code):
    if not code:
        print('Code is null')
        return
    

    # yn = input('[E]dit,[R]un,[A]bort: ')
    yn = 'r'
    yn = yn.lower() if len(yn) > 0 else 'e'

    filename = '/tmp/bard_code'

    print(re.search('```.*', code))

    if yn == 'a':
        return

    elif yn == 'e':
        with open(filename, 'w') as f:
            f.write(code)
        os.system(f'nvim {filename}')
        return

    elif yn == 'r':
        with open(filename, 'w') as f:
            f.write(code)

        os.system(f'chmod +x {filename} && sh {filename}')

# while True:
# Get Response for this
response = bard.get_answer(generate_prompt())

code_exists = False
for key in modes:
    if key == 'code':
        code_exists = True
    print(key.title(), end=': \n')
    print(response[key], end='\n\n')
    pass

if code_exists:
    code_exec(response['code'])

# if input('Continue conversation(Y/n)? ').lower() != 'y':
    # break
