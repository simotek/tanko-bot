
# Threaded Websocket - Simon Lees simon@simotek.net
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

import threading
import time
import websockets

class  ThreadedWebsocket(threading.Thread):

  def __init__(self, hostname=None, port=None):
    # First set up thread related  code
    threading.Thread.__init__(self)
    self.__dataLock = threading.RLock()
    self.__stopRunning = False
    self.__finished =  True

    # now set up socket related code
    self.__hostname = hostname
    self.__port = port
    self.__recieveFunc = None
    self.__connection = None

  def __del__(self):
    if self.__stopRunning:
      return
    self.__dataLock.acquire()
    self.__stopRunning = True
    self.__dataLock.release()

    waiting = True

    while waiting:
      if self.__dataLock.acquire(False):
        if self.__finished == True:
          waiting = False

        self.__dataLock.release()
      else:
        # if can't get a lock wait for it
        time.sleep(0.2)

  # This method takes a function as a paramater,
  # that function should take 1 paramater which will be passed a line of serial data
  def setRecieveFunction(self, RecvFunc):
    self.__dataLock.acquire()
    self.__recieveFunc = RecvFunc
    self.__dataLock.release()

  def createServer(self):
    self.__dataLock.acquire()
    self.__connection = serial.Serial(self.__serialPort, self.__serialBaud, timeout=None)
    self.__dataLock.release()

  def createClient(self):
    self.__dataLock.acquire()
    self.__connection = serial.Serial(self.__serialPort, self.__serialBaud, timeout=None)
    self.__dataLock.release()

  # writes data to the serial port, automatically re encodes data to
  def write(self, data):
    self.__connection.send(data)
    self.__serialConnection.flush()

  # overloads the theads run class to provide non blocking Seral responses
  # @note create should be called before start
  def run(self):

    while True:
      # take out lock for access to stop running
      # Use a non blocking lock, there is no harm in looping more times here while waiting for
      # something else to unlock
      if self.__dataLock.acquire():
        # if its time to stop running stop
        if self.__stopRunning == True:
          ## do cleanup here

          self.__dataLock.release()
          return

        self.__dataLock.release()

      # this code blocks until it recieves a new line char
      read = self.__connection.recv()

      # check whatever you need to check here
      if self.__serialRecieveFunc is not None:
        # Call the function passing it the line as a parami
        self.__serialRecieveFunc(read)
      time.sleep(0.5)

  def stop(self):
    self.__dataLock.acquire()
    self.__stopRunning = True
    self.__dataLock.release()
