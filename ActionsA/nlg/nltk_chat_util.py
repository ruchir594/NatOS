# Natural Language Toolkit: Chatbot Utilities
#
# Copyright (C) 2001-2016 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <jez@jezuk.co.uk>.
from __future__ import print_function

import re
import random
from nltk import compat

import random, string

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}

class Chat(object):
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self._pairs = [(re.compile(x, re.IGNORECASE),y) for (x,y) in pairs]
        self._full_pairs = pairs
        self._reflections = reflections
        self._regex = self._compile_reflections()


    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len,
                reverse=True)
        return  re.compile(r"\b({0})\b".format("|".join(map(re.escape,
            sorted_refl))), re.IGNORECASE)

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(lambda mo:
                self._reflections[mo.string[mo.start():mo.end()]],
                    str.lower())

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def respond(self, string):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """
        #print('~~~~~')
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(string)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

        #print('Didnt return shit...')

        #try matching strings with multiple hooks
        #brute forcing from pairs

        for (x, y) in self._full_pairs:
            if x.find('_') != -1:
                sub_x = x.split('_')
                sub_x[0] = sub_x[0] + '(.*)'
                sub_x[len(sub_x)-1] = '(.*)' + sub_x[len(sub_x)-1]
                i=0
                for each in sub_x:
                    if i > 0 and i < len(sub_x)-1:
                        sub_x[i] = '(.*)' + sub_x[i] + '(.*)'
                    i+=1
                flag_sub_x = True
                for each in sub_x:
                    lhs = re.compile(each, re.IGNORECASE)
                    match = lhs.match(string)
                    if not match:
                        flag_sub_x = False
                        break
                if flag_sub_x:
                    # recurse call would be cool but NOT EFFICIENT
                    resp = random.choice(y)    # pick a random response
                    resp = self._wildcards(resp, match) # process wildcards

                    # fix munged punctuation at the end
                    if resp[-2:] == '?.': resp = resp[:-2] + '.'
                    if resp[-2:] == '??': resp = resp[:-2] + '?'
                    return resp

        # Default response
        # Note: Recurse will be called only once to specify Default
        # return self.respond('DefaultResponse42')
        # -- greater risk of stack overflow with recursive definition --

        # A Default Response must be set in Conversation.CSV

        string = 'DefaultResponse'
        for (pattern, response) in self._pairs:
            match = pattern.match(string)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp


    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        input = randomword(10)
        while input != quit:
            input = quit
            try: input = randomword(10)
            except EOFError:
                print(input)
            if input:
                while input[-1] in "!.": input = input[:-1]
                print(self.respond(input))
                return
            return
        return

    def converse2(self, input = randomword(10), quit="quit"):
        #input = randomword(10)
        if input:
            while input[-1] in "!.":
                input = input[:-1]
            d = (self.respond(input))
            return d
        return d
