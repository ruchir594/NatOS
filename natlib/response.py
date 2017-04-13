class Response(object):
    # Idea is we can send in message in a response, 
    # and the response can then be handled in different ways via this interface
    def __init__(self, message):
        self.message = message

    # Hooks to the text to speech API to say things
    def speak(self):
        pass

    def say(self):
        print(self.message)
