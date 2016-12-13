'''import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    dic=os.path.join(model_path, 'cmudict-en-us.dict')
)

for phrase in speech:
    print(phrase)
    print(phrase.segments(detailed=True))
    print(phrase.best(count=10))
    print('~~~~~~~~~~~~~~')'''

'''
curl -X POST -u 446dda25-aa78-46ed-bc92-d1569008b46f:b56QwI2ofryB --header "Content-Type: audio/wav" --header "Transfer-Encoding: chunked" --data-binary @/recordings/0001.wav "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true"
curl -u 446dda25-aa78-46ed-bc92-d1569008b46f:b56QwI2ofryB  "https://stream.watsonplatform.net/authorization/api/v1/token?url=https://stream.watsonplatform.net/speech-to-text/api"
python ./sttClient.py -credentials 446dda25-aa78-46ed-bc92-d1569008b46f:b56QwI2ofryB -model en-US_BroadbandModel
'''

import subprocess
import json
###############################################################################
# Gulp (multiple JSON object { ..{1}. }{ ..{2}. }{ ..{3}. } )
# Returns the last object { ..{3}. }
###############################################################################
def gulp(f):
    index = []
    count = 0
    lower = None
    upper = None
    i=0
    while i < len(f):
        each = f[i]
        if each == '{':
            if count == 0:
                lower = i
            count = count + 1
        if each == '}':
            count = count - 1
            if count == 0:
                upper = i
                index.append([lower, upper])
                lower = None
                upper = None
        i = i + 1
    return f[index[-1][0] : index[-1][1]+1]

###############################################################################
# ---------- listening through microphone ----------------------------------- #
###############################################################################
listen = subprocess.Popen("python to_audio.py", shell=True)
listen.wait()
print "heard"

###############################################################################
# --------- using IBM Watson to send output.wav file for voice - text ------- #
###############################################################################
out = subprocess.Popen("python sttClient.py -credentials 446dda25-aa78-46ed-bc92-d1569008b46f:b56QwI2ofryB -model en-US_BroadbandModel", shell=True)
out.wait()
print "Processed though IBM Watson"

###############################################################################
# -------- reading txt output of IBM JSON object ---------------------------- #
###############################################################################
f = open('output/0.json.txt', 'r')
f = f.read()
f = gulp(f)
j = json.loads(f)
text = j['results'][0]['alternatives'][0]['transcript'] #best possible response

###############################################################################
# ---------- Using Actions Architecture ------------------------------------- #
# ---------- NLE -> NLU -> NLG using Actions Architecture ------------------- #
# ---------- State and Elements to be managed by Actions Architecture ------- #
# ---------- Receiving the best possible NLG -------------------------------- #
###############################################################################
'''text = "good morning, it is a lovely day today. buy pizza at 6 PM tomorrow?"
from ActionsA.nle.entities import ner_primitive
ayrton = ner_primitive(text)
print ayrton.view()'''
###############################################################################
# using local python lib to convert text to voice
#
###############################################################################
import pyttsx
engine = pyttsx.init()
#engine.say('Sally sells seashells by the seashore.')
engine.say(text)
engine.runAndWait()

# Alexa integration
