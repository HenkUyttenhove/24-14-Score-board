# 24-14-Score-board

This project includes the code for creating a basketball shotclock based upon PYCOM devices.

# How does it work
## The controller
The controller is a Pycom with MicroPython connected to three buttons.
1. Button 1 (P13) to reset to 24 sec
2. Button 2 (P14) to reset to 14 sec
3. Button 3 (P15) to start/stop the shotclock
> Note that pushing Button A and Button 2 simultaneous will create code "bb" for blanking display

The controller will create a wireless network (see boot.py) and will serve as a DHCP server.
When 2 displays are connected to the controller, the controller will start running sending out the "secs" using a UDP connection.

> Note that the Pycom has limited memory.  When an UDP can't be sent, it goes into cache and Pycom fails.  Therefore, a garbage collector (GC) has been created to avoid the Pycom to crash. No work-around found until now.

The controller will sent 2 bytes containing remaining seconds to the displays (see main.py)

To test the controller, run the script udpreceiver.py on any Python PC as it will act a simple receiver

## The display
The display is a project build upon a Pycom combined with a MCP23017 I2C processor.
The MCP23017 processor is connected to a dual LED seven-segment display (see more in subdirectory)

The display will connect to the wireless network of the Controller and show the counter.  
Two special states are defined besides the normal digits:
1. 'xx' time is up so a buzzer will be activated
2. 'bb' or blank.  This means nothing should be shown on the display
