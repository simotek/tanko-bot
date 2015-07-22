
# Websocket Client - Simon Lees simon@simotek.net
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


# This class uses asyncio from a different thread to ensure it doesn't need to interupt
#  or be involved in other event loops such as the efl or pyqt ones depending 
#  on which other libs are being used

import threading

class  WebsocketClient(threading.Thread):

  def __init__(self, url):
    # First set up thread related  code
    threading.Thread.__init__(self)
    self.__dataLock = threading.RLock()
    self.__stopRunning = False
    self.__finished =  True

    # now set up serial related code
    self.url = url
    self.__recieveFunc = None
    self.__socket = None
    self.__sendQueue[]

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
  # that function should take 1 paramater which will be passed a line of data
  def setRecieveFunction(self, RecvFunc):
    self.__dataLock.acquire()
    self.__recieveFunc = RecvFunc
    self.__dataLock.release()


  # writes data
  def write(self, data):
    self.__dataLock.acquire()
    self.__sendQueue.append(data)
    self.__dataLock.release()

  # overloads the theads run class to provide non blocking Seral responses
  # @note create should be called before start
  def run(self):

    self.__dataLock.acquire()
    self.__socket =  websockets.connect('ws://localhost:8765/')
    self.__dataLock.release()
    
    asyncio.get_event_loop().run_until_complete(__process())


  def __process(self):
    while True:
      # take out lock for access to stop running
      # Use a non blocking lock, there is no harm in looping more times here while waiting for
      # something else to unlock
      aquired = yield from self.__dataLock.acquire()
      if aquired:
        # if its time to stop running stop
        if self.__stopRunning == True:
          ## do cleanup here

          self.__dataLock.release()
          return

        self.__dataLock.release()

      # this code blocks until it recieves a new line char
      aquired = yield from self.__dataLock.acquire()
      if aquired:
        data = websocket.recv()

        # check whatever you need to check here
        if self.__recieveFunc is not None:
          # Call the function passing it the line as a parami
          self.__recieveFunc(data)
          
        self.__dataLock.release()
      
      
      aquired = yield from self.__dataLock.acquire()
      if aquired:
        for data in self.__sendQueue:
          websocket.send(data) 
        
        self.__dataLock.release()

  def stop(self):
    self.__dataLock.acquire()
    self.__stopRunning = True
    self.__dataLock.release()