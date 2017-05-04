#!/usr/bin/python

# this is from preliminary testing of NatOS

import re, datetime, json, urllib2, urllib
import sys
from os import environ, path
#sys.path.insert(0,'.')
#sys.path.append('.')
sys.path.append(path.join(path.dirname(path.abspath(__file__)), "." ))
from geotext import GeoText
import yweather
from ActionsA.nlg import generate
from ActionsA import scheduler

with open('core/khal.json', 'r') as f:
    khal = json.load(f)

def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def jdump(element, value):
    with open('core/khal.json', 'r') as f:
        khal = json.load(f)
    khal[element] = value
    with open('core/khal.json', 'w') as f:
        json.dump(khal,f)

def get_weather(city, type):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid="+city
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    condition = data['query']['results']['channel']['item']['condition']['text']
    temperature = str(int((float(data['query']['results']['channel']['item']['forecast'][0]['high'])-32)/1.8))
    return 'The weather is ' + condition + ' reaching ' + temperature + ' degree celsius'

def peep(a):
    if a.find('motivate') != -1:
        print 'in here peep   '
        from Modules.MotivationBot import bot
        return bot.lambda_function(a)
    if a.find('tell') != -1 and a.find('joke') != -1:
        from Modules.joke import bot
        return bot.lambda_function(a)
    return ''

#peep('use motivation bot')

def intent(a):
    words = getWords(a)
    # --- find if user is asking for time
    time_text = ['time']
    for each in time_text:
        if each in words:
            now = datetime.datetime.now()
            res = 'It is ' + str(now.hour) + ' ' + str(now.minute)
            return res
    # --- weather data
    weather_text = ['weather']
    non_cap_weather = ['show', 'tell', 'what', 'is', 'the', 'weather', 'city', 'today',
                        'right', 'now']
    for each in weather_text:
        if each in words:
            potential = GeoText(' '.join([x for x in words if x not in non_cap_weather])).cities
            if potential != []:
                city = potential[0]
                client = yweather.Client()
                city = client.fetch_woeid(city)
            else:
                city = khal['city_id']
            return get_weather(city, 'simple')
    # --- simple reminder
    reminder_text = ['remind', 'reminder']
    number_text = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'fifteen', 'twenty', 'thirty']
    unit_text = ['seconds', 'minutes', 'hours', 'days', 'second', 'minute', 'hour', 'day']
    relative_ref_text=['today','tomorrow']
    buff_text=['in', 'to', 'for']
    dict_num = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'fifteen': 15,
        'twenty': 20,
        'thirty': 30
    }

    for each in reminder_text:
        if each in words:
            num_t = [x for x in number_text if x in words]
            uni_t = [x for x in unit_text if x in words]
            rel_t = [x for x in relative_ref_text if x in words]
            rest = [x for x in words[2:] if x not in num_t and x not in uni_t and x not in rel_t and x not in buff_text]
            if num_t != [] and uni_t != []:
                txt_msg = ' '.join(rest)
                tstamp = uni_t[0]
                if uni_t[0][-1] != 's':
                    tstamp = tstamp + 's'
                scheduler.message(**{tstamp: dict_num[num_t[0]], 'text':txt_msg})
                return 'Okay ' + khal['name'] + ' i will remind you to ' + txt_msg + ' in ' + str(num_t[0]) +' '+ str(uni_t[0])


    return 'NoneConf'

def extract(a):
    a=a.lower()
    # --- pipeline?
    jump = peep(a)
    print 'jump ',jump
    if jump != '':
        return jump

    # --- adv cases
    res = intent(a)
    if res != 'NoneConf':
        return res

    # --- update khal
    if a.find('call me') != -1:
        jdump('name', a[a.lower().find('call me')+8:]) #plus 8 because len(call me) + 1
        return 'Okay, will call you ' + a[a.lower().find('call me')+8:]
    # --- "what's my name"
    if a.find('my name') != -1:
        return 'Indeed ' + khal['name']
    # --- Greetings Managemeny
    if a.find('good morning') != -1:
        return 'Good morning ' + khal['name']
    chatbot = generate.generate(path = './core/conversation.csv')
    ret = chatbot.converse2(a)
    print ret, type(ret)
    if ret != 'NoneConf':
        return ret + ' ' + khal['name']


    return a

#jdump('name', 'love')
