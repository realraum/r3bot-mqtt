# R3mqtt

This plugin (*R3mqtt*) connects your Limnoria bot to zeromq.

Listen to an zeromq broker, filter them, and notify irc channel about events.


## Install

Install the plugin by cloning it into the *R3mqtt* directory in your Limnoria's plugin directory:

```
% cd runbot/plugins 
% git clone https://github.com/realraum/r3bot-mqtt.git R3mqtt
```

Now you need to install the required libraries (see requirements.txt), either via pip ...

```
% cd R3mqtt
% sudo pip install -r requirements.txt
```

... or via your package manager, for example:

```
sudo pip install paho-mqtt
```

Afterwards tell your Limnoria bot to load the plugin:

```
load R3mqtt
```

And you are done.

## Configuration

You can get all configuraiton-parameters via the ```config list plugins.R3mqtt``` command.

* ```plugins.R3mqtt.mqttbroker``` - URI of your zeromq's broker
* ```plugins.R3mqtt.network``` - IRC Network to which the events are reported.
* ```plugins.R3mqtt.channel``` - IRC Channel to which the events are reported.


You can set them either in your Limnoria configuration or via the bot's cli:

```
<user> config plugins.R3mqtt.mqttbroker tcp://mqttbroker.realraum.at:4244
[bot] The operation succeeded.
```

## Filter

Your zeromq traffic may be to verbatim to relay it directly to your channel. If so you can filter/format the events by implementing a filter in *r3mqttfilter.py*.
