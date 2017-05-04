#!/usr/bin/env python
# ------------------------------------------------------------------------------
# this file should be the only file that needs to be executed.
# it will listen to mike, convert speech to audio, to text, extract intents,
# perform commands, waits till returned, and listens again
# ------------------------------------------------------------------------------

import subprocess, io, json, csv, time
import speech_recognition as sr
from gtts import gTTS
from core import nlqueen
import pygame
from ActionsA.nlg import speak

def push_in_csv(req, res, uid):
    timestamp = int(round(time.time() * 1000))
    date = time.strftime("%m/%d/%Y")
    with open('logs/logs.csv', 'a') as csvfile:
        fieldnames = ['uid', 'req', 'res', 'timestamp', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'uid': uid, 'req': req, 'res': res, 'timestamp': timestamp, 'date': date})


'''def mothercall():
    # ---------- listening through microphone
    listen = subprocess.Popen("python to_audio.py", shell=True)
    listen.wait()
    print "heard"

    # --------- preprocessing
    r = sr.Recognizer()
    r.energy_threshold = 4000
    with io.open('secret.json') as cred:
        creds = json.load(cred)
    with sr.AudioFile('output.wav') as source: # open the audio file for reading
        audio_data = r.record(source) #read the entire audio file
    # --------- sending to Microsoft Bing for speech-to-text
    print 'speech-to-text... '
    ret=''
    try:
        res = r.recognize_bing(audio_data, key=str(creds['bing_api']), language = "en-US", show_all = True)
    except sr.UnknownValueError:
        ret = "Microsoft Bing Voice Recognition could not understand audio"
    except sr.RequestError as e:
        ret = "Could not request results from Microsoft Bing Voice Recognition service; Check internet?"
    if ret=='':
        print res
        if res['header']['status'] == 'error':
            ret = "Could not hear what you are saying. Sorry."
        else:

            #try:
            ret = nlqueen.extract(res['header']['lexical'])
            push_in_csv(res['header']['lexical'], ret, 104)
            print 'ret ', ret # -------- logging in
        #except Exception:
        #    ret = "Could not here what you are saying... Sorry!"
    # --------- using Google to convert text-to-speech
    print 'text-to-speech... '
    speak.say(ret)'''

def mothercall():
    maketest()

def maketest():
    #ret = nlqueen.extract('Ok Nat good morning')
    #speak.say(ret)
    ret = nlqueen.extract('OK Nat good bye')
    speak.say(ret)
    #ret = nlqueen.extract('Ok Nat, call me Nishant')
    #speak.say(ret)
    ret = nlqueen.extract('Ok Nat, what is the time?')
    speak.say(ret)
    ret = nlqueen.extract('remind me to buy milk in twenty seconds')
    speak.say(ret)
    #ret = nlqueen.extract('Motivate me to burn calories')
    #speak.say(ret)
    ret = nlqueen.extract('tell a joke')
    speak.say(ret)

#mothercall()
