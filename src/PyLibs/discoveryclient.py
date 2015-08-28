
# Discovery Client - Simon Lees simon@simotek.net
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

import socket

from .constants import discoveryPort, uiPort

# Blocking function that will find ip
def DiscoveryClient():
  discoverySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  discoverySocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
  discoverySocket.settimeout(5)

  discoverySocket.sendto(b"hello", ("<broadcast>", 8701))

  url = None

  while url is None:

      try:
        data, address = discoverySocket.recvfrom(1024)

        url = "ws://" + address[0] + ":" + str(uiPort)
        print ("Found: "+ url)
      except socket.timeout:
        print ("No server found")

      discoverySocket.close()

  return url
