# boot.py -- run on boot-up
import os
import machine

uart = UART(0, 115200)
os.dupterm(uart)

from network import WLAN
wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    wlan.antenna(1)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(id=0,config='dhcp')
    print("WLAN details:",wlan.ifconfig())

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('basket1000', auth=(WLAN.WPA2, 'gpz32914'), timeout=5000)
