
# Discovery Server - Simon Lees simon@simotek.net
# Copyright (C) 2015 Simon Lees
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from socketserver import UDPServer, BaseRequestHandler
import threading

from .constants import discoveryPort

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
    addr = ("", discoveryPort)
    print ("listening on %s:%s" % addr)
    server = UDPServer(addr, DiscoveryHandler)
    server.serve_forever()
