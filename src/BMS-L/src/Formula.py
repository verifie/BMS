#!/usr/bin/python3
#

#########################################################################################################################################    
# Formula.py
# LIBRARY
# 
# BMS-L
# (c) 2020 Leighton Electronics
# 
# Description :         Building Management System Lighting Control Interface trials.
#
# Status :              25 - Start code interfacing tests and principle functions.
#
# Version History
# 2020/06/10 2237 v0.01 PME - Separate functions in to modules.


#########################################################################################################################################    
# Reference - useful information

# Interface Variables - For 16 port MCP23017 GPIO Expander Chips.  We use these at each local lighting / device control site (e.g. one per room or block)
# to sense and control.
#
# You set a bit in setPinInputOutputStateA (0x00) or setPinInputOutputStateB (0x01) to define whether the pin is in input or an output 1== input, 0 == output.
# You read input bits from GPIOA (0x12) or GPIOB (0x13) reading 1 == high, 0 == low.
# You write output bits to setOutputStateA (0x14) or setOutputStateB (0x15) where 1 == high and 0 == low.
#
# Syntax 
# bus.write_byte_data([device],[command],[Pin 7,6,5,4,3,2,1,0 addressed as an 8 bit binary number presented in HEX]
# e.g.
# bus.write_byte_data(Device003,setPinInputOutputStateA,0x80)
#
#                                                7 6 5 4 3 2 1 0
# ... tells device C, sets direction for pins    1 0 0 0 0 0 0 0
# ... the last pin is an input, the others are outputs.

# From the datasheet: When a bit is set, the corresponding pin becomes an input. When a bit is clear, the corresponding pinbecomes an output.




#########################################################################################################################################    
# Import External Libraries.

import RPi.GPIO as GPIO
# import MFRC522
# import signal
import time
import datetime

# Import Local Library
#from RemoteGPIO import RemoteGPIO
#RemoteGPIO = RemoteGPIO()

import Variables as v

#########################################################################################################################################    
# Initiate class.
class Formula(object):

    def __init__(self):
        print ("[LIBRARY] Formula.py \n")




    #########################################################################################################################################    
    # When addressing the external GPIO interfaces, we address a block of 8 each time in binary.  The first digit is Pin 0, last is pin 7, etc.
    # However, by default, the information is presented as a decimal, which is informative but not helpful for a quick human determination of
    # what is going on.  Ideally, we will also deal with it as a sequence of binary digits as opposed to a decimal to make the program easier
    # to read.
    def binary(self, num, pre='0b', length=8, spacer=0):

        binaryConverted = '{0}{{:{1}>{2}}}'.format(pre, spacer, length).format(bin(num)[2:])
        
        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print("[DEBUG]   binaryConverted :", binaryConverted)
        # DEBUG end

        # Now convert the binary data into a string.
        binaryConvertedString = str(self.binaryConverted)

        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print("[DEBUG]   binaryConvertedstring :", binaryConvertedString)
        # DEBUG end

        return binaryConvertedString

    

       
    #########################################################################################################################################   
    # convertBinaryString
    #
    # This is called if a trigger has been found. It checks to see if it was already requested and actions if not.

    def convertBinaryString(self, binary_string):
        binaryStringInt = int(binary_string, 2)

        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print("[DEBUG]   binaryStringInt :", binaryStringInt)
        # DEBUG end

        return binaryStringInt

