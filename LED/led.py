from pynq import Overlay
from pynq import GPIO

ol= Overlay("./led.bit")
led=ol.axi_gpio_0
ch1=led.channel1
ch1[1].on()