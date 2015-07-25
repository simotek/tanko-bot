/*
Motor Control - Simon Lees simon@simotek.net
Copyright (C) 2015 Simon Lees

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

// Pins In USE
// Motor PWM
int PIN_LEFT_REV = A3;
int PIN_LEFT_FOR = A2;

int PIN_LEFT_SPEED = 3;


int PIN_RIGHT_REV = A1;
int PIN_RIGHT_FOR = A0;

int PIN_RIGHT_SPEED = 5;


// Serial Pins are only used by the Serial Driver
int PIN_SERIAL_RX = 0;
int PIN_SERIAL_TX = 1;

// Note SPI Pins are Used by the ODROID
int PIN_SPI_SS   = 10;
int PIN_SPI_MOSI = 11;
int PIN_SPI_MISO = 12;
int PIN_SPI_SCK  = 13;

// Note I2C Pins are Used by the ODROID
int PIN_I2C_SDA  = 27;
int PIN_I2C_SCL  = 28;

// Command Strings
// // Incoming
String CMD_IN_DRIVE_MOTOR_CTRL = "DMC";
String CMD_IN_PROGRAM = "PROG";         // Sets spi lines back to high impedence for ISP

// // Outgoing
String CMD_OUT_READY = "READY";
String CMD_OUT_DRIVE_MOTOR_LEFT_SPEED = "DMLS";
String CMD_OUT_DRIVE_MOTOR_RIGHT_SPEED = "DMRS";

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

// the setup function runs once when you press reset or power the board
void setup() {

  // Motor pins as outputs
  pinMode(PIN_LEFT_REV,   OUTPUT);
  pinMode(PIN_LEFT_FOR,   OUTPUT);
  pinMode(PIN_RIGHT_REV,  OUTPUT);
  pinMode(PIN_LEFT_SPEED, OUTPUT);
  pinMode(PIN_RIGHT_FOR,  OUTPUT);
  pinMode(PIN_RIGHT_SPEED,OUTPUT);

  leftMotorSpeed(0);
  rightMotorSpeed(0);

  // Wait 10 seconds before starting to give the ISP programmer a chance to kick in
  //  Will remove once the prog command is tested
  delay(2000);

  // initialize digital pin b2-b5 as input so they can be used as spi bus
  digitalWrite(PIN_SPI_SS, LOW);
  digitalWrite(PIN_SPI_MOSI, LOW);
  digitalWrite(PIN_SPI_MISO, LOW);
  digitalWrite(PIN_SPI_SCK, LOW);

  // SPI Pins are inputs
  pinMode(PIN_SPI_SS, INPUT);
  pinMode(PIN_SPI_MOSI, INPUT);
  pinMode(PIN_SPI_MISO, INPUT);
  pinMode(PIN_SPI_SCK, INPUT);


  inputString.reserve(200);  // Reserve space for incoming command
  Serial.begin(115200);      // open the serial port at 9600 bps:

  Serial.print(CMD_OUT_READY+"\n");
}

// the loop function runs over and over again forever
void loop()
{
  // Decode the string when a newline arrives:
  if (stringComplete)
  {
    // Temp debug code
    String echo = String("echo:");
    Serial.println(echo+inputString);
    String DecodeString = inputString;
    // clear the string early incase more comes in
    inputString = "";
    stringComplete = false;

    // Decode commands
    //   Extract command name before (:)
    DecodeString.trim();
    String CMDString;
    String DataString;

    int DecodeSplit = DecodeString.indexOf(':');
    if (DecodeSplit == -1)
    {
       CMDString = DecodeString;
    }
    else
    {
       CMDString = DecodeString.substring(0,DecodeSplit);
       DataString = DecodeString.substring(DecodeSplit+1);
    }

    // Main Drive Motor Control, value from -100 to 100
    if (CMDString == CMD_IN_DRIVE_MOTOR_CTRL)
    {
       int DataSplit = DataString.indexOf(',');
       String LeftStr = String("0");
       String RightStr = String("0");
       if (DataSplit == -1)
       {
          LeftStr = DataString;
       }
       else
       {
         LeftStr = DataString.substring(0,DataSplit);
         RightStr = DataString.substring(DataSplit+1);
       }

       leftMotorSpeed(LeftStr.toInt());
       rightMotorSpeed(RightStr.toInt());
    }
    else if (CMDString == CMD_IN_PROGRAM)
    {
       // SPI Pins back to High for ISP
       digitalWrite(PIN_SPI_SS,   HIGH);
       digitalWrite(PIN_SPI_MOSI, HIGH);
       digitalWrite(PIN_SPI_MISO, HIGH);
       digitalWrite(PIN_SPI_SCK,  HIGH);

       Serial.print(CMD_OUT_READY+" Program\n");
    }
  }

}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;

    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

// Sets left Motor Speed -100 to 100
void leftMotorSpeed(int Speed)
{
   char Direction = 'N';
   if (Speed == 0 ||
       Speed > 100 ||
       Speed < -100)
   {
     Speed = 0;
     digitalWrite(PIN_LEFT_FOR, LOW);
     digitalWrite(PIN_LEFT_REV, LOW);
     analogWrite(PIN_LEFT_SPEED,0);
   }
   else if (Speed < 0)
   {
     Direction = 'R';
     Speed = Speed*-1;
     // Convert from 0-100 to 0-255
     digitalWrite(PIN_LEFT_FOR, LOW);
     digitalWrite(PIN_LEFT_REV, HIGH);
     analogWrite(PIN_LEFT_SPEED,(Speed*255)/100);
   }
   else
   {
     Direction = 'F';
     digitalWrite(PIN_LEFT_FOR, HIGH);
     digitalWrite(PIN_LEFT_REV, LOW);
     analogWrite(PIN_LEFT_SPEED,(Speed*255)/100);
   }
   Serial.print(CMD_OUT_DRIVE_MOTOR_LEFT_SPEED+":"+Speed+","+Direction+"\n");
}

void rightMotorSpeed(int Speed)
  {
    char Direction = 'N';
    if (Speed == 0 ||
       Speed > 100 ||
       Speed < -100)
     {
       Speed = 0;
       digitalWrite(PIN_RIGHT_FOR, LOW);
       digitalWrite(PIN_RIGHT_REV, LOW);
       analogWrite(PIN_RIGHT_SPEED,0);
     }
     else if (Speed < 0)
     {
       Speed = Speed*-1;
       Direction = 'R';
       // Convert from 0-100 to 0-255
       digitalWrite(PIN_RIGHT_FOR, LOW);
       digitalWrite(PIN_RIGHT_REV, HIGH);
       analogWrite(PIN_RIGHT_SPEED,(Speed*255)/100);
     }
     else
     {
       Direction = 'F';
       digitalWrite(PIN_RIGHT_FOR, HIGH);
       digitalWrite(PIN_RIGHT_REV, LOW);
       analogWrite(PIN_RIGHT_SPEED,(Speed*255)/100);
     }
     Serial.print(CMD_OUT_DRIVE_MOTOR_RIGHT_SPEED+":"+Speed+","+Direction+"\n");
}
