# List of components
## Raspberry PI
  * Aditional accesories
    * SD Card
    * Power Cable
    * wifi dongle
    * web cam (optional) I used a Logitech USB one.
## Display (Optional)
 I used the following one which wasn't designed for RPi and may not have kernel drivers mainlined so one known to work with a RPi would be better if we want one.
  * http://www.hardkernel.com/main/products/prdt_info.php?g_code=G142060963922

## Arduino
This one requires some soldering (I can do) It sits on the raspberry pi header and takes its power from the RPi
  * https://www.seeedstudio.com/Alamode-Arduino-Compatible-Raspberry-Pi-Plate-p-1285.html
## Chassis
I used this one https://www.aliexpress.com/item/DIY-499-AlloyTank-chassis-tracked-car-for-remote-control-robot-parts-for-maker-DIY-development-kit/32800326970.html?spm=2114.40010308.4.70.HNHgPp
  * Other slightly bigger options
    * https://www.aliexpress.com/item/Official-iSmaring-Tank-chassis-crawler-chassis-Climbing-obstacle-for-Crawler-robot-Model-Smart-Tank/32796402723.html?spm=2114.40010308.4.24.38KASi
    * https://www.aliexpress.com/item/T900-crawler-smart-car-4-x-4-metal-tank-chassis-Wall-e-robot-chassis-for-remote/1000002053934.html?spm=2114.40010308.4.2.LMaMMj
## Other electronics
### Motor controller
The chassis I got don't use servo's just 12V DC Motors, I used a L298n Dual H-Bridge board to control it (there are 100's to choose from so I picked one that looked nice)
  * http://www.dx.com/p/l298n-dual-h-bridge-dc-stepper-motor-driver-controller-for-arduino-robot-car-149107#.WUJ5Ga3-jRY 
### Voltage Regulator 
Converts 12V from the battery to 5V for the RPI
  * I picked one with a display so I could tell when the battery was getting flat.
      * http://www.dx.com/p/l298n-dual-h-bridge-dc-stepper-motor-driver-controller-for-arduino-robot-car-149107#.WUJ5Ga3-jRY
      
### Battery
I bought the biggest one I could find, it lasts atleast 6 hrs of light driving.
  * http://www.rcmodelscout.com/Batteries-and-Chargers/Turnigy-nano-tech-4500mah-3S-25-50C-Lipo-Pack/6841
