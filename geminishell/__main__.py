import google.generativeai as genai
import re
import os
import argparse
import toml
import sys

CONFIG_FILE = '~/.config/bardshell/config.toml'

config = toml.load(os.path.expanduser(CONFIG_FILE))
parser = argparse.ArgumentParser(
prog='Gemini Shell',
description='Powerup your terminal with AI',)

parser.add_argument('-v', '--version', action='store_true', help='Print version info')
parser.add_argument('-i', '--interactive', action='store_true', help='Start a new chat')
parser.add_argument('-p', '--prompt', help='Give a prompt')
parser.add_argument('-m', '--mode', help='available modes: code, text(default)')

args = parser.parse_args()

def color_text(text, color, end='\n'):
    color_codes = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }
    print(color_codes[color] + text + "\033[0m", end=end)

# Setup
genai.configure(api_key=config['api_key'])
model = genai.GenerativeModel(config['model'])

prompt = '''Prompt:'''

def interactive_mode():
    color_text("Starting Chat.. ", 'yellow')
    chat = model.start_chat(history=[])
    while True:
        color_text(">>> ", 'yellow', end='')
        prompt = input()
        if prompt == 'exit':
            break
        response = chat.send_message(prompt, stream=True)
        for chunk in response:
            print(chunk.text)
    pass

if (args.version):
    print(config['version'])
    sys.exit()

# Skip everything if interactive
if (args.interactive):
    interactive_mode()
    sys.exit()

# Exit if no prompt
if (args.prompt == None):
    color_text("Please Provide a prompt.", 'red')
    parser.print_help()
    sys.exit()

def get_code(text):
    code_blocks = re.findall(r"```([^`]*)\n(.*?)```", text, flags=re.DOTALL)
    # Combine
    full_code = ""
    for c in code_blocks[0]:
        full_code += c
    return full_code

def write_code(code, filename):
    code = str(code).splitlines()
    full_code = code[1:]
    language = code[0]
    color_text(f"Language: {language}", 'green')
    with open(filename, 'w') as f:
        f.write("\n".join(full_code))

def get_stdin():
    # Get stdin output
    if not sys.stdin.isatty():
        stdin = sys.stdin.read()
        return '\nStdin: ' + stdin + '\n'
    return ''

# Function to execute code
def code_exec(code):
    # File to store code
    filename = '/tmp/geminicode'

    written = False
    while True:
        # Search for code in content
        print('Code: ')
        print(code)

        if code == '':
            color_text('No Code recieved.', 'red')
            return
        
        color_text('[E]dit,[R]un,[C]lear,[W]rite,[A]bort: ', 'yellow', end='')
        yn = input()
        yn = yn.lower() if len(yn) > 0 else 'a'

        # Abort
        if yn == 'a':
            break

        if not written:
            write_code(code, filename)
            written = True

        if yn == 'c':
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        # Edit
        elif yn == 'e':
            os.system(f'nvim {filename}')
            with open(filename, 'r') as f:
                code = f.read()

        # Execute code
        elif yn == 'r':
            os.system(f'chmod +x {filename} && {filename}')
            break
        
        # Write to a file
        elif yn == 'w':
            path = input('Enter path to save script [Default: ~/myscript.sh]: ')
            if path == '':
                path = '~/myscript.sh'
            path = os.path.expanduser(path)
            with open(path, 'w') as f:
                f.write(code)
            color_text(f'Written to {path}', 'green')
    pass

def code_mode():
    global prompt
    prompt += "\nMode: code"
    prompt += "\nDon't forget to add a shebang to start of each code block"
    response = model.generate_content(prompt)
    try:
        code = get_code(response.text)
    except Exception as e:
        color_text(f'{e} exception occured. Probably no code recieved', 'red')
        sys.exit()
    code_exec(code)
    sys.exit()

def text_mode():
    global prompt
    prompt += get_stdin()
    color_text("Getting Response...", 'yellow')
    response = model.generate_content(prompt)
    response.resolve()
    responsetext = response.text
    while True:
        color_text('Response:\n', 'yellow')
        print(responsetext)
        color_text('[E]dit,[C]learScreen,[W]rite,[A]bort: ', 'yellow', end='')
        cmd = input()
        cmd = cmd.lower() if len(cmd) > 0 else 'a'

        # Edit
        if cmd == 'e':
            filename = '/tmp/geminiresponse'
            with open(filename, 'w') as f:
                f.write(responsetext)
                os.system(f'nvim {filename}')
            with open(filename, 'r') as f:
                responsetext = f.read()
        elif cmd == 'c':
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        # Write to a file
        elif cmd == 'w':
            path = input('Enter path to save script [Default: ~/response.txt]: ')
            if path == '':
                path = '~/response.txt'
            path = os.path.expanduser(path)
            with open(path, 'w') as f:
                f.write(responsetext)
            color_text(f'Written to {path}', 'green')
        else:
            color_text('Successfully Aborted', 'green')
            exit()

    sys.exit()

mode = 'text'
if (args.mode != None):
    mode = args.mode

prompt += str(args.prompt)
if mode == 'code':
    code_mode()
else:
    text_mode()
