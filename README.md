# R3zmq

This plugin (*R3zmq*) connects your Limnoria bot to zeromq.

Listen to an zeromq broker, filter them, and notify irc channel about events.


## Install

Install the plugin by cloning it into the *R3zmq* directory in your Limnoria's plugin directory:

```
pi@thinkpi ~ % cd runbot/plugins 
pi@thinkpi ~/runbot/plugins % git clone https://github.com/realraum/r3bot-zmq.git R3zmq
Cloning into 'R3zmq'...
remote: Counting objects: 19, done.
remote: Compressing objects: 100% (10/10), done.
remote: Total 19 (delta 7), reused 19 (delta 7), pack-reused 0
Unpacking objects: 100% (19/19), done.
Checking connectivity... done.
```

Then tell your Limnoria bot to load it:

```
load R3zmq
```

And you are done.
