#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import signal
import json
import paho.mqtt.client as mqtt
import traceback
import time
from .r3mqttfilter import r3mqttfilter
#
# r3mqtt listener
# by verr
# based on code by xro


class r3mqtt():

    def __init__(
        self,
        broker="mqtt.realraum.at",
     brokerport=1883,
     clientid="r3bot-mqtt",
     subscriptions=[("realraum/+/boredoombuttonpressed",
                     1)]):
        self.broker = broker
        self.brokerport = brokerport
        self.client = None
        self.active = True
        self.subscriptions = subscriptions
        self.clientid = clientid

    def connectToBroker(self):
        client = mqtt.Client(client_id=self.clientid)
        client.connect(self.broker, self.brokerport, 60)
        client.on_message = self.recvMQTTMsg
        client.subscribe(self.subscriptions)
        self.client = client

    def sendR3Message(self, mqtttopic, datadict, qos=0, retain=False):
        self.client.publish(mqtttopic, json.dumps(datadict), qos, retain)

    def decodeR3Message(self, mqtttopic, payload):
        try:
            return (mqtttopic, json.loads(payload.decode("utf-8")))
        except Exception as e:
            logging.debug("Error decodeR3Payload:" + str(e))
            return ("", {})

    def recvMQTTMsg(self, client, userdata, msg):
        (mqtttopic, dictdata) = self.decodeR3Message(msg.topic, msg.payload)
        self.listener(mqtttopic, dictdata)

    def disconnectFromBroker(self):
        try:
            if isinstance(self.client, mqtt.Client):
                self.client.disconnect()
        except:
            pass

    def exitHandler(self, signum, frame):
        self.disconnectFromBroker()
        sys.exit(0)

    def mqtttloop(self, listener):
        self.listener = listener
        while self.active:
            try:
                self.connectToBroker()
                while self.active:
                    self.client.loop()
            except Exception as ex:
                print "main: " + str(ex)
                traceback.print_exc(file=sys.stdout)
                self.disconnectFromBroker()
                time.sleep(5)


def mqttlistener(mqtttopic, dictdata):
    filter = r3mqttfilter()
    print filter.do(mqtttopic, dictdata)

if __name__ == "__main__":
    z = r3mqtt()
    signal.signal(signal.SIGINT, z.exitHandler)
    signal.signal(signal.SIGQUIT, z.exitHandler)
    z.mqtttloop(mqttlistener)
