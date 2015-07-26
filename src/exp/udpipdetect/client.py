
# original code from http://wiki.python-forum.de/UDP-Broadcasts
import socket

discoverySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
discoverySocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
discoverySocket.settimeout(5)

discoverySocket.sendto(b"hello", ("<broadcast>", 7789))
try:
   data, address = discoverySocket.recvfrom(1024)

   addressStr = address[0] + ":" + str(address[1])
   print ("From: "+ addressStr)
except socket.timeout:
   print ("No server found")

discoverySocket.close()
