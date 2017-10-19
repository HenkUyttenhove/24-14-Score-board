# main.py -- put your code here!
import socket     # import the IP stack
import struct
import time       # import required for delay for dooropener
from machine import Pin    # Control via pins the Keyes Funduino 4-relay board
# addr = socket.getaddrinfo('location.dyndns.org', 80)[0][-1] # only used in case of DNS resolution
from  machine import I2C
i2c = I2C(0,I2C.MASTER)
if not i2c.scan():
    print("I2C bus not ready")

I2Caddr = 0x20
IODIRA = 0x00
IODIRB = 0x01
OLATA = 0x14
OLATB = 0x15

#prepare GPA and GPB for output
i2c.writeto_mem(I2Caddr,IODIRA,0x00)
i2c.writeto_mem(I2Caddr,IODIRB,0x00)

#Translate the incoming code into display
ConvertDigit={'0':63,'1':6,'2':91,'3':79,'4':102,'5':109,'6':125,'7':7,'8':127,'9':111}

#Set the network listner
addr =('172.16.1.1',80)        # IP address to be used to connect
s = socket.socket()
s.bind(addr)        # bind the board to the IP address
s.listen(1)         # listen to a single session, no multiple connections allowed

#Get via http the code to show
while True:
    cl, port = s.accept()   # cl is the IP of connecting client, port is TCP port
    data = cl.recv(10)      # receive 10 bytes
    dataString = data.decode('utf-8')[-5:] #convert the bytes into string and take last 5 char
    digitA = dataString[0]      #Set the code to be used in the html call 172.16.0.30/D7jzF
    digitB = dataString[1]

    if digitA in ConvertDigit:
        print("DigitA:",int(ConvertDigit[digitA]))
        ShowDigitA = int(ConvertDigit[digitA])
    else:
        ShowDigitA = 0

    if digitB in ConvertDigit:
        print("DigitB:",int(ConvertDigit[digitB]))
        ShowDigitB = int(ConvertDigit[digitB])
    else:
        ShowDigitB = 0

    i2c.writeto_mem(I2Caddr,OLATA,ShowDigitA)
    i2c.writeto_mem(I2Caddr,OLATB,ShowDigitB)
    cl.close()
s.close()
