from __future__ import print_function
import re
import json
import pickle
import sys
import urllib
#import word2vec
sys.path.insert(0, './head')
from geotext import GeoText
import nltk
from nltk.tag.hunpos import HunposTagger
from nltk.tokenize import word_tokenize
#from crf_location import crf_exec

def conver_pos(full_pos):
    a = []
    for each_pos in full_pos:
        if each_pos[1] == 'VERB':
            a.append([each_pos[0], 'VB'])
        elif each_pos[1] == 'NUM':
            a.append([each_pos[0], 'CD'])
        elif each_pos[1] == 'NOUN':
            a.append([each_pos[0], 'NN'])
        elif each_pos[1] == 'ADJ':
            a.append([each_pos[0], 'JJ'])
        else:
            a.append(each_pos)
    return a


#################################################################################
def ner(event, full_pos, full_ents):
    '''Provide an event that contains the following keys:
      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    love = str(event)
    #print (type(love))
    lust = getWords_special_location(love)
    #print (lust)
    #################################################################################
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
    #d1 = []
    kiss = ''
    bang = ''
    bump_last = ['.', ',', ';', ':', '(', ')', '?', '!']
    for c_cmall in lust:
        if c_cmall[-1] not in bump_last:
            if c_cmall not in d1:
                kiss = kiss + c_cmall.title() + ' '
                bang = bang + c_cmall.title() + ' '
            else:
                kiss = kiss + c_cmall + ' '
                bang = bang + c_cmall + ' '
        else:
            if c_cmall not in d1:
                kiss = kiss + c_cmall[:-1].title() + ' '
                bang = bang + c_cmall[:-1].title() + ' ' + c_cmall[-1] + ' '
            else:
                kiss = kiss + c_cmall[:-1] + ' '
                bang = bang + c_cmall[:-1] + ' ' + c_cmall[-1] + ' '
    #################################################################################
    #a = crf_exec(bang, 0)
    b = conver_pos(full_pos)
    data_ayrton = full_ents
    ####################################################################
    q=[]
    demo = stamps("yesminister",data_ayrton,love,b,q)
    demo.fw_dispatch()
    demo.fill_init()
    demo.fill_rest()
    demo.just_location_plus()
    demo.uniquefy()
    #demo.baggage()
    ####################################################################
    return demo


class stamps:
    def __init__(self, name, data_ayrton, aliner, message_text, output_dep):
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

        self.location = data_ayrton
        # SFO, Los Alamos, 22661 Merrick, Long Island

        self.message_text = message_text
        # full message to be stored for future evaluation?, basically POS Tagging

        self.foreign_word = []
        # words that cannot be tagger by a traditional tagger

        self.output_dep = output_dep
        # Full dependency text

        self.aliner = aliner
        # just full text

        self.bagged = []
        # words that may be important and could be used by KGB but don't seem to fit anywhere

        self.checked = None

        self.d1 = ['i', 'live', 'in', 'please', 'hi', 'give', 'find', 'who', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you', \
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
        print ("self.location``````````", self.location)
        print ("self.aliner````````````", self.aliner + "]")
        print ("self.message_text``````", self.message_text)
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

    def fw_dispatch(self):
        i = 0
        a = []
        while i < len(self.message_text):
            #print self.message_text[i]
            if self.message_text[i][1] == 'FW':
                # I have my doubts with this NNS. for string 7th July, ot July 7th; the "7th" is "NNS"
                # so i removed it, it is a small decrepancy but can't take the risk. because all the email
                # will be sparced
                k1 = ''
                k2 = ''
                j = 0
                for j in range(len(self.message_text[i][0])):
                    if self.message_text[i][0][j].isdigit():
                        k1=k1+self.message_text[i][0][j]
                    else:
                        k2=k2+self.message_text[i][0][j:-1]
                        break
                if k1 != '':
                    a.append([k1, 'CD'])
                    a.append([k2, 'NNS'])
                else:
                    a.append(self.message_text[i])
            else:
                a.append(self.message_text[i])
            i=i+1
        self.message_text = a



    def fill_init(self):

        duration_text = ['month','year','week','day','hour','minute','min','second', \
                        'months','years','weeks','days','hours','minutes','mins','seconds']
        datetime_text = ['time', 'today', 'tomorrow', 'am', 'pm',\
                        'january', 'febuary', 'marth', 'april', 'may', 'june', 'july', \
                        'august', 'september', 'october', 'november', 'december', \
                        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_text = ['january', 'febuary', 'marth', 'april', 'may', 'june', 'july', \
                    'august', 'september', 'october', 'november', 'december']
        time_text = ['am', 'pm', 'noon']
        distance_text = ['km', 'kilometer', 'kilometers', 'meter', 'm', 'cm', 'kms', 'miles', 'yards', 'feet', 'feets']
        amount_of_money = ['usd', 'dollar', 'dollars', 'euro', 'pound', 'pounds', 'euros', 'rupee', 'rupees', 'rs']

        b = self.message_text

        self.checked = [False] * len(b)

        #print (b)

        i=0
        for i in range(len(b)):
            b[i][0] = b[i][0].lower()
            if b[i][0] in duration_text:
                if i>0 and b[i-1][1]=='CD' and self.checked[i] == False and self.checked[i-1] == False:
                    #print "found a duration text here " + b[i-1][0] + " " + b[i][0]
                    self.checked[i] = True
                    self.checked[i-1] = True
                    self.duration.append(b[i-1][0] + " " + b[i][0])
            if b[i][0] in day_text:
                if i>0 and b[i-1][1]=='CD' and self.checked[i] == False and self.checked[i-1] == False:
                    #print "found a day text here " + b[i-1][0] + " " + b[i][0]
                    self.checked[i] = True
                    self.checked[i-1] = True
                    self.day.append(b[i-1][0] + " " + b[i][0])
                if i<len(b)-1 and b[i+1][1]=='CD' and self.checked[i] == False and self.checked[i+1] == False:
                    self.checked[i] = True
                    self.checked[i+1] = True
                    self.day.append(b[i][0] + " " + b[i+1][0])
            if b[i][0] in time_text:
                if i>0 and b[i-1][1]=='CD' and self.checked[i] == False and self.checked[i-1] == False:
                    #print "found a time text here " + b[i-1][0] + " " + b[i][0]
                    self.checked[i] = True
                    self.checked[i-1] = True
                    self.time.append(b[i-1][0] + " " + b[i][0])
            if b[i][0] in amount_of_money:
                if i>0 and b[i-1][1]=='CD' and self.checked[i] == False and self.checked[i-1] == False:
                    #print "found a amount of money here " + b[i-1][0] + " " + b[i][0]
                    self.checked[i] = True
                    self.checked[i-1] = True
                    self.amount_of_money.append(b[i-1][0] + " " + b[i][0])
            if b[i][0] in distance_text:
                if i>0 and b[i-1][1]=='CD' and self.checked[i] == False and self.checked[i-1] == False:
                    #print "found a distance here " + b[i-1][0] + " " + b[i][0]
                    self.checked[i] = True
                    self.checked[i-1] = True
                    self.distance.append(b[i-1][0] + " " + b[i][0])
            if b[i][0] == "remind" or b[i][0] == "reminded" or b[i][0] == "reminder":
                #print "reminder at time - day found "
                self.reminder = True
            match = None
            match = re.search(r'[\w\.-]+@[\w\.-]+', b[i][0])
            if match != None:
                #print "found email here " + b[i][0]
                self.email.append(b[i][0])
                self.checked[i] = True
        match = None
        match = re.findall(r'(https?://[^\s]+)', self.aliner)
        if match != []:
            self.url.append(match)
            self.checked[i] = True

    def fill_rest(self):
        to_fill_quant = ['NNS', 'NNPS', 'NNP', 'NN']
        day_text = ['today', 'tomorrow', 'january', 'febuary', 'marth', 'april', 'may', 'june', 'july', \
                    'august', 'september', 'october', 'november', 'december', \
                    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        time_text = ['evening', 'morning', 'afternoon', 'noon', 'night']
        for i in range(len(self.checked)):
            if self.message_text[i][1] in to_fill_quant and i > 0 and self.checked[i] == False and \
               self.checked[i-1] == False and self.message_text[i-1][1]=='CD':
                self.quantity.append(self.message_text[i-1][0] + ' ' + self.message_text[i][0])
                self.checked[i] = True
                self.checked[i-1] = True
            if self.message_text[i][0] in day_text and self.checked[i] == False:
                self.day.append(self.message_text[i][0])
                self.checked[i] = True
            if self.message_text[i][0] in time_text and self.checked[i] == False:
                self.time.append(self.message_text[i][0])
                self.checked[i] = True
        for i in range(len(self.checked)):
            if self.message_text[i][1] == 'CD' and self.checked[i] == False:
                self.number.append(self.message_text[i][0])
                self.checked[i] = True


    def completia(self):
        if self.time is not [] and self.day is [] and self.reminder is True:
            # if we know when the timer is to be set, but don't know on which day
            # then we need to find out.
            i=0
            for i in range(len(self.message_text)):
                if self.message_text[i][0] in day_text and self.checked[i] is False:
                    self.day.append(message_text[i][0])
                    #```````````self.setreminder()`````````````
                    break
        if self.reminder is True and self.duration is []:
            # Ask for reminder
            # Set reminder
            self.reminder = True

    def just_location_plus(self):
        c = getWords_special_location(self.aliner)

        a = ''
        for c_cmall in c:
            if c_cmall not in self.d1:
                a = a + c_cmall.title() + ' '
            else:
                a = a + c_cmall + ' '
        #print a
        potentiav = GeoText(a)
        b1 = potentiav.cities
        b2 = potentiav.countries
        #print ('list of potential countries are',b2)
        c = self.location
        self.location = []
        for ea in c:
            if ea[1] == 'GPE':
                self.location.append(ea[2])
            if ea[1] == 'TIME':
                self.time.append(ea[2])
            if ea[1] == 'DATE':
                self.day.append(ea[2])
        #print ("len(self.message_text)", len(self.message_text))
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
                if b[i][0] not in self.location and b[i][0] not in self.d1:
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
