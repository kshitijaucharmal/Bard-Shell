import re
from bardapi import Bard
import os
import sys
import toml

class BardShell:
    def __init__(self, parser):
        self.all_modes = ['content', 'conversation_id', 'response_id', 'factualityQueries', 'textQuery', 'choices', 'links', 'images', 'code']
        self.stdin = ''
        self.modes = []
        self.parser = parser
        (self.options, self.args) = self.parser.add_options()
        self.response = dict() # the raw response sent by bard
        pass

    def setup_token(self, configfile='~/.config/bardshell/bard.toml'):
        print('Initializing....')
        config = toml.load(os.path.expanduser(configfile))
        self.token = config['user']['token']

        # Give the token to bard
        self.bard = Bard(token=self.token)
        print('Done.')
        pass

    def get_stdin(self):
        # Get stdin output
        if not sys.stdin.isatty():
            self.stdin = sys.stdin.read()
            sys.stdin.flush()
            pass

    # Method to check if given modes are Available
    def check_mode(self, mode):
        e = mode in self.all_modes
        if not e:
            print(f'Error: {e} is not in Available Modes\n')
            self.parser.print_help()
            exit()

    def setup_modes(self):
        # Get all modes
        self.modes = self.options.modes.split(',')
        # Check if these modes exist
        if len(self.modes) == 0:
            self.modes.append('content')
        for m in self.modes:
            self.check_mode(m)

    def generate_prompt(self):
        info = ''

        # Get os info from neofetch
        info = 'OS Information: '

        # Get neofetch info
        with os.popen('neofetch --off --color_blocks off') as process:
            info += process.read()
        # Get pwd info
        info += 'Present Working Directory:\n' + os.getcwd() + '\n\n'

        # Prompt to give bard all the info it might need
        info += 'Instructions:\nTake my system Information into consideration if necessary before giving outputs.'
        info += 'If the command output is not empty, use it as the input to perform operations.'
        info += 'Do what the Prompt says with the input.\n\n'

        # If There is no stdin pass the prompt as normal
        if self.stdin == '':
            p = 'Prompt:\n' + self.options.prompt
        else:
            p = 'Command Output:\n' + self.stdin + '\nPrompt:\n' + self.options.prompt + '\n'

        prompt = str(info) + str(p)

        if self.options.show_prompt:
            print(prompt)
        return prompt

    # Function to execute code
    def code_exec(self, code):
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
        pass

    def get_response(self):
        print('Fetching Bard\'s response...')
        # Get Response for the prompt
        final_prompt = self.generate_prompt()
        self.response = self.bard.get_answer(final_prompt)
        pass

    def show_response(self):
        # If code exists
        code_exists = False
        for key in self.modes:
            # And user asking for code
            if key == 'code':
                code_exists = True
            print(key.title(), end=': \n')
            print(self.response[key], end='\n\n')
            pass

        # Run code-exec if asked for code
        if code_exists:
            self.code_exec(self.response['code'])
        pass
