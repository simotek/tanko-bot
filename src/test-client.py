
# test client - Simon Lees simon@simotek.net
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

from PyLibs.uiclient import UiClient, UiClientCallbacks

import time

if __name__ == '__main__':
  
  clientCallbacks = UiClientCallbacks()

  uiClient = UiClient(clientCallbacks)

  count = 0

  # Main app event loop
  while True:
    uiClient.processMessages()
    time.sleep(0.01)
    
    count = count+1
    
    if count > 2000:
      count = 0
      
      uiClient.sendDriveMotorSpeed(0,0)
      
    elif count == 500:
      uiClient.sendDriveMotorSpeed(60,60)
    elif count == 1000:
      uiClient.sendDriveMotorSpeed(-60,-60)    
    elif count == 1500:
      uiClient.sendDriveMotorSpeed(60,-60)
