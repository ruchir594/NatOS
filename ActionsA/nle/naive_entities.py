from __future__ import print_function
import re
import json
import pickle
import sys
import urllib
sys.path.insert(0, './head')
from geotext import GeoText
import nltk
from nltk.tag.hunpos import HunposTagger
from nltk.tokenize import word_tokenize


class stamps:
    def __init__(self, name, aliner):
        self.protagonist = name
        # a proper noun

        self.number = [] #
        # 2.4, 3.5

        self.datetime = []
        # datetime, like, tomorrow at 3 PM, June 3 2016

        self.day = [] #
        # tuesday, today, tomorrow, sunday

        self.time = [] #
        # 6 PM, 12 Noon

        self.amount_of_money = []
        # $40, 35 pounds

        self.duration = [] #
        # 30 mins, 2 hours, 4 days

        self.distance = []

        self.email = []

        self.url = []

        self.phone_number = []

        self.quantity = []
        # any units other than time, like grams, kmph

        self.reminder = [] #
        # reminder on or off, for snooze

        self.reminder_text = []
        # what would be reminded about, this text should be generated while making
        # above "True"

        self.foreign_word = []
        # words that cannot be tagger by a traditional tagger

        self.aliner = aliner
        # just full text

        self.bagged = []
        # words that may be important and could be used by KGB but don't seem to fit anywhere

        self.checked = None

    def view(self):
        print ("self.protagonist```````", self.protagonist + "]")
        print ("self.number````````````", self.number)
        #print ("self.datetime``````````", self.datetime)
        print ("self.day``````````", self.day)
        print ("self.time`````````", self.time)
        print ("self.amount_of_money```", self.amount_of_money)
        print ("self.duration `````````", self.duration)
        print ("self.distance `````````", self.distance)
        print ("self.email`````````````", self.email)
        print ("self.url```````````````", self.url)
        print ("self.phone_number``````", self.phone_number)
        print ("self.quantity``````````", self.quantity)
        print ("self.reminder``````````", self.reminder)
        print ("self.reminder_text`````", self.reminder_text)
        #print ("self.location``````````", self.location)
        print ("self.aliner````````````", self.aliner + "]")
        #print ("self.message_text``````", self.message_text)
        print ("self.foreign_word``````", self.foreign_word)
        print ("self.checked```````````", self.checked)

    def view_return(self):
        return str({
         "self.protagonist```````": self.protagonist,
         "self.number````````````": self.number,
         "self.datetime``````````": self.datetime,
         "self.day``````````": self.day,
         "self.time`````````": self.time,
         "self.amount_of_money```": self.amount_of_money,
         "self.duration `````````": self.duration,
         "self.distance `````````": self.distance,
         "self.email`````````````": self.email,
         "self.url```````````````": self.url,
         "self.phone_number``````": self.phone_number,
         "self.quantity``````````": self.quantity,
         "self.reminder``````````": self.reminder,
         "self.reminder_text`````": self.reminder_text,
         "self.message_text``````": self.message_text,
         "self.location``````````": self.location,
         "self.foreign_word``````": self.foreign_word,
         "self.checked```````````": self.checked
         })

    d1 = ['i', 'live', 'in', 'please', 'hi', 'give', 'find', 'who', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you', \
            'want', 'to', 'eat', 'like','liked', 'I', 'can', 'you', 'suggest', 'of', 'is', 'are', 'near', 'there', 'some', \
            'little', 'now', 'wanna', 'want', 'at', 'on', 'in', 'near', 'area', 'next', 'and', 'how', 'about', 'or', \
            'the', 'a', 'an', 'about', 'for', 'with', 'should', 'could', 'would', 'out','time','person','year','way','day',\
            'thing','man','world','life','hand','part','child','eye','woman','place','work','week', 'doing',\
            'case','point','government','company','number','group','problem','fact','be','have','do','say',\
            'get','make','go','know','take','see','come','think','look','want','give','use','find','tell', 'telling',\
            'ask','work','seem','feel','try','leave','call','good','new','first','last','long','great','little','own','other',\
            'old','right','big','high','different','small','large','next','early','young','important','few',\
            'public','bad','same','able','to','of','in','for','on','with','at','by','from','up','about','into',\
            'over','after','beneath','under','above','the','and','a','that','I','it','not','he','as','you', \
            'this','but','his','they','her','she','or','an','will','my','one','all','would','there','their', 'talk', \
            'talking', 'love', 'loved', 'hello', 'help', 'helping', 'helped', 'pleasure', 'bye', 'goodbye', 'care', 'later', \
            'no','nothing', 'thanks', 'welcome', 'something', 'hey', 'am', 'month','year','week','day','hour','minute','min','second', \
            'months','years','weeks','days','hours','minutes','mins','seconds','time', 'today', 'tomorrow', 'am', 'pm',\
            'january', 'febuary', 'marth', 'april', 'may', 'june', 'july','august', 'september', 'october', 'november', 'december', \
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','km', 'kilometer', 'kilometers', 'meter', 'm',\
            'cm', 'kms', 'miles', 'yards', 'feet', 'feets','evening', 'morning', 'afternoon', 'noon', 'night']
            
    def fill_init(self):

        duration_text = ['month','year','week','day','hour','minute','min','second', \
                        'months','years','weeks','days','hours','minutes','mins','seconds']
        day_text = ['today', 'tomorrow', 'yesterday',\
                        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        datenum_text = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',\
                        'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen','sixteen',\
                        'seventeen', 'eighteen', 'nineteen', 'twenty']
        month_text = ['january', 'febuary', 'marth', 'april', 'may', 'june', 'july', \
                    'august', 'september', 'october', 'november', 'december']
        time_text = ['am', 'pm', 'noon']
        distance_text = ['km', 'kilometer', 'kilometers', 'meter', 'm', 'cm', 'kms', 'miles', 'yards', 'feet', 'feets']
        amount_of_money = ['usd', 'dollar', 'dollars', 'euro', 'pound', 'pounds', 'euros', 'rupee', 'rupees', 'rs']

        b = self.getWords(aliner)

        self.checked = [False] * len(b)

        i=0
        for i in range(len(b)):
            if b[i] in day_text:
                self.day_text.append(b[i])
                self.checked[i] = True


    def fill_rest(self):
        to_fill_quant = ['NNS', 'NNPS', 'NNP', 'NN']
        day_text = ['today', 'tomorrow', 'january', 'febuary', 'marth', 'april', 'may', 'june', 'july', \
                    'august', 'september', 'october', 'november', 'december', \
                    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        time_text = ['evening', 'morning', 'afternoon', 'noon', 'night']



    def completia(self):


    def just_location_plus(self):
        c = getWords_special_location(self.aliner)
        a = ''
        for c_cmall in c:
            if c_cmall not in d1:
                a = a + c_cmall.title() + ' '
            else:
                a = a + c_cmall + ' '
        #print a
        potentiav = GeoText(a)
        b1 = potentiav.cities
        b2 = potentiav.countries
        c = self.location
        self.location = []
        self.location = self.location + b1
        self.location = self.location + b2

    def uniquefy(self):
        self.location = uniquefy_p(self.location)
        self.day = uniquefy_p(self.day)
        self.time = uniquefy_p(self.time)

    def baggage(self):
        b = self.message_text
        for i in range(len(self.checked)):
            if self.checked[i] is False:
                if b[i][0] not in self.location and b[i][0] not in d1:
                    self.baggage.append(b[i][0])
                    self.checked[i] = True



####################################################################
def getWords_x(data):
    return re.compile(r"[\w'/.@-]+").findall(data)
def getWords(data):
    return re.compile(r"[\w']+").findall(data)
def getWords_special_location(data):
    return re.compile(r"[\w'/.,-@]+").findall(data)
def uniquefy(a):
    b=[]
    for i in a:
        if i not in b:
            b.append(i)
    return b
####################################################################
def uniquefy_p(a):
    b=[]
    for i in a:
        if i.lower() not in b:
            b.append(i.lower())
    return b
####################################################################
####################################################################
####################################################################
#################################################################################
def ner_primitive(event):
    '''Provide an event that contains the following keys:
      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    love = str(event)

    ####################################################################
    q=[]
    demo = stamps("yesminister",love)
    demo.fill_init()
    demo.fill_rest()
    demo.just_location_plus()
    demo.uniquefy()
    #demo.baggage()
    ####################################################################
    return demo
