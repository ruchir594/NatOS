class NoPath(Exception):
    def __init__(self, arg):
        self.arg = arg
    def __str__(self):
        return repr(self.arg)

class NoFile(Exception):
    def __init__(self, arg):
        self.arg = arg
    def __str__(self):
        return repr(self.arg)

class suger(object):
    # this class will judge if chatbot object can automate this response

    # Everytime a user query comes in, this class will see if the standard CSV
    # FAQ style query can handle that response, if not, the bot will not respond
    # and maybe a real user can check it out.

    def __init__(self, pathfile = 'undefined'):
        self.conversation_filepath = pathfile

    def spice(self):
        # builds NLTK chatobject like from original CSV
        if self.conversation_filepath == 'undefined':
            raise NoPath('A path is necessary')
        try:
            with open(self.conversation_filepath+'conversation.csv') as fh:
                f = map(lambda x: x.split(","), filter(lambda x: (x != ""), fh.read().split("\n")))
            print f
        except Exception, e:
            raise NoFile(str(e))
