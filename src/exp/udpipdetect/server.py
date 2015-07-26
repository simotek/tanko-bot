
# original code from http://wiki.python-forum.de/UDP-Broadcasts

from socketserver import UDPServer, BaseRequestHandler # python 3

class DiscoveryHandler(BaseRequestHandler):
   def handle(self):
       print ("message:", self.request[0])
       print ("from:", self.client_address)
       socket = self.request[1]
       socket.sendto(b"hello", self.client_address)

addr = ("", 8701)
print ("listening on %s:%s" % addr)
server = UDPServer(addr, DiscoveryHandler)
server.serve_forever()
