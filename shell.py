import re
from bardapi import Bard
import os
import sys
import toml

class BardShell:
    def __init__(self, parser, configfile='~/.config/bardshell/bard.toml'):
        self.all_modes = ['content', 'conversation_id', 'response_id', 'factualityQueries', 'textQuery', 'choices', 'links', 'images', 'code']
        self.stdin = ''
        self.modes = []
        self.parser = parser
        (self.options, self.args) = self.parser.add_options()
        self.response = dict() # the raw response sent by bard

        self.config = toml.load(os.path.expanduser(configfile))
        self.token = self.config['user']['token']
        pass

    def color_text(self, text, color):
        color_codes = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
        }

        print(color_codes[color] + text + "\033[0m")


    def setup_token(self):
        self.color_text('Initializing....', 'green')
        # Give the token to bard
        if self.token[-1] != '.':
            self.color_text('Invalid token given, check the config file', 'red')
            exit()
        self.bard = Bard(token=self.token)
        self.color_text('Done.', 'yellow')
        pass

    def get_stdin(self):
        # Get stdin output
        if not sys.stdin.isatty():
            self.stdin = sys.stdin.read()
            pass

    # Method to check if given modes are Available
    def check_mode(self, mode):
        e = mode in self.all_modes
        if not e:
            self.color_text(f'Error: {e} is not in Available Modes\n', 'red')
            self.parser.print_help()
            exit()

    def setup_modes(self):
        # Get all modes
        self.modes = self.options.modes.split(',')
        # Check if these modes exist
        if len(self.modes) == 0:
            self.modes = self.config['default']['modes'].split(',')
        for m in self.modes:
            self.check_mode(m)

    def generate_prompt(self, prompt):
        info = ''

        # Get neofetch info
        if self.options.send_sysinfo:
            info += 'OS Information: '
            with os.popen('neofetch --off --color_blocks off') as process:
                info += process.read()

        # Get pwd info
        if self.options.send_pwd:
            info += 'Present Working Directory:\n' + os.getcwd() + '\n\n'

        # Prompt to give bard all the info it might need
        instructions = ''
        if 'code' in self.modes:
            instructions = self.config['prompt']['code']
        else:
            instructions = self.config['prompt']['normal']
        info += instructions

        # If There is no stdin pass the prompt as normal
        if self.stdin == '':
            p = 'Prompt:\n' + prompt
        else:
            p = 'Command Output:\n' + self.stdin + '\nPrompt:\n' + prompt + '\n'

        final_prompt = str(info) + str(p)

        if self.options.show_prompt:
            print(final_prompt)
        return final_prompt

    # Function to execute code
    def code_exec(self, content):
        # File to store code
        filename = '/tmp/bard_code'

        written = False
        while True:
            # Search for code in content
            all_codes = re.split('```.*\n', content)
            code = ''
            for i in range(1, len(all_codes), 2):
                code += all_codes[i]

            print(code)

            if code == '':
                self.color_text('No Code recieved.', 'red')
                return
            
            self.color_text('[E]dit,[R]un,[C]lear,[W]rite,[A]bort: ', 'yellow')
            yn = input()
            yn = yn.lower() if len(yn) > 0 else 'e'

            if not written:
                with open(filename, 'w') as f:
                    f.write(code)
                written = True

            # Abort
            if yn == 'a':
                break

            if yn == 'c':
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')


            # Edit
            elif yn == 'e':
                os.system(f'$EDITOR {filename}')
                with open(filename, 'r') as f:
                    code = f.read()

            # Execute code
            elif yn == 'r':
                os.system(f'chmod +x {filename} && sh {filename}')
                break
            
            # Write to a file
            elif yn == 'w':
                path = input('Enter path to save script[Default: ~/myscript.sh]: ')
                if path == '':
                    path = '~/myscript.sh'
                path = os.path.expanduser(path)
                with open(path, 'w') as f:
                    f.write(code)
                self.color_text(f'Written to {path}', 'green')
        pass

    def get_response(self):
        new_prompt = self.options.prompt
        while True:
            if not new_prompt:
                try:
                    new_prompt = input('>> ')
                except Exception:
                    exit()
                if new_prompt == 'exit':
                    return
            self.color_text('Fetching Bard\'s response...', 'yellow')
            # Get Response for the prompt
            final_prompt = self.generate_prompt(new_prompt)
            try:
                self.response = self.bard.get_answer(final_prompt)
            except Exception as e:
                self.color_text(str(e), 'red')
                continue
            # Show response
            self.show_response()

            new_prompt = None


    def show_response(self):
        # If code exists
        code_exists = False
        for key in self.modes:
            # And user asking for code
            if key == 'code':
                code_exists = True
                continue
            print(key.title(), end=': \n')
            print(self.response[key], end='\n\n')
            pass

        # Run code-exec if asked for code
        if code_exists:
            self.code_exec(self.response['content'])
        pass
