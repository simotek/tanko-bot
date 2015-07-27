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

import threading
import time

clientMessageQueueGbl = []

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        clientMessageQueueGbl.append("Connect")

        def hello():
            self.sendMessage(u"Hello, world!".encode('utf8'))
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.loop.call_later(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
            clientMessageQueueGbl.append(payload.decode('utf8'))


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        clientMessageQueueGbl.append("Disconnect")



class  BotWebSocketClient(threading.Thread):

  def __init__(self):
    # First set up thread related  code
    threading.Thread.__init__(self)

    self.__loop = asyncio.get_event_loop()

  def run(self):
      asyncio.set_event_loop(self.__loop)

      factory = WebSocketClientFactory("ws://localhost:9000", debug=False)
      factory.protocol = MyClientProtocol

      coro = self.__loop.create_connection(factory, '127.0.0.1', 9000)
      self.__loop.run_until_complete(coro)
      self.__loop.run_forever()
      self.__loop.close()


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    client = BotWebSocketClient()
    client.start()

    print ("Threads started")

    while True:
        if clientMessageQueueGbl:
            for data in clientMessageQueueGbl:
                print ("MSG: " + data)

            clientMessageQueueGbl = []
        time.sleep(0.1)
