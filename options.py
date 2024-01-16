import optparse

class Parser:
    def __init__(self):
        self.parser = optparse.OptionParser()

    def add_options(self):
        self.parser.add_option("-m", "--modes",
                        dest = "modes",
                        default = 'content',
                        help = "Available modes: content, conversation_id, response_id, factualityQueries, textQuery, choices, links, images, code",)
        self.parser.add_option("-p", "--prompt",
                        dest = "prompt",
                        type = 'string',
                        help = "Give a prompt",)
        self.parser.add_option("-i", "--send-sysinfo",
                        action = 'store_true',
                        dest = "send_sysinfo",
                        default = False,
                        help = "Whether to send the system Information (default: False)",)
        self.parser.add_option("-w", "--send-pwd",
                        action = 'store_true',
                        dest = "send_pwd",
                        default = False,
                        help = "Whether to send the Present working Directory (default: False)",)
        self.parser.add_option("-s", "--show-prompt",
                        action = 'store_true',
                        dest = "show_prompt",
                        default = False,
                        help = "Whether to show the prompt passed in (default: False)",)

        return self.parser.parse_args()
