from command import Command

#
# The Abstract Intent
# Contains the default methods to define an intent
#
class Intent(object):

    def __init__(self, command):
        super(Intent, self).__init__()
        if type(command) is Command:
            self.command = command # command has to be final function that runs it.

    def hook(self, hook, command):
        pass
        
    def runCommand(self):
        return self.command()