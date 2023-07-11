#!/bin/python3

import re
from bardapi import Bard
import optparse
import os
import sys

if not sys.stdin.isatty():
    stdin = sys.stdin.read()
    sys.stdin.flush()
else:
    stdin = ''
    print('No Stdin')

parser = optparse.OptionParser()

# add options
parser.add_option("-m", "--modes",
                  dest = "modes",
                  default = 'content',
                  help = "Available modes: content, conversation_id, response_id, factualityQueries, textQuery, choices, links, images, code",)
parser.add_option("-s", "--shell",
                  action = "store_false",
                  dest = "shell",
                  default = True,
                  help = "Give output as shell scripts",)

(options, args) = parser.parse_args()

all_modes = ['content', 'conversation_id', 'response_id', 'factualityQueries', 'textQuery', 'choices', 'links', 'images', 'code']
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
    info += "Take my system Information into consideration if necessary.\n" 
    info += stdin

    p = input('Enter Prompt: ') + '\n'
    print('Getting Bard Response..')

    prompt = info + p
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
    

    yn = input('[E]dit,[R]un,[A]bort: ')
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

while True:
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

    if input('Continue conversation(Y/n)? ').lower() != 'y':
        break
