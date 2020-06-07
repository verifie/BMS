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
print(" Dependencies:")
print("     1. Raspberry Pi 2,3 or 4. ")
print("     2. MCP23017 I2C Port Expanders at each local control location. ")
print("     3. I2C for local electronic communication, converting to Differential I2C for location to location comms. ")
print("     4. 24v DC supply, regulated to 5v and 3.3v at each local site.")
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


# Import Local Library
from RemoteGPIO import RemoteGPIO
RemoteGPIO = RemoteGPIO()

import Variables as v


#########################################################################################################################################    
# Create class.

class bmsl(object):

    def __init__(self):
        print ("init BMS-L") # never prints


    #########################################################################################################################################    
    # When addressing the external GPIO interfaces, we address a block of 8 each time in binary.  The first digit is Pin 0, last is pin 7, etc.
    # However, by default, the information is presented as a decimal, which is informative but not helpful for a quick human determination of
    # what is going on.  Ideally, we will also deal with it as a sequence of binary digits as opposed to a decimal to make the program easier
    # to read.
    def binary(self, num, pre='0b', length=8, spacer=0):
        return '{0}{{:{1}>{2}}}'.format(pre, spacer, length).format(bin(num)[2:])

    

    #########################################################################################################################################    
    # lookForTriggers
    def lookForTriggers(self, selectedDevice):

        # Pause in loop to allow OS Recovery and debug
        time.sleep(self.debounceDelay)

        # Read state of GPIOB register
        self.MySwitch = self.bus.read_byte_data(self.selectedDevice, self.GPIOA)
        # print("A input state:", self.MySwitch) # Debug print after first read.
    
        # This is really simply code for test.  If the state is different to the last actioned request, proceed to qualify the trigger.
        if not self.MySwitch == self.MySwitchCurrentState:


            ########################################################################
            # Software EMF Interference and Debounce filter.
            #
            # A trigger was acknowledged.  Action a software debounce to check for electrical interference or accidental trigger. We do this by:

            # DEBUG - Verbose announcer.
            if self.debug_verbose:
                print (" [TRIGGER] A new trigger was acknowledged but not yet put through our interference / debounce filter") # Dev code
            # DEBUG end

            # 1. Pausing for a moment so if this trigger was found as a result of momentary spike or interference, it has time to end (so the pause it acts as a software filter)..
            time.sleep(self.debounceDelay)

            # 2. Then we read the input again to check the reading is the same as the trigger.
            self.MySwitchDebounceReadA = self.bus.read_byte_data(self.selectedDevice, self.GPIOA)
            
            # 3. We then pause again, just in case the second read was also accidental.
            time.sleep(self.debounceDelay)

            # 4. Read again to check the reading is the same as the trigger.  A deliberate and intended trigger will persist, whilst noise is likely to be inconsistent, so
            # this technique should filter unintended triggers out.
            self.MySwitchDebounceReadB = self.bus.read_byte_data(self.selectedDevice, self.GPIOA)
            
            
            # 5. We then pause again, just in case the second read was also accidental.
            time.sleep(self.debounceDelay)

            # 6. Read again to check the reading is the same as the trigger.  A deliberate and intended trigger will persist, whilst noise is likely to be inconsistent, so
            # this technique should filter unintended triggers out.
            self.MySwitchDebounceReadC = self.bus.read_byte_data(self.selectedDevice, self.GPIOA)
            
            # 5. Now we compare the 4 reads.  If the trigger identified is the same on every read, action the trigger, else it was probably electrical noise, so ignore.
            # Because the reads are done so closely together, (speed in fractions of a second) - no multiple trigger state changes could possibly occur.  Importantly, what
            # we mere mortals consider fast is an age both in computer terms and EMF interference, so it's easy to spot.
            # If there is enough interference to fool this filter - it's time to rework the electronics and interfacing!
            if self.MySwitch == self.MySwitchDebounceReadA and self.MySwitch == self.MySwitchDebounceReadB and self.MySwitch == self.MySwitchDebounceReadC:

                # If we reach here, we believe the trigger was genuine.

                # DEBUG - Verbose announcer.
                if self.debug_verbose:
                    print (" [TRIGGER] A new trigger was acknowledged and passed the interference filter") # Dev code
                # DEBUG end

                # Update the Circuit State.
                self.changeCircuitState = True
            
            else:
                # We want to keep a tally of triggers that do not pass our debounce check.  This information will help us determine if there is excess interference causing false triggers
                self.debounceFail = self.debounceFail + 1



       
    #########################################################################################################################################   
    # convertBinaryString
    #
    # This is called if a trigger has been found. It checks to see if it was already requested and actions if not.

    def convertBinaryString(self, binary_string):

        return int(binary_string, 2)



            
    #########################################################################################################################################   
    # actionTrigger
    #
    # This is called if a trigger has been found. It checks to see if it was already requested and actions if not.

    def actionTrigger(self):
        
        # A trigger passed our tests and appeared genuine and was different to the current state. Increment the action tally
        self.actionTally = self.actionTally + 1

        # DEBUG - Verbose announcer.
        if self.debug_verbose:
            print("  [LOG] Action Tally : ", self.actionTally, " and Triggers that did not pass the debounce test :", self.debounceFail) # Shoe triggers - successful and unsuccessful.
        # DEBUG end

        # Read the bus status and interpret as a binary string.
        self.inputBusStatus = self.binary(self.MySwitch)
        humanBus = str(self.inputBusStatus)

        # DEBUG - Verbose announcer.
        if self.debug_verbose:
            print ("  [LOG] A new trigger was acknowledged.  Bus Read Status : ", self.inputBusStatus)  # Show the trigger:
        
            bitCount = 0
            for i in range(9, 1, -1):
                print ("  [LOG] Bit ", bitCount," Bus Read Status : ", humanBus[i])
                bitCount = bitCount + 1
        # DEBUG end

        # Action the request.
        self.room_light_circuit_A_status_INVERT(1)   # This toggles outputs on device A. For early development only.

        # Then record the state actioned to MySwitchCurrentState
        self.MySwitchCurrentState = self.MySwitch

        # Finally, set the change request state to False as we've actioned the change and there is nothing left to do in this cycle.
        self.changeCircuitState = False



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
        print(" [BOOT] .. Sending SMART MODE signal to all Local Switch Interfaces")
        #self.bus.write_byte_data(self.Device002, self.setOutputStateA, 1)      #TODO - this doesn't do anything useful. Do not enable yet!




    #########################################################################################################################################    
    # RunProgram
    #
    # This is run after everything is setup.

    def RunProgram(self):

        print(" [BOOT] Starting BMS-L Sequence")

        # Loop until user presses CTRL-C
        while True:

            # Select the switch device. #TODO Fixed at device 1 for now. Hook for dev.
            self.selectedDevice = self.Device001

            # Look for trigger (changes)
            self.lookForTriggers(self.selectedDevice)

            # Test to see if an action has been requested.
            if self.changeCircuitState:

                # A trigger request was made. #TODO Pass request on to action.
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
