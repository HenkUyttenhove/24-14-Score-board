# boot.py -- run on boot-up
import os
import machine

uart = UART(0, 115200)
os.dupterm(uart)

from network import WLAN
wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.AP, ssid='basket1000', auth=(WLAN.WPA2,'gpz32914'), channel=7, antenna=WLAN.INT_ANT)
# set the DHCP server
    wlan.ifconfig(id = 1, config = ('172.16.1.10', '255.255.255.0', '0.0.0.0', '0.0.0.0'))
