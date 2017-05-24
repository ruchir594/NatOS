# NatOS - Libraries

If at first you don't succeed, we have a lot in common.

### Scheduling async bash commands with one line. Literally.

```
from ActionsA import scheduler

scheduler.message(seconds=7, command='afplay imagine.mp3')
scheduler.message(minutes=5, command='python 334.py &')
```

### Voice messages too...

```
from ActionsA import scheduler

scheduler.message(seconds=4, text='Nitesh is brilliant...')
scheduler.message(minutes=2, text='Or is he?')
scheduler.message(hours=6, text='Only time will tell', player='afplay')
scheduler.message(days=7, text='He is!', player='mpg123')
```

The default player is omxplayer, which runs well on raspberry Pi, but a player must be specified for other OS.

### Installing

```
git clone https://github.com/ruchir594/NatOS.git
cd NatOS
sudo make
```

If you are running this on a Mac or any other Unix, please make sure your redis-server and queue-server is running. Open CLI, and run

```
redis-server

cd NatOS
python queue-server.py &
```

In Raspberry Pi, for some weird reason, even after adding queue-server into init.d, it still has to be manually started.

Do not forget to run redis-server and queue-server.


### Technical Documentation

Uses Redis and tasktiger as backend.

During make, redis-server and a queue for "tasks" is added to deamon for perceived seemless interaction. (Tasks = when to play, text to be played).

text-to-speech is powered by omxplayer on raspberry pi.


-- more coming soon --


- - - -

*comments, criticism, and contributions welcome*

*Designed and Tested for Raspberry Pi running Raspbian Jessie*

# NatOS

### Commands it can understand

> Ok Nat, -- Greetings --

> OK Nat, Call me  -- Khal Drogo? --

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
