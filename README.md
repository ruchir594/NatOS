# NatOS

### Commands it can understand

> Ok Nat, --Greetings--

> OK Nat, Call me <Heart wants what it wants>

> Ok Nat, What time is it?

> Ok Nat, Hows the weather?

### Things to be added

1. Wake work Engine (completed) (Thanks to KITT.ai)
2. Image Recognition
3. Asynchronous process management for wait_on(s)

P.S. Good internet is of utmost important

![alt tag](https://raw.githubusercontent.com/ruchir594/NatOS/master/legacy/story1.png)


# Technical Documentation

### Overview of code

The only thing one has to run, is parent.py. Which in turn executes WakeWord.py, with WakeWord being "Ok Nat."

When the WakeWord is detected, the snowboydecoder immediately calls Mothership which starts recording the rest of the voice. Processes.

### Processing Commands

1. Core
Common functions and casual Natural Language interactions (weather, time, hi-hello) will be handles by Core directory, mainly, nlqueen.py. Thoughful contributions to casual NLI welcomed.

2. Advance Actions

I. Standard Modules.
Reminders, Schedule, Monitoring; will be handled by Actions Architecture. Which is our Module Based approach.

II. Custom Modules
Any hacker or organization can built their own Module and push into main repository which will allow any user of NatOS to download and use them. Any Custom Module which follows Actions Architectures Documentation (see here - work in progress) will be integrated on its own and all the functionality of that module will be available to NatOS main voice interface directly. It is gonna be that simple.  
