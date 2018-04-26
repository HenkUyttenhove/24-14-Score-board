# main.py -- put your code here!

# LoRA raw mode between devices
from network import LoRa
import socket
import time

# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

from machine import Pin
from machine import Timer
from machine import WDT

# set the inputs for 24/14/start-stop for the pins
p_24 = Pin('P13', mode=Pin.IN, pull=Pin.PULL_UP)   #24 seconds reset
p_14 = Pin('P14', mode=Pin.IN, pull=Pin.PULL_UP)   #14 seconds reset
p_hold = Pin('P15', mode=Pin.IN, pull=Pin.PULL_UP) #hold clock
Clock24 = 24
Clock14 = 14
chrono = Timer.Chrono()
updateTimer = Timer.Chrono()
updateTimer.start()
chrono.stop()
chrono.reset()
chronoclock = Clock24
remaining = 0
showClock = True
buzzer = False
buzzerTimer = Timer.Chrono()  #define how long buzzer may work
buzzerTimer.stop()
buzzerTimer.reset()

wdt = WDT(timeout=10000)  #autoreboot after 10 seconds if no solution

# Define the procedure to update via network
def updateClocks(remaining,show,buzzer):
    if buzzer:
        s.send('dd')
    else:
        if show:
            s.send('%s' % remaining)
        else:
            s.send('bb')

while True:
    wdt.feed()
    if p_24():
        chronoclock = Clock24
        chrono.reset()
        buzzercounter = 0
    if p_14():
        chronoclock = Clock14
        chrono.reset()
        buzzercounter = 0
    if p_hold():
        chrono.stop()
    else:
        chrono.start()
    if p_24() and p_14():  #check if blanc screen
        showClock = False
    else:
        showClock = True

    if (chrono.read()+1) >= chronoclock:
        buzzerTimer.start()
        if int(buzzerTimer.read_ms()) < 500:  #buzzer will work for 500 msec
                buzzer = True
        else:
            buzzer = False
            buzzerTimer.stop()
        remaining = 0
    else:
        remaining = int(chronoclock-round(chrono.read()))
        buzzerTimer.reset()

# update via het netwerk
    if int(updateTimer.read_ms()) > 300:
        updateClocks(remaining,showClock,buzzer)
        updateTimer.reset()
