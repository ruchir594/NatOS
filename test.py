'''###############################################################################
import pyttsx
engine = pyttsx.init()
#engine.say('Sally sells seashells by the seashore.')
engine.say(u"Welcome, Water Buffalo")
engine.runAndWait()
print 'waited now i guess.... '
engine.stop()'''

#!/usr/bin/env python
from os import environ, path
from pocketsphinx import LiveSpeech, get_model_path, AudioFile, get_data_path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "pocketsphinx/model"
model_path = get_model_path()
DATADIR = "pocketsphinx/test/data"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(model_path, 'en-us'))
config.set_string('-lm', path.join(model_path, 'en-us.lm.bin'))
config.set_string('-dict', path.join(model_path, 'cmudict-en-us.dict'))
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open('output2.wav', 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()
print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
