# boot.py -- run on boot-up
import os
from machine import UART
uart = UART(0, 115200)
os.dupterm(uart)

# Code to allow WiFi during setup
# import machine
# from network import WLAN
# wlan = WLAN()
# if machine.reset_cause() != machine.SOFT_RESET:
#    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
#    wlan.ifconfig(config=('172.16.0.77', '255.255.255.0', '172.16.0.10', '8.8.8.8'))

# if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
#    wlan.connect('kawanda.be', auth=(WLAN.WPA2, 'gpz32914'), timeout=5000)
#    while not wlan.isconnected():
#        machine.idle() # save power while waiting
