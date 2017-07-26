# Welcome to Actions Architecture

An Architecture for Hackers and Companies to build Bot Modules.

Integrate automatically
1. NatOS Raspberry Pi Client
2. NatOS iOS and Android App

You can build a module with Actions Architecture which will allow you to easily build complex bots,

or you can build your own module with a compatible endpoint (see below),

### Let's start with an Example, which will help us elaborate and you understand easily

Our own Motivation Bot. using Actions Architecture (at ../Modules/MotivationBot)

The purpose of this bot is to motivate you and remind you to eat healthy and avoid alcohol. It sends motivational messages in the evening, or whenever you are home, to help you avoid excess calories.

Things you don't need to write with NatOS and Actions Architecture

1. Named Entity Recognizer
2. Sentence Similarity functions for "sentence hashing"

Things you do

1. specs.json - to specify which NLU, NLG functions to use.
2. conversation.csv - A simple conversation with possible responses.
3. bot.py

specs.json lets you use Naive NLG or Advance NLG (under development) depending upon your requirement.
We use Naive NLG.

Conversation.csv lets you define simple communication standard. What should be the response to a typical input? See the CSV.

bot.py - This is where we give you the control. merely 10 lines here will make your bot compatible with NatOS.
But we allow you to customize this the way you want. You could decide to not use our Architecture at all and code whatever you wish.
You could send POST requests to your own servers you wish to do that. Adding a few lines to make our endpoint compatible is all you have to care about.

### Conversation.CSV

It is a 2 pass system.

\1. Uses a NLTK based approach to pattern matching.

a Pattern between asterisk 1. \*super car\* or 2. \*amazing\* is matched.

Strings "Ferrari builds Super cars" will be matched with first pattern, and a string  "Game of Thrones is amazing" will be matched with both patterns.

\2. Uses a modification of NLTK chat util to match broken patterns.

Broken Patters are defined as a mixure of two patters. Let us say you want to match two substring \*super car\* and \*amazing\*.
A pattern separated by '\_' (underscore) will allow you to do that.
A Pattern \*super car_amazing\* will yield such results.

A string "Pagani makes more than super cars and they are amazing!" will be matched with above Pattern.

It is important to note than Patterns are evaluated in linear order.

-- Our heavily Modified NLTK Chat Util is at ActionsA/nlg/nltk_chat_util.py. Other Class and Methods used are from standard NLTK and does require that. 
