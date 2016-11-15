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

out = subprocess.Popen("python sttClient.py -credentials 446dda25-aa78-46ed-bc92-d1569008b46f:b56QwI2ofryB -model en-US_BroadbandModel", shell=True)
out.wait()

print "over"
'''import pyttsx
engine = pyttsx.init()
#engine.say('Sally sells seashells by the seashore.')
engine.say('Ruchir is Hot. Brij is a bitch.')
engine.runAndWait()'''
