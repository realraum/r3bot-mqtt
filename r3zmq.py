#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import signal
import zmq.utils.jsonapi as json
import zmq
import traceback
import time
from r3zmqfilter import r3zmqfilter
########################
# r3zmq listener
# by verr
# based on code by xro

class r3zmq():
    def __init__(self, broker="tcp://zmqbroker.realraum.at:4244"):
        self.broker = broker
        self.active = True

    def decodeR3Message(self, multipart_msg):
        try:
            return (multipart_msg[0], json.loads(multipart_msg[1]))
        except Exception, e:
            logging.debug("decodeR3Message:"+str(e))
            return ("",{})
    def exitHandler(signum, frame):
      try:
        zmqsub.close()
        zmqctx.destroy()
      except:
        pass
      sys.exit(0)
    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGQUIT, exitHandler)


    def zmqloop(self, listener):
        while self.active :
          try:
            #Start zmq connection to publish / forward sensor data
            zmqctx = zmq.Context()
            zmqctx.linger = 0
            zmqsub = zmqctx.socket(zmq.SUB)
            zmqsub.setsockopt(zmq.SUBSCRIBE, "")
            zmqsub.connect(self.broker)
            while self.active :
              data = zmqsub.recv_multipart()
              (structname, dictdata) = self.decodeR3Message(data)
              listener(structname, dictdata)
          except Exception, ex:
            print "main: "+str(ex)
            traceback.print_exc(file=sys.stdout)
            try:
              zmqsub.close()
              zmqctx.destroy()
            except:
              pass
            time.sleep(5)

def zmqlistener(structname, dictdata):
    filter = r3zmqfilter()
    print filter.do(structname, dictdata)

if __name__ == "__main__":
    z = r3zmq()
    z.zmqloop(zmqlistener)

