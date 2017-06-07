class suger(object):
    # this class will judge if chatbot object can automate this response

    # Everytime a user query comes in, this class will see if the standard CSV
    # FAQ style query can handle that response, if not, the bot will not respond
    # and maybe a real user can check it out.

    def __init__(self, incoming):
        self.qry=incoming

    def spice(self, botobj, msg):
        #botobj: NLTK Chat object object
        # msg: incoming text message
        
