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

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

import sys

from twisted.python import log
from twisted.internet import reactor
import threading

from urllib.parse import urlparse

import socket

class UiClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            self.sendMessage(u"Hello, world!".encode('utf8'))
            #self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.reactor.callLater(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


class  UiClient(threading.Thread):

  def __init__(self, url=None):
    # First set up thread related  code
    threading.Thread.__init__(self)

    self.__url = url

  def run(self):
      while self.__url is None:
          discoverySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
          discoverySocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
          discoverySocket.settimeout(5)

          discoverySocket.sendto(b"hello", ("<broadcast>", 8701))
          try:
             data, address = discoverySocket.recvfrom(1024)

             self.__url = "ws://" + address[0] + ":8702"
             print ("Found: "+ self.__url)
          except socket.timeout:
             print ("No server found")

          discoverySocket.close()

      factory = WebSocketClientFactory(self.__url, debug=False)
      #factory = WebSocketClientFactory("ws://192.168.1.7:8702", debug=False)

      factory.protocol = UiClientProtocol

      parsed = urlparse(self.__url)

      ipaddr = parsed.netloc.replace("ws://","").split(':', 1)[0]
      print ("Connecting to: "+ipaddr+"-"+str(parsed.port))

      reactor.connectTCP(ipaddr, parsed.port, factory)
      reactor.run()

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    # Connect with no url to use discovery
    client = UiClient()

    client.run()
