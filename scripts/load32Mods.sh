#!/bin/bash
modprobe spicc
sudo modprobe fbtft_device name=odroidc_tft32 rotate=270 gpios=reset:116,dc:115 speed=32000000 cs=0
