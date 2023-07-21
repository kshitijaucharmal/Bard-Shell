import optparse

class Parser:
    def __init__(self):
        self.parser = optparse.OptionParser()

    def add_options(self):
        self.parser.add_option("-m", "--modes",
                          dest = "modes",
                          default = 'content',
                          help = "Available modes: content, conversation_id, response_id, factualityQueries, textQuery, choices, links, images, code",)
        self.parser.add_option("-s", "--shell",
                          action = "store_false",
                          dest = "shell",
                          default = True,
                          help = "Give output as shell scripts",)
        self.parser.add_option("-p", "--prompt",
                          dest = "prompt",
                          type = 'string',
                          help = "Give output as shell scripts",)

        return self.parser.parse_args()
