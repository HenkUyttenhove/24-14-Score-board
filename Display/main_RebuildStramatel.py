######################################
# main.py -- put your code here!
#  Developed by Henk Uyttenhove
#  Date: 16 Nov 2017
#  Based upon Pycom Wipy
#
#  No license, free to copy decode
#
######################################

import socket     # import the IP stack
import struct
import ubinascii
import time       # required to support the delay
from machine import Pin

#Translate the incoming code into display
Digit = [[1,1,1,1,1,0,1],\
         [0,0,1,1,0,0,0],\
         [0,1,1,0,1,1,1],\
         [0,1,1,1,1,1,0],\
         [1,0,1,1,0,1,0],\
         [1,1,0,1,1,1,0],\
         [1,1,0,1,1,1,1],\
         [0,1,1,1,0,0,0],\
         [1,1,1,1,1,1,1],\
         [1,1,1,1,1,1,0]]

# Pin layout on the Pycom
p1 = Pin('P5', mode=Pin.OUT)
p2 = Pin('P6', mode=Pin.OUT)
p3 = Pin('P7', mode=Pin.OUT)
p4 = Pin('P8', mode=Pin.OUT)
p5 = Pin('P11', mode=Pin.OUT)
p6 = Pin('P12', mode=Pin.OUT)
p7 = Pin('P19', mode=Pin.OUT)
Pbuzzer = Pin('P20', mode=Pin.OUT)
PA = Pin('P22', mode=Pin.OUT)
PB = Pin('P21', mode=Pin.OUT)
PA.value(0)     # display is not active
PB.value(0)     # display is not active
Pbuzzer.value(0) # buzzer is not active

#Set the network listner
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("172.16.0.202",1000))
sock.settimeout(0)
print("Listning mode enabled")
ShowDisplay = True
digitA = 0
digitB = 0
databuffer = ""

while True:
    data = sock.recv(2)  # Receive the information from the controller
    if data:    # check if the data has changed
        print("Ontvangen:", data)
        if len(data)==1:
            if (data[0]>47 and data[0]<58):
                databuffer = int(data)
                digitA = databuffer
                digitB = 0
                ShowDisplay = True
        else:
            if ((data[0]>47 and data[0]<58) and (data[1]>47 and data[1]<58)):
                databuffer = int(data)
                if databuffer < 10:
                    digitB = 0
                    digitA = databuffer
                else:
                    digitB = int(str(databuffer)[0])
                    digitA = int(str(databuffer)[1])
                ShowDisplay = True
            else:
                if data == b'dd':
                    print("buzzer")
                    Pbuzzer.value(1)
                    time.sleep(3)
                    Pbuzzer.value(0)
                if data == b'bb':
                    print("Blanc display")
                    ShowDisplay = False

    # Show the Digits on leds
    p1.value(Digit[digitA][0])
    p2.value(Digit[digitA][1])
    p3.value(Digit[digitA][2])
    p4.value(Digit[digitA][3])
    p5.value(Digit[digitA][4])
    p6.value(Digit[digitA][5])
    p7.value(Digit[digitA][6])
    if ShowDisplay:
        PA.value(1)
        time.sleep(0.005)
    PA.value(0)

    p1.value(Digit[digitB][0])
    p2.value(Digit[digitB][1])
    p3.value(Digit[digitB][2])
    p4.value(Digit[digitB][3])
    p5.value(Digit[digitB][4])
    p6.value(Digit[digitB][5])
    p7.value(Digit[digitB][6])
    if ShowDisplay:
        PB.value(1)
        time.sleep(0.005)
    PB.value(0)
