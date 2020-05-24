#!/usr/bin/python3
#

#########################################################################################################################################    
# cardRW.py
# 
# BMS-L
# (c) 2020 Leighton Electronics
# 
# Description :         Building Management System Lighting Control Interface trials.
#
# Status :              25 - Start
#
# Version History
# 2020/05/23 2211 v0.00 PME - Start interface tests from demo at: https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-2/



# Simple print screen introduction
print("")
print("=============================================================================================================================================")
print("")
print("  MCP23017 I2C Port Expander ")
print("                                ")
print(" Copyright (c) Leighton Electronics 2020 Onwards. Patent Pending. NO UNAUTHORISED ACCESS PERMITTED. ")
print(" www.LeightonElectronics.co.uk ")
print("")
print("=============================================================================================================================================")
print("")
print("")



#########################################################################################################################################    
# Reference - useful information

# You set a bit in IODIRA (0x00) or IODIRB (0x01) to define whether the pin is in input or an output 1== input, 0 == output.
# You read input bits from GPIOA (0x12) or GPIOB (0x13) reading 1 == high, 0 == low.
# You write output bits to OLATA (0x14) or OLATB (0x15) where 1 == high and 0 == low.
#
# Syntax 
# bus.write_byte_data([device],[command],[Pin 7,6,5,4,3,2,1,0 addressed as an 8 bit binary number presented in HEX]
# e.g.
# bus.write_byte_data(DEVICEC,IODIRA,0x80)
#
#                                                7 6 5 4 3 2 1 0
# ... tells device C, sets direction for pins    1 0 0 0 0 0 0 0
# ... the last pin is an input, the others are outputs.

# From the datasheet: When a bit is set, the corresponding pin becomes an input. When a bit is clear, the corresponding pinbecomes an output.




#########################################################################################################################################    
# Import Libraries.

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import smbus


#########################################################################################################################################    
# Define Variables

room_light_circuit_A = 0x00
room_light_circuit_B = 0x01
room_light_circuit_C = 0x02

toggler = 0





#########################################################################################################################################    
# Define Variables - Friendly names for I2C Bus registers.  It makes it easier to read the code and relates to datasheet names at:
# http://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf
 
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

# To use more than 8 MCP23017 chips, a multiplexer is required, allowing the same address to be used. These are the multiplexer names.


# Address of MCP23017 being accessed.  Address can be changed to 1 of 8 options by setting pins A0, A1 and A2.
DEVICEA = 0x22 # Device address (A0-A2)
DEVICEB = 0x23 # Device address (A0-A2)
DEVICEC = 0x25 # Device address (A0-A2)

# Register to access Input / Output Direction Configuration.
IODIRA = 0x00 # Pin direction register A
IODIRB = 0x01 # Pin direction register B

# Register to Output Latches
OLATA  = 0x14 # Register for outputs A
OLATB  = 0x15 # Register for outputs B

# Register for Input
GPIOA  = 0x12 # Register for inputs A
GPIOB  = 0x13 # Register for inputs B




#########################################################################################################################################    
# Set Pin configuration as Input or Output.
# For our example, Bank A are OUTPUTs, Bank B are INPUTs


bus.write_byte_data(DEVICEC,IODIRA,0x00)
bus.write_byte_data(DEVICEC,IODIRB,0xFF)

 




#########################################################################################################################################    
#INPUT DEMO

# Loop until user presses CTRL-C
while True:
 
    # Read state of GPIOA register
    MySwitch = bus.read_byte_data(DEVICEC,GPIOB)
 
    print ("Read Status : ", MySwitch)

    if MySwitch & 0b10000000 == 0b10000000:
        print ("Switch was pressed!")
        
        bus.write_byte_data(DEVICEB,OLATA,toggler)

        # Invert light state
        if toggler = 1
            toggler = 0
        else:
            toggler = 1

        time.sleep(1)



#########################################################################################################################################    
# OUTPUT DEMO
 
# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICEA,IODIRA,0x00)
bus.write_byte_data(DEVICEB,IODIRA,0x00)
bus.write_byte_data(DEVICEC,IODIRA,0x00)
 
# Set output all 7 output bits to 0
bus.write_byte_data(DEVICEA,OLATA,0)
bus.write_byte_data(DEVICEB,OLATA,0)
bus.write_byte_data(DEVICEC,OLATA,0)
 
for MyData in range(1,999999000):
  mydatainv = MyData - 1
  # Count from 1 to 8 which in binary will count
  # from 001 to 111
  bus.write_byte_data(DEVICEA,OLATA,mydatainv)
  bus.write_byte_data(DEVICEB,OLATA,MyData)
  bus.write_byte_data(DEVICEC,OLATA,MyData)

  print (MyData)
  time.sleep(0.05)
 
# Set all bits to zero
bus.write_byte_data(DEVICEA,OLATA,0)
bus.write_byte_data(DEVICEB,OLATA,0)
bus.write_byte_data(DEVICEC,OLATA,0)