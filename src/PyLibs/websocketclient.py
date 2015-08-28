# Based off a test app with the following license
###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
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

from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import asyncio


import threading
import time
from urllib.parse import urlparse
from .util import CallbackHelper

class ClientCallbacks:
    def __init__(self):
        self.connect = CallbackHelper()
        self.disconnect = CallbackHelper()
        self.message = CallbackHelper()

class ThreadedClientProtocol(WebSocketClientProtocol):

    def __init__(self, *args):
        WebSocketClientProtocol.__init__(self, *args)

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def send(self, data):
        self.sendMessage(data.encode('utf8'))

    def onOpen(self):
        print("WebSocket connection open.")
        self.factory.register(self)


    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            self.factory.onMessage(payload.decode('utf8'))


    def connectionLost(self, reason):
      WebSocketServerProtocol.connectionLost(self, reason)
      self.factory.unregister(self)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

class ThreadedClientFactory(WebSocketClientFactory):
    def __init__(self, url, callbacks, debug=False, debugCodePaths=False):
        print ("URL is: "+url)
        WebSocketClientFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.__clients = []
        self.__callbacks = callbacks

    def register(self, client):
        self.__clients.append(client)
        self.__callbacks.connect.invoke()

    def unregister(self, client):
        self.__clients.remove(client)
        self.__callbacks.disconnect.invoke()

    def onMessage(self, message):
        print("On Message: "+ str(message))
        self.__callbacks.message.invoke(message)

    def sendMessage(self, message):
        for c in self.__clients:
            self.loop.call_soon_threadsafe(c.sendMessage, message.encode('utf8'))

class  ThreadedWebSocketClient(threading.Thread):

  def __init__(self, url, callbacks):
    # First set up thread related  code
    threading.Thread.__init__(self)

    self.__url = url

    self.__loop = asyncio.get_event_loop()

    self.__factory = ThreadedClientFactory(self.__url, callbacks, debug=False)
    self.__factory.protocol = ThreadedClientProtocol

  def sendMessage(self, data):
    self.__factory.sendMessage(data)

  def run(self):
      asyncio.set_event_loop(self.__loop)

      parsed = urlparse(self.__url)

      ipaddr = parsed.netloc.replace("ws://","").split(':', 1)[0]
      print ("Connecting to: "+ipaddr+"-"+str(parsed.port))

      print ("Warning more hardcoding")
      coro = self.__loop.create_connection(self.__factory, ipaddr, parsed.port)
      self.__loop.run_until_complete(coro)
      self.__loop.run_forever()
      self.__loop.close()
