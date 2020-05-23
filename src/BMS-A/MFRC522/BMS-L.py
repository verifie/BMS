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
print("  MCP23017 I2C Port Expander "
print("                                ")
print(" Copyright (c) Leighton Electronics 2020 Onwards. Patent Pending. NO UNAUTHORISED ACCESS PERMITTED. ")
print(" www.LeightonElectronics.co.uk ")
print("")
print("=============================================================================================================================================")
print("")
print("")


#########################################################################################################################################    
# Import Libraries.

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import smbus
 
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
 
DEVICE = 0x22 # Device address (A0-A2)
IODIRA = 0x00 # Pin direction register
OLATA  = 0x14 # Register for outputs
GPIOA  = 0x12 # Register for inputs
 
# Set all GPA pins as outputs by setting
# all bits of IODIRA register to 0
bus.write_byte_data(DEVICE,IODIRA,0x00)
 
# Set output all 7 output bits to 0
bus.write_byte_data(DEVICE,OLATA,0)
 
for MyData in range(1,8):
  # Count from 1 to 8 which in binary will count
  # from 001 to 111
  bus.write_byte_data(DEVICE,OLATA,MyData)
  print MyData
  time.sleep(1)
 
# Set all bits to zero
bus.write_byte_data(DEVICE,OLATA,0)