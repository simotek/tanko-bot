###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Simon Lees 2015
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import asyncio

from PyLibs.websocketserver import ThreadedWebSocketServer, ServerCallbacks
from PyLibs.discoveryserver import DiscoveryServer

import time

class Printer:
    def __init__(self):
        print ("create")

    def cn():
        print ("Connected CB")

    def dn ():
        print ("Disconnected CB")

    def m(Message):
        print ("Msg Recieved: "+ str(Message))


if __name__ == '__main__':

    pnt = Printer

    callbacks = ServerCallbacks()

    callbacks.connect.register(pnt.cn)
    callbacks.disconnect.register(pnt.dn)
    callbacks.message.register(pnt.m)

    discovery = DiscoveryServer()
    discovery.start()

    server = ThreadedWebSocketServer("ws://127.0.0.1:8702", callbacks)

    server.start()

    time.sleep(4)

    while True:
        server.broadcastMessage("Broadcast")

        time.sleep(1)
