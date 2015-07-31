
# UiServer - Simon Lees simon@simotek.net
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

import asyncio
import threading
import time

from .websocketserver import ThreadedWebSocketServer, ServerCallbacks
from .discoveryserver import DiscoveryServer

from .constants import *
from .util import CallbackHelper


class UiServerNetworkException(Exception):
    pass


class UiServerCallbacks:
    def __init__(self):
        self.connect = CallbackHelper()
        self.disconnect = CallbackHelper()
        self.sendDriveMotor = CallbackHelper()

class UiServer:
  def __init__(self, callbacks):
    self.__dataLock = threading.RLock()
    self.__messageQueue = []
    
    self.__uiServerCallbacks = callbacks
    
    serverCallbacks = ServerCallbacks()

    serverCallbacks.connect = self.__uiServerCallbacks.connect
    serverCallbacks.disconnect = self.__uiServerCallbacks.disconnect
    serverCallbacks.message.register(self.onMessage)

    discovery = DiscoveryServer()
    discovery.start()

    self.__server = ThreadedWebSocketServer("ws://127.0.0.1:"+str(uiPort), serverCallbacks)

    self.__server.start()
    
  # Adds message to queue for processing
  def onMessage(self, message):
    self.__dataLock.acquire()
    self.__messageQueue.append(message[0])
    self.__dataLock.release()
    
  # Processes all messages on queue and fires there callbacks
  def processMessages(self):
    self.__dataLock.acquire()
    
    while self.__messageQueue:
        
      message = self.__messageQueue.pop(0)

      #Unlock mutex to avoid holding while signals are triggered
      self.__dataLock.release()
      
      self.decodeMessage(message)
      
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
      raise UiServerNetworkException("Invalid Message, too many commands (:)")
    
    
    if (command == CONST_SERVER_COMMAND_MOTOR_DRIVE):
      dataSplit = data.split(',')
      
      if len(dataSplit) != 2:
        raise UiServerNetworkException("DMC Command must have 2 params")
      
      left = dataSplit[0]
      right = dataSplit[1]
      
      print("Drive motor")
      self.__uiServerCallbacks.sendDriveMotor.invoke(left, right)
    else:
      print ("Unknown command:"+command)
      
  def announceLeftMotorSpeed(self, speed):
    self.__server.broadcastMessage(CONST_SERVER_ANN_DRIVE_MOTOR_LEFT_SPEED+":"+speed)

  def announceRightMotorSpeed(self, speed):
    self.__server.broadcastMessage(CONST_SERVER_ANN_DRIVE_MOTOR_RIGHT_SPEED+":"+speed)
