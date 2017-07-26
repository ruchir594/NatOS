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

1. Uses a NLTK based approach to pattern matching.

a Pattern between asterisk 1. *super* or 2. *super duper* is matched.

Strings "Ferrari builds Supercars" will be matched with first pattern, and a string  "Game of Thrones is Super Duper good" will be matched with both patterns.
