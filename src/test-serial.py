# RobotMain - Simon Lees simon@simotek.net
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

from .threadedserial import ThreadedSerial
from .util import CallbackHelper
from .constants import *

class SerialTestParsingException(Exception):
    pass


class SerialTestInterfaceCallbacks:
    def __init__(self):
        self.annMessage = CallbackHelper()

class SerialTestInterface:
  def __init__(self, callbacks):
    self.__dataLock = threading.RLock()
    self.__messageQueue = []

    self.__callbacks = callbacks

    self.__serial = ThreadedSerial("/dev/ttyS1", 4800)
    self.__serial.setSerialRecieveFunction(self.onMessage)
    self.__serial.create()

  def getCallbacks(self):
      return self.__callbacks

  def setCallbacks(self, callbacks):
      self.__callbacks = callbacks

  # Adds message to queue for processing
  def onMessage(self, message):
    self.__dataLock.acquire()
    self.__messageQueue.append(message)
    self.__dataLock.release()

  # Processes all messages on queue and fires there callbacks
  def processMessages(self):
    self.__dataLock.acquire()

    while self.__messageQueue:

      message = self.__messageQueue.pop(0)

      #Unlock mutex to avoid holding while signals are triggered
      self.__dataLock.release()

      self.decodeMessage(message[0])

      #relock mutex for next check of the queue
      self.__dataLock.acquire()

    # Release mutex once finished
    self.__dataLock.release()

  def decodeMessage(self, message):

    data = message
    self.__callbacks.annMessage.invoke(data)

  def sendMessage(self, message):    
    print ("Sending: " + message)
    self.__serial.write(message)
    
  def sendDriveMotorSpeed(self, args):
    message = str(CONST_SERVER_COMMAND_MOTOR_DRIVE+":"+args[0]+","+args[1]+"\n")
 
    print (message)

    self.__serial.write(message)

def printMessage(self, args):
    print ("MSG:"+args[0])

if __name__ == '__main__':

  parser = argparse.ArgumentParser("Main Robot control app")
  #parser.add_argument("-s", "--no-serial", type=str, required=False, help="Stub out serial")
  parser.add_argument('--no-serial', dest='noserial', action='store_true')

  args = parser.parse_args()

  serialCallbacks = SerialTestInterfaceCallbacks()

  serialCallbacks.annMessage.register(printMessage)
  serialInterface = SerialTestInterface(serialCallbacks)


  # Main app event loop
  while True:
    serialInterface.processMessages()
    time.sleep(1)
    serialInterface.sendMessage("Foo\n")
    serialInterface.processMessages()
    time.sleep(1)
    serialInterface.sendMessage("Baa\n")
