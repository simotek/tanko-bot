
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

from PyLibs.uiserver import UiServer, UiServerCallbacks

import argparse
import time

uiServer = None

# only used when serial is stubbed out
def onDriveMotor(args):
  print("On DriveMotor")
  
  uiServer.announceLeftMotorSpeed(args[0])
  uiServer.announceRightMotorSpeed(args[1])

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser("Main Robot control app")
  #parser.add_argument("-s", "--no-serial", type=str, required=False, help="Stub out serial")
  parser.add_argument('--no-serial', dest='noserial', action='store_true')
  
  args = parser.parse_args()
  
  serverCallbacks = UiServerCallbacks()

  # hook up stub callbacks
  if args.noserial:
    serverCallbacks.sendDriveMotor.register(onDriveMotor)

  uiServer = UiServer(serverCallbacks)


  # Main app event loop
  while True:
    uiServer.processMessages()
    time.sleep(0.01)