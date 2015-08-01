
# Arduino Interface - Simon Lees simon@simotek.net
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

from .threadedserial import ThreadedSerial
from .util import CallbackHelper
from .constants import *

class ArduinoParsingException(Exception):
    pass


class ArduinoInterfaceCallbacks:
    def __init__(self):
        self.annLeftDriveMotor = CallbackHelper()
        self.annRightDriveMotor = CallbackHelper()

class ArduinoInterface:
  def __init__(self, callbacks):
    self.__dataLock = threading.RLock()
    self.__messageQueue = []

    self.__callbacks = callbacks

    self.__serial = ThreadedSerial("/dev/ttyS2", 115200)
    self.__serial.setSerialRecieveFunction(self.onMessage)

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

    split = message.split(':')

    command = split[0]
    data = None

    if len(split) == 2:
      data = split[1]

    if len(split) > 2:
      raise UiClientNetworkException("Invalid Message, too many commands (:)")


    if (command == CONST_SERVER_ANN_DRIVE_MOTOR_LEFT_SPEED):
      self.__callbacks.annLeftDriveMotor.invoke(data)
    elif (command == CONST_SERVER_ANN_DRIVE_MOTOR_RIGHT_SPEED):
      self.__callbacks.annRightDriveMotor.invoke(data)
    else:
      print("Unknown command:"+command)

  def sendDriveMotorSpeed(self, args):
    self.__serial.write(CONST_SERVER_COMMAND_MOTOR_DRIVE+":"+args[0]+","+args[1])
