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

# pip install autobahn
# pip install zope.interface
# pip install twisted

import sys

from twisted.python import log
from twisted.internet import reactor
import threading

from urllib.parse import urlparse

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

from socketserver import UDPServer, BaseRequestHandler

class UiServerProtocol(WebSocketServerProtocol):

  def onConnect(self, request):
    print("Client connecting: {0}".format(request.peer))

  def onOpen(self):
    print("WebSocket connection open.")
    self.factory.register(self)

  def onMessage(self, payload, isBinary):
    if isBinary:
      print("Binary message received: {0} bytes".format(len(payload)))
    else:
      print("Text message received: {0}".format(payload.decode('utf8')))

    # echo back message verbatim
    self.sendMessage(payload, isBinary)
    self.factory.broadcast("Broadcasting")

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

  def onClose(self, wasClean, code, reason):
    print("WebSocket connection closed: {0}".format(reason))

class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []
        self.tickcount = 0
        self.tick()

    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d from server" % self.tickcount)
        reactor.callLater(1, self.tick)

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))

class DiscoveryHandler(BaseRequestHandler):
   def handle(self):
       print ("message:", self.request[0])
       print ("from:", self.client_address)
       socket = self.request[1]
       socket.sendto(b"hello", self.client_address)

class DiscoveryServer(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def run(self):
    # start discovery
    addr = ("", 8701)
    print ("listening on %s:%s" % addr)
    server = UDPServer(addr, DiscoveryHandler)
    server.serve_forever()

class  UiServer(threading.Thread):

  def __init__(self, url):
    # First set up thread related  code
    threading.Thread.__init__(self)

    self.__url = url

  def run(self):
    # Setup discovery
    discovery = DiscoveryServer()
    discovery.start()

    # Setup websockets
    factory = BroadcastServerFactory(self.__url, debug=False)
    factory.protocol = UiServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    port = urlparse(self.__url).port

    reactor.listenTCP(port, factory)
    reactor.run()

if __name__ == '__main__':


    log.startLogging(sys.stdout)

    server = UiServer("ws://localhost:8702")

    server.run()
