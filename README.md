# 24-14-Score-board

This project includes the code for creating a basketball shotclock based upon PYCOM devices.
See v3 to resolve the socket and WiFi problem

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
Note that we have two alternatives for the displays
- Build from scratch
- Modify legacy displays Stramatel (see lower)

### Build from scratch
The display is a project build upon a Pycom combined with a MCP23017 I2C processor.
The MCP23017 processor is connected to a dual LED seven-segment display (see more in subdirectory)

The display will connect to the wireless network of the Controller and show the counter.  
Two special states are defined besides the normal digits:
1. 'xx' time is up so a buzzer will be activated
2. 'bb' or blank.  This means nothing should be shown on the display

### Modify legacy displays Stramatel
The Legacy Stramatel system is build upon a 24v power switch connected to a Stramatel X3309 motherboard.  This board drives two big 7-segments red LED common cathode displays.

**Special remarks about the LED displays**
Every segment is build upon a parallel array of 7 red LED's with a resistance of 151 Ohm.  

The current will be (24v - 7x 2v)/151 Ohm = 66 mA or 3x to much for the LED display.  This is done because both 7-segment LEDS are sharing the anode connections and are activated via the two cathodes.  As a result, we have to target 50Hz or 20 msec activation for none flickering presentation.  Because we have two displays, we can only activate a display for 10 msec.  Therefore, the current is 3x higher than normal operations due to the short puls.  However, I have seen that the displays are suffering (after 10 years) from different broken LED's so this is not advised.  Better to put a ~350 Ohm resistance in the ring so we get 500 Ohm or 20 mA of current. 

# V3 Replacement of the WiPy with a LoPy so broadcast can be used
The WiPy device has very limited memory and a buggy network socket.  As a result, you can't use network broadcasting.  Due to the limited memory, the WiPy crashes when there are to much undelivered packages.
The solution is the LoPy device supporting LoRa.  This LoRa functionality is a broadcasting protocol so perfect for the clocks.  Note that an antenna is required for LoRa or the LoRa chip can get damaged. You can also disable WiFi after activation of LoRa. The code can be found in v3.
