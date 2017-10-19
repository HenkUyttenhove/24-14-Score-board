# main.py -- put your code here!
from machine import Pin
import time
import socket
import gc

gc.enable()
gc.collect()

# set the inputs for 24/14/start-stop for the pins
p_24 = Pin('P13', mode=Pin.IN, pull=Pin.PULL_UP)
p_14 = Pin('P14', mode=Pin.IN, pull=Pin.PULL_UP)
p_start = Pin('P15', mode=Pin.IN, pull=Pin.PULL_UP)
addrA = ("172.16.1.1",1000)
addrB = ("172.16.1.11",1000)

# Activate UDP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create the class to do the countdown
class StopWatch:
    """ Implements a stop watch widget. """
    def __init__(self,timer = 24):
        self.start = 0.0     # Start time of timer
        self.timer = timer      # Countdown timer
        self.elapsedtime = 0.0  # How much time already expired
        self.running = 0    # Is countdown started
        self.warning = 0.0  # Early warning of timer
        self.timeUp = 0

    def update(self):
        """ Update the label with elapsed time. """
        if self.running:
            self.elapsedtime = int(time.time() - self.start)
            if int(self.elapsedtime + self.warning) >= int(self.timer):
                print("beep waarschuwing")
            if self.elapsedtime >= self.timer:
                print("tijd is afgelopen")
                self.running = 0
                self.timeUp = 1
            #    s.sendto("xx",addrA)
            #    s.sendto("xx",addrB)
                self.elapsedtime = self.timer

        if self.timeUp:
            self.min ="xx"
            self.sec ="xx"
        else:
            self.min = int((self.timer - self.elapsedtime)/60)
            self.sec = int(self.timer - self.elapsedtime - self.min*60.0)

    def Start(self,timer=24, warning=0):
        """ Start the stopwatch, ignore if running. """
        self.start = time.time()
        self.timer = timer
        self.warning = warning
        self.elapsedtime = 0.0
        self.timeUp = 0

    def ReStart(self):
        """ Start the stopwatch, ignore if running. """
        if not self.running:
            self.start = time.time() - self.elapsedtime
            self.running = 1
            self.update()

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self.running:
            self.running = 0
            self.update()

# Code required to use the timer
shotclock=StopWatch(24)

# Check if displays are ready
s.bind(("",1000))
data, addrA = s.recvfrom(10)
print("from:",addrA)
print("garbage collector:",gc.mem_free())
data, addrB = s.recvfrom(10)
print("from:",addrB)
print("garbage collector:",gc.mem_free())

while True:
    if p_24():
        shotclock.Start(24,0)
    if p_14():
        shotclock.Start(14,0)
    if p_start():
        shotclock.Stop()
    else:
        shotclock.ReStart()
    shotclock.update()
    print(shotclock.sec)
    print("garbage collector:",gc.mem_free())
    if p_24() and p_14():  #check if blanc screen
        s.sendto("bb",addrA)
        s.sendto("bb",addrB)
    else:
        s.sendto("%s" % shotclock.sec, addrA)
        s.sendto("%s" % shotclock.sec, addrB)
