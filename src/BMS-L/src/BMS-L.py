#!/usr/bin/python3
#

#########################################################################################################################################    
# BMS-L.py
# RUN PROGRAM
# 
# BMS-L
# (c) 2020 Leighton Electronics
# 
# Description :         Building Management System Lighting Control Interface trials.
#
# Status :              25 - Start code interfacing tests and principle functions.
#
# Version History
# 2020/05/23 2211 v0.00 PME - Start interface tests from demo at: https://www.raspberrypi-spy.co.uk/2013/07/how-to-use-a-mcp23017-i2c-port-expander-with-the-raspberry-pi-part-2/
# 2020/05/23 2211 v0.01 PME - Interfacing tests complete.  Now develop the logic for light control. Move into a Class / Function Object Oriented Code structure.
# 2020/05/27 0900 v0.02 PME - Installing class system. Remove test code that poked interface.  Changed variables to friendlier names, although they no longer match the example or datasheet.
# 2020/05/27 1107 v0.03 PME - Fix control logic.  The prior software flips the light on for a moment.  Multiple read fails too. So tidy up code and logic sequence.
# 2020/05/27 1208 v0.04 PME - Improve trigger detection - If switch is pressed, dont toggle on or off all the time. A plan will be needed, but lets test some ideas.
# 2020/05/31 1035 v0.05 PME - Trialing next stage breadboard.  All B IO is Led control output.  All A IO is Input. Pre-Bugfix.
# 2020/06/06 1523 v0.06 PME - Separate functions in to modules.
# 2020/06/11 2020 v0.07 PME - Adding binary decoding and enconding to read and write to the remote GPIO chips.

# Simple print screen introduction
print("")
print("==================================================================================================================")
print("")
print("  _________  ________  ")
print("  | ___ |  \/  /  ___| ")
print("  | |_/ | .  . \ `--.  ")
print("  | ___ | |\/| |`--. \ ")
print("  | |_/ | |  | /\__/ /    BMS-L - Building Management System - Smart Environment Control (Lighting)")
print("  \____/\_|  |_\____/  ")
print("                       ")
print("")
print(" Dependencies: (Proposed)")
print("     1. Raspberry Pi 2,3 or 4. ")
print("     2. MCP23017 I2C Port Expanders at each local control location. ")
print("     3. I2C for local electronic communication, converting to Differential I2C for location to location comms. ")
print("     4. 24v or 12v DC supply, regulated to 5v and 3.3v at each local site.")
print("")
print(" Copyright (c) Leighton Electronics 2020 Onwards. Patent Pending. NO UNAUTHORISED ACCESS PERMITTED. ")
print(" www.LeightonElectronics.co.uk ")
print("")
print("==================================================================================================================")
print("")
print("")



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
from RemoteGPIO import RemoteGPIO
RemoteGPIO = RemoteGPIO()

from Formula import Formula
Formula = Formula()

import Variables as v
print("[BOOT]    Debug state =", v.debug_verbose)

#########################################################################################################################################    
# Create class.

class bmsl(object):

    def __init__(self):
        print ("[INIT]    BMS-L")

    
            
    #########################################################################################################################################   
    # actionTrigger
    #
    # This is called if a trigger has been found. It checks to see if it was already requested and actions if not.

    def actionTrigger(self):
        
        # Log the request
        now = datetime.datetime.now()
        print ("\n\n[ACTION]  A lighting state change was acknowledged.")
        print ("[LOG]     Current date and time : ", now.strftime("%Y-%m-%d %H:%M:%S"))

        # A trigger passed our tests and appeared genuine and was different to the current state. Increment the action tally
        v.actionTally = v.actionTally + 1

        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print("[LOG]     Action Tally : ", v.actionTally, " and Triggers that did not pass the debounce test :", v.debounceFail) # Shoe triggers - successful and unsuccessful.
        # DEBUG end

        # Read the bus status and interpret as a binary string.
        self.inputBusStatus = Formula.binary(v.MySwitch)
        

        # Now count the binary string and convert into Hex.
        OutputStateChange = Formula.binaryStringToHex(self.inputBusStatus)

        # Action the request.
        circuitID = 1
        #RemoteGPIO.room_light_circuit_A_status_INVERT(1)   # This toggles outputs on device A. For early development only.
        RemoteGPIO.actionSwitch(circuitID, OutputStateChange)

        # Then record the state actioned to MySwitchCurrentState
        v.MySwitchCurrentState = v.MySwitch

        # Finally, set the change request state to False as we've actioned the change and there is nothing left to do in this cycle.
        v.changeCircuitState = False



    #########################################################################################################################################   
    # setBMSLive
    #
    # To offer some protection against system BMS microcontroller failure (any condition), the local circuit switch interfaces default to a simple
    # local switch trigger, with the primary light circuit ON and the rest off.  We change that state by turning on pin 8 (0 to 7, so pin 7 really)
    # at the local GPIO interface to make the local switch interface do what the BMS microcontroller tells it (SMART MODE)
    #
    # TODO: A bit-bash clock system (BMS heartbeat) would be better, so if the program ceases to function, the heartbeat would fail in an either on
    # or off position, causing the local switch interface to revert to simple mode.  That will require local electronics to detect a bit-bashed irregular
    # clock, however - so we'll leave that out of version 1 for now...

    def setBMSLive(self):

        # Read current state of pins.

        # Set pin 7 HIGH.
        print("[BOOT]    Sending SMART MODE signal to all Local Switch Interfaces")
        #self.bus.write_byte_data(self.Device002, self.setOutputStateA, 1)      #TODO - this doesn't do anything useful. Do not enable yet!




    #########################################################################################################################################    
    # RunProgram
    #
    # This is run after everything is setup.

    def RunProgram(self):

        print ("\n\n[RUN]     Starting BMS-L State Machine.")

        # Loop until user presses CTRL-C
        while True:

            # Select the switch device. #TODO Fixed at device 1 for now. Hook for dev.
            self.selectedDevice = v.Device001

            # Look for trigger (changes)
            RemoteGPIO.lookForTriggers(self.selectedDevice, v.MySwitchCurrentState) # TODO: Note this just passes 0, so anything other than 0 will flag to any state change challenge. Change this to refer to the actual current state of lights! DEBUG.

            # Test to see if an action has been requested.
            if v.changeCircuitState:

                # A trigger request was made. #TODO Pass request on to action.  At the moment, it just calls the function which turns everything on or off (inverts).
                self.actionTrigger()

            # End of RunProgram Loop. Restarting.


###########################################################################################################################################################################
# Define Class Names
environmentController = bmsl()



###########################################################################################################################################################################
# Run the program

# Setup Local GPIO expander ICs - sense or control.  Then set the start state of pins.
RemoteGPIO.setPinDirection()
RemoteGPIO.setGPIOStartTest()
RemoteGPIO.setGPIOStartState()

# Tell the local switch interfaces we're up and running.
environmentController.setBMSLive()

# Start the run program.  This is a loop.
environmentController.RunProgram()
