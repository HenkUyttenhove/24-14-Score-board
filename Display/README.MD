# Display of the 24/14 shot clock

#Introduction
It's possible to buy a ready-to-use display but it's more fun to build one yourself.  
What is required?
- LED-strip (red strip is ok)
- MCP23017 I2C chip to get more I/O ports
- PyCom WiPY processor
- 15x BS 170 MOSFET
- 15x Resistor 100k 
- Power supply 12V (LED strip), 5V (PyCom)

## Network diagram
> See also DisplayWires.png

The MCP23017 is connected to the PyCom via I2C
 SCL (pin12) - SCL (pin10)
 SDA (pin13) - SDA (pin9)
 The MCP23017 is put on address 0x20 so A0/A1/A2 (pin15-pin17) are grounded
 The MCP23017 RESET (pin18) is connected to power
 
 The output of the MCP23017 is connected to the segments of the digits via a MOSFET. The MOSFET base is connected to ground with a 100k resistant to avoid wrong detection of input.  Not required.
 GPA0 - GPA6 are segments of LED1
 GPA7 is the buzzer
 GPB0 - GPB6 are segments of LED2
 
 > See other images in the folder for photo's
