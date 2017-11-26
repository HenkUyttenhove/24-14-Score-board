# Display of the 24/14 shot clock

# Introduction
This project started off as a make-it-yourself project so combining different components into a physical display.

A first display was built but due to the extensive work, a second version was based upon the adaptation of existing Stramatel displays.

Note that in the code, you can find two files.  This is typical to PyCom
- boot.py: All code required to boot the device (typical networking)
- main.py: The actual code required to run the controller

See a clock in action [mp4 movie](https://github.com/HenkUyttenhove/24-14-Score-board/blob/master/IMG/20171006_184051.mp4)

# Do-it-yourself display (v1)

It's possible to buy a ready-to-use display but it's more fun to build one yourself.  
What is required?
- LED-strip (red strip is ok)
- MCP23017 I2C chip to get more I/O ports
- PyCom WiPY processor
- 15x BS 170 MOSFET
- 15x Resistor 100k
- Power supply 12V (LED strip), 5V (PyCom)

 ## Network diagram
*How does it work?*

The main controller is the Pycom WiPy.  This small controller is very cost effective and running MicroPython.  The Pycom controller will receive two digits using UDP and will translate the two digits into the required code to light up the display.

We have two options to controle the dislay:
1. 7-LED display swapping. We will have an alternating activation of the displays. So we will activate display A-B-A-B-A-B.....
 - Advantage: Limited requirement for IO ports.  7 for LEDS + kathode A + kathode B = 9 IO ports.
  - Disadvantage: Alternating frequency needs to be above 50 msec to avoid flickering.  Also the brightness will be lower due to none permanent powering of LED's.
2. Independent 7-LED display controllers
  - Advantage: No flickering and easy to implement
  - Disadvantage: Need for more IO ports. 2x 7 LEDS = 14 ports.

For the do-it-yourself display, we go for option 2.  To solve the issue of limited IO ports on the Pycom, an external MCP23017 I2C chip is deployed.

> Note: that MicroPython has some serious limitations on networking like multicasting not supported.  (only UDP/TCP and LoRA)

 See  [Network diagram](https://github.com/HenkUyttenhove/24-14-Score-board/blob/master/IMG/DisplayWiresv1.jpg)

The MCP23017 is connected to the PyCom via I2C
 SCL (pin12) - SCL (pin10)
 SDA (pin13) - SDA (pin9)
 The MCP23017 is put on address 0x20 so A0/A1/A2 (pin15-pin17) are grounded
 The MCP23017 RESET (pin18) is connected to power

 The output of the MCP23017 is connected to the segments of the digits via a MOSFET. The MOSFET base is connected to ground with a 100k resistant to avoid wrong detection of input.  (optional).
 GPA0 - GPA6 are segments of LED1
 GPA7 is the buzzer
 GPB0 - GPB6 are segments of LED2

 # Modification of existing Stramatel display (v2)
 Note that this can also be used for do-it-yourself07

 What is required?
 - Stramatel 24/14 display [Photo](https://github.com/HenkUyttenhove/24-14-Score-board/blob/master/IMG/Stramatel.jpg)
 - Pycom Wipy Controller
 - 7x 330k Ohm resistant to protect display (optional)
 - ULN2803 (high current device)
 - 3x VNP20N07 MosFET (kathode display A&B, buzzer)

 ## Network diagram
 *How does it work?*

 The Pycom is connected to 7 channels of the ULN2803 converting the 3.3V output of Pycom into 24V.  The 24V signals are connected to the 7 LED-segments of both displays.  
 Both displays have independent cathode (ground port) connections.  These are connected to the VNP20N07 MosFet so when the Pycom drives the MosFet, the cathode of the display is connected to the ground.

 So the Pycom uses 7 IO ports to power 24V to the 7 LED segments of both displays.  However only when the cathode of a display is connected to ground, it will light up.
 Example: Pycom puts code of Display A on 7 LED segments and activates cathode of display A.  After deactivation of cathode display A, Pycom puts code of Display B on 7 LED segments and activates cathode of display B.  This is done in a alternating way.

 See [Network diagram](https://github.com/HenkUyttenhove/24-14-Score-board/blob/master/IMG/schemeStramatel.jpg)

## Software coding
Note that for the coding, the self-made project is using code based upon a clock.  It reads the actual time and calculate the difference between start and actual to define the past time.

For the Stramatel project, another concept was used.  The Pycom supports two interesting libraries.  The first is a Chrono and the second is a Watchdog process.  The Chrono allows a major simplification of the code due to no recalculation of time.
The Watchdog library allows an automatic reboot if the process breaks.  This can happen when the controller can't reach the displays using UDP.  The controller will crash due to the limited memory of the Pycom for caching network traffic.

### Remark concerning the WiFi set-up
Due to the limited memory of the Pycom, a failing connection from the controller to the displays will crash the Pycom. With the Watchdog process, the controller will reboot and retry the connection.
However, due to the reboot of the controller, it's not advised to use the controller as the AP (Access Point).
> Note: When the controller reboots and acts as AP, the displays will also need to resync with the AP.  When the controller tries to connect before the display is synced, the controller will fail and reboot again. You are in a loop.  Solution, use external AP or configure a displays as AP.
