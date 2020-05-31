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

# Simple print screen introduction
print("")
print("=============================================================================================================================================")
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
print("                                ")
print(" Copyright (c) Leighton Electronics 2020 Onwards. Patent Pending. NO UNAUTHORISED ACCESS PERMITTED. ")
print(" www.LeightonElectronics.co.uk ")
print("")
print("=============================================================================================================================================")
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
# bus.write_byte_data(DEVICEC,setPinInputOutputStateA,0x80)
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
# Create class.

class bmsl(object):


    #########################################################################################################################################    
    # Define Variables

    # Software variables.

    print (" ... Setup default variables.")


    changeCircuitState = False
    MySwitchCurrentState = 0
    inputBusStatus = 0x00

    room_light_circuit_A = 0x00
    room_light_circuit_A_status = False

    room_light_circuit_B = 0x01
    room_light_circuit_B_status = False

    room_light_circuit_C = 0x02
    room_light_circuit_A_status = False

    toggler = 0
    actionTally = 0
    PrintOnce = True
    debounceDelay = 0.02

    # Friendly names for I2C Bus registers.  It makes it easier to read the code and relates to datasheet names at:
    # http://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf
    # To use more than 8 MCP23017 chips, a multiplexer is required, allowing the same address to be used. These are the multiplexer names.

    #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    bus = smbus.SMBus(1) # Rev 2 Pi uses 1

    # Address of MCP23017 being accessed.  Address can be changed to 1 of 8 options by setting pins A0, A1 and A2.
    DEVICEA = 0x20 # Device address (A0-A2)
    DEVICEB = 0x21 # Device address (A0-A2)
    DEVICEC = 0x22 # Device address (A0-A2)

    # Register to access Input / Output Direction Configuration.
    setPinInputOutputStateA = 0x00 # Pin direction register A
    setPinInputOutputStateB = 0x01 # Pin direction register B

    # Register to Output Latches
    setOutputStateA  = 0x14 # Register for outputs A
    setOutputStateB  = 0x15 # Register for outputs B

    # Register for Input
    GPIOA  = 0x12 # Register for inputs A
    GPIOB  = 0x13 # Register for inputs B

    print (" ... Setup default variables. DONE \n\n")



    #########################################################################################################################################    
    # When addressing the external GPIO interfaces, we address a block of 8 each time in binary.  The first digit is Pin 0, last is pin 7, etc.
    # However, by default, the information is presented as a decimal, which is informative but not helpful for a quick human determination of
    # what is going on.  Ideally, we will also deal with it as a sequence of binary digits as opposed to a decimal to make the program easier
    # to read.
    def binary(self, num, pre='0b', length=8, spacer=0):
        return '{0}{{:{1}>{2}}}'.format(pre, spacer, length).format(bin(num)[2:])


    #########################################################################################################################################    
    # Set Pin configuration as Input or Output.
    # For our example, Bank A are OUTPUTs, Bank B are INPUTs.
    # The hex at the end translates into an 8 bit binary presentation.  Each bit refers to a pin.
    # Syntax: bus.write_byte_data([device_ID], [Register to set direction for bank Bank A or B], [Direction (0 or 1)] )

    def setPinDirection(self):

        # Device A
        self.bus.write_byte_data(self.DEVICEA, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(self.DEVICEA, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        # Device B
        self.bus.write_byte_data(self.DEVICEB, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(self.DEVICEB, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        self.bus.write_byte_data(self.DEVICEC, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(self.DEVICEC, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

    

    #########################################################################################################################################    
    # Procedure to invert light state.  Fixed to light A for this test.
    # TODO: design a method to invert generically based on which light chosen, OR duplicate for each lighting circuit status.
    # CircuitID is GPIO Pin we want to change the state of.

    def room_light_circuit_A_status_INVERT(self, CircuitID):
        
        print("   -- LIGHT Status Change.")

        if not self.room_light_circuit_A_status:
            self.bus.write_byte_data(self.DEVICEA, self.setOutputStateB, 0xFF) 
            self.bus.write_byte_data(self.DEVICEB, self.setOutputStateB, 0xFF) 
            self.bus.write_byte_data(self.DEVICEC, self.setOutputStateB, 0xFF) 
            print("   -- Turn LIGHT ON (debug)")
            self.room_light_circuit_A_status = True
        
        else:
            self.bus.write_byte_data(self.DEVICEA, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(self.DEVICEB, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(self.DEVICEC, self.setOutputStateB, 0x00)
            print("   -- Turn LIGHT OFF (debug)")
            self.room_light_circuit_A_status = False





    #########################################################################################################################################    
    # setGPIOStartStat
    # The "Pre-Startup / Power failure / BMS Failure" state of controls is determined by the local relay configuration.  For the safety of the site users, power is 
    # directed to the primary room lights in the Normally Closed "NC" (normally connected or ON) state, with secondary (effect or supplementary) lighting wired to the
    # Normally Open "NO" (Normally Disconnected or OFF) state.  This configuration means building users have sufficient basic light in the event of a BMS failure.
    # However, it also means we have to determine and invert the control we send to the local relays to effect the demand.

    def setGPIOStartState(self):
        
        # Set output all 7 output bits to 0
        print("Setting all outputs.")
        self.bus.write_byte_data(self.DEVICEA, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.DEVICEB, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.DEVICEC, self.setOutputStateB, 0x00)
        print("Setting all outputs... done.")


        while True:

        time.sleep(0.5)
        print("Setting all outputs. ON")
        self.bus.write_byte_data(self.DEVICEA, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(self.DEVICEB, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(self.DEVICEC, self.setOutputStateB, 0xFF)
        print("Setting all outputs... ON done.")
        time.sleep(0.5)
        print("Setting all outputs.")
        self.bus.write_byte_data(self.DEVICEA, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.DEVICEB, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.DEVICEC, self.setOutputStateB, 0x00)
        print("Setting all outputs... done.")


    #########################################################################################################################################    
    # lookForTriggers
    def lookForTriggers(self):


        # Read state of GPIOB register
        self.MySwitch = self.bus.read_byte_data(self.DEVICEA, self.GPIOA)
    
        # This is really simply code for test.  If the state is different to the last actioned request, proceed to qualify the trigger.
        if not self.MySwitch == self.MySwitchCurrentState:


            ########################################################################
            # Software EMF Interference and Debounce filter.
            #
            # A trigger was acknowledged.  Action a software debounce to check for electrical interference or accidental trigger. We do this by:
            
            # 1. Pausing for a moment so if this trigger was found as a result of momentary spike or interference, it has time to end (so the pause it acts as a software filter)..
            time.sleep(self.debounceDelay)

            # 2. Then we read the input again to check the reading is the same as the trigger.
            self.MySwitchDebounceReadA = self.bus.read_byte_data(self.DEVICEA, self.GPIOA)
            
            # 3. We then pause again, just in case the second read was also accidental.
            time.sleep(self.debounceDelay)

            # 4. Read again to check the reading is the same as the trigger.  A deliberate and intended trigger will persist, whilst noise is likely to be inconsistent, so
            # this technique should filter unintended triggers out.
            self.MySwitchDebounceReadB = self.bus.read_byte_data(self.DEVICEA, self.GPIOA)
            
            
            # 5. We then pause again, just in case the second read was also accidental.
            time.sleep(self.debounceDelay)

            # 6. Read again to check the reading is the same as the trigger.  A deliberate and intended trigger will persist, whilst noise is likely to be inconsistent, so
            # this technique should filter unintended triggers out.
            self.MySwitchDebounceReadC = self.bus.read_byte_data(self.DEVICEA, self.GPIOA)
            
            # 5. Now we compare the 4 reads.  If the trigger identified is the same on every read, action the trigger, else it was probably electrical noise, so ignore.
            # Because the reads are done so closely together, (speed in fractions of a second) - no multiple trigger state changes could possibly occur.  Importantly, what
            # we mere mortals consider fast is an age both in computer terms and EMF interference, so it's easy to spot.
            # If there is enough interference to fool this filter - it's time to rework the electronics and interfacing!
            if self.MySwitch == self.MySwitchDebounceReadA and self.MySwitch == self.MySwitchDebounceReadB and self.MySwitch == self.MySwitchDebounceReadC:

                # If we reach here, we believe the trigger was genuine.
                print ("A new trigger was acknowledged and passed the interference filter") # Dev code

                # Update the Circuit State.
                self.changeCircuitState = True


            
            
    #########################################################################################################################################   
    # actionTrigger
    #
    # This is called if a trigger has been found. It checks to see if it was already requested and actions if not.

    def actionTrigger(self):
        
        # A trigger passed our tests and appeared genuine and was different to the current state. Increment the action tally
        self.actionTally = self.actionTally + 1
        print("Action Tally : ", self.actionTally)

        # Read the bus status and interpret as a binary string.
        self.inputBusStatus = self.binary(self.MySwitch)
        humanBus = str(self.inputBusStatus)

        # Show the trigger:
        print ("A new trigger was acknowledged.  Bus Read Status : ", self.inputBusStatus)
        
        bitCount = 0
        for i in range(9, 1, -1):
            print ("Bit ", bitCount," Bus Read Status : ", humanBus[i])
            bitCount = bitCount + 1

        # Action the request.
        self.room_light_circuit_A_status_INVERT(1)

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
        print(" .. Sending SMART MODE signal to all Local Switch Interfaces")
        #self.bus.write_byte_data(self.DEVICEB, self.setOutputStateA, 1)      #TODO - this doesn't do anything useful. Do not enable!




    #########################################################################################################################################    
    # RunProgram
    #
    # This is run after everything is setup.

    def RunProgram(self):

        # Loop until user presses CTRL-C
        while True:

            # Look for trigger (changes)
            self.lookForTriggers()

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
environmentController.setPinDirection()
environmentController.setGPIOStartState()

# Tell the local switch interfaces we're up and running.
environmentController.setBMSLive()

# Start the run program.  This is a loop.
environmentController.RunProgram()
