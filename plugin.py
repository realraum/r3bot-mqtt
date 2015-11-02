###
# Copyright (c) 2010, quantumlemur
# Copyright (c) 2012, Valentin Lorentz
# Copyright (c) 2015, verr/realraum.at
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import json
import time
import socket
import threading
import traceback
import supybot.log as log
import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.registry as registry
import supybot.callbacks as callbacks

from r3zmq import r3zmq
from r3zmqfilter import r3zmqfilter

from supybot.i18n import PluginInternationalization
from supybot.i18n import internationalizeDocstring
_ = PluginInternationalization('R3zmq')


class R3zmq(callbacks.Plugin):

    """Add the help for "@plugin help R3zmq" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(R3zmq, self)
        self.__parent.__init__(irc)
        self.listenerThreads = []
        self._loadFromConfig()

    def _loadFromConfig(self, name=None):
        broker = self.registryValue('zmqbroker')
        network = self.registryValue('network')
        channel = self.registryValue('channel')
        for thread in self.listenerThreads:
            thread.zmqhandler.active = False
        time.sleep(2)
        self.listenerThreads = []
        try:
            log.info('Starting zmq listener thread: %s' % broker)
            thread = self.ListeningThread(network, channel, broker)
            thread.start()
            self.listenerThreads.append(thread)
        except TypeError:
            irc.error('Cannot load zmq: %s' % broker)

    class ListeningThread(threading.Thread):

        def __init__(self, network, channel, broker):
            threading.Thread.__init__(self)
            self.network = network
            self.channel = channel
            self.broker = broker
            self.buffer = ''
            self.zmqhandler = r3zmq()
            self.filter = r3zmqfilter()

        def notifyIrc(self, structname, structdata):
            msg = filter.do(structname, structdata)
            if msg is None or len(msg) < 0:
                return
            for IRC in world.ircs:
                if IRC.network == self.network:
                    try:
                        IRC.queueMsg(
                            ircmsgs.privmsg(self.channel, msg))
                    except Exception as e:
                        traceback.print_exc(e)

        def run(self):
            self.zmqhandler.zmqloop(self.notifyIrc)

    def die(self):
        for thread in self.listenerThreads:
            thread.zmqhandler.active = False
            log.info('shutdown zmqhandler %s' % thread.broker)
        self.listenerThreads = []
        time.sleep(2)

Class = R3zmq


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
