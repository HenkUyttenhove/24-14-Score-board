# main.py -- put your code here!
########################################################
#  Code developed by Henk Uyttenhove
#  Date: 22 nov 2018
#
#  Code is not limited to any license and is free to use
########################################################

from machine import Pin   # control the pins for the buttons
from machine import Timer # Support delays in the code
from machine import WDT   # watchdog timer so when failure, reboot device
import time               # convert time format
import socket             # network stack
import gc                 # Garbage collector.  Acts as buffer during problems

gc.enable()
gc.collect()

# set the inputs for 24/14/start-stop for the pins
p_24 = Pin('P13', mode=Pin.IN, pull=Pin.PULL_UP)   #24 seconds reset
p_14 = Pin('P14', mode=Pin.IN, pull=Pin.PULL_UP)   #14 seconds reset
p_hold = Pin('P15', mode=Pin.IN, pull=Pin.PULL_UP) #hold clock
addrA = ("172.16.1.100",1000)                      # display 1
addrB = ("172.16.1.200",1000)                      # display 2
Clock24 = 24                                       # set time of 24 sec
Clock14 = 14                                       # set time of 12 sec
chrono = Timer.Chrono()                            # actual counter for 24/14
updateTimer = Timer.Chrono()                       # timer for the network updates
updateTimer.start()
chrono.stop()
chrono.reset()                                     # stop and reset chrono before running code
chronoclock = Clock24                              # define the countdown timer (14 of 24 seconds)
remaining = 0                                      # how many seconds remaining
showClock = True                                   # should displays be active
buzzer = False                                     # should buzzer be active

# Activate The network
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
wdt = WDT(timeout=10000)  #autoreboot after 10 seconds if no solution
while not wlan.isconnected():
    time.sleep(1)
print("Sender mode enabled")
sock.settimeout(0.3)
print("program started")
# Define the procedure to update via network
def updateClocks(remaining,show,buzzer):
    if buzzer:
        sock.sendto(b"dd",addrA)
        sock.sendto(b"dd",addrB)
    if show:
        sock.sendto(b"%s" % remaining,addrA)
        sock.sendto(b"%s" % remaining,addrB)
    else:
        sock.sendto(b"bb",addrA)
        sock.sendto(b"bb",addrB)

# The actual code to run the controller
while True:
    wdt.feed()                       # Feed the watchdog timer.  If no puls, reboot after 10 sec
    if p_24():                       # the 24sec button is pushed
        chronoclock = Clock24
        chrono.reset()
    if p_14():                       # the 14sec button is pushed
        chronoclock = Clock14
        chrono.reset()
    if p_hold():                     # the switch to stop counting is active
        chrono.stop()
    else:
        chrono.start()
    if p_24() and p_14():            # if 24 and 14 sec button are pushed simultaneous
        showClock = False
    else:
        showClock = True

    if (chrono.read()+1) >= chronoclock:       # check if the crono has passed the preset counter
        remaining = 0                          # when time has expired, show 0 on the displays
        if not (chrono.read()+1) >= (chronoclock +1):    # 1 seconds buzzer (will be 2 buzzers because update every 0.3 sec)
            buzzer = True
        else:
            buzzer = False
    else:
        remaining = int(chronoclock-round(chrono.read()))     # show remaining time on displays

# update via het netwerk
    if int(updateTimer.read_ms()) > 300:      # only update every 0.3 sec (to lower the networkload)
        updateClocks(remaining,showClock,buzzer)
        updateTimer.reset()
