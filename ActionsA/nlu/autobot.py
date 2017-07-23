import re
from prepro import latentify, distance, distance2
import word2vec
import json

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

def getWordsX(data):
    return re.compile(r"[\w'.*]+").findall(data)

class suger(object):
    # this class will judge if chatbot object can automate this response
    
    # Everytime a user query comes in, this class will see if the standard CSV
    # FAQ style query can handle that response, if not, the bot will not respond
    # and maybe a real user can check it out.

    def __init__(self, pathfile = 'undefined'):
        self.conversation_filepath = pathfile
        self.parts = []

    def spice(self):
        # builds NLTK chatobject like from original CSV

        model = word2vec.load('./ActionsA/latents.bin')

        data = {}

        if self.conversation_filepath == 'undefined':
            raise NoPath('A path is necessary')

        try:
            with open(self.conversation_filepath+'conversation.csv') as fh:
                f = map(lambda x: x.split(","), filter(lambda x: (x != ""), fh.read().split("\n")))
            for each in f:
                words = getWordsX(each[0])
                x=[]
                for y in words:
                    x.extend(y.split('*'))
                features = latentify(x, model)
                data[each[0]] = features
            #print data
            with open(self.conversation_filepath+'feature_file.txt', 'w') as outfile:
                json.dump(data, outfile)

        except Exception, e:
            raise NoFile(str(e))


    def salt(self):
        print '\nfrom salt !!!!!', '\n'
        model = word2vec.load('./ActionsA/latents.bin')
        with open(self.conversation_filepath+'conversation.csv') as fh:
            f = map(lambda x: x.split(","), filter(lambda x: (x != ""), fh.read().split("\n")))
        for each in f:
            print distance(each[0],'very well said i bet but i need more beer', model)

    def chef(self, dish):
        # dish: a string
        # this is where every incoming message comes in dish variable.
        # this method will do latent features mapping to judge if bot can answer
        # this incoming string well or not.

        model = word2vec.load('./ActionsA/latents.bin')

        j=[]
        with open(self.conversation_filepath+'conversation.csv') as fh:
            f = map(lambda x: x.split(","), filter(lambda x: (x != ""), fh.read().split("\n")))
        for each in f:
            # Calling distance, and calculating distance of incoming dish string to all other
            # responses in conv.csv
            j.append((each[0], distance(each[0],dish, model)))
        return j
