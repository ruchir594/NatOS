# speak.py
from gtts import gTTS
import pygame
import subprocess

def say(ret):
    tts = gTTS(text=ret, lang='en')
    tts.save('ret.mp3')
    '''pygame.mixer.init()
    pygame.mixer.music.load('ret.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue'''
    listen = subprocess.Popen("omxplayer -o local ret.mp3", shell=True)
    listen.wait()
