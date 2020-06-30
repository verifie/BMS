#!/usr/bin/python3
#

#########################################################################################################################################    
# RemoteGPIO
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
# 2020/06/07 v0.01 PME - Initial creation of module and transfer of functions from the main program.
# 2020/06/30 v0.02 PME - Add error handling - TODO: Add manager comms in multiple network failures.


#########################################################################################################################################    
# Import External Libraries.
import smbus
import time

# Import internal Libraries
import Variables as v

#########################################################################################################################################    
# Initiate class.
class RemoteGPIO(object):

    def __init__(self):
        print ("[LIBRARY] RemoteGPIO.py")


    #########################################################################################################################################    
    # Define Variables and MCP23017 chip pin configuration:

    # Friendly names for I2C Bus registers.  It makes it easier to read the code and relates to datasheet names at:
    # http://ww1.microchip.com/downloads/en/devicedoc/20001952c.pdf
    # To use more than 8 MCP23017 chips, a multiplexer is required, allowing the same address to be used. These are the multiplexer names.

    #bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    bus = smbus.SMBus(1) # Rev 2 Pi uses 1

    # Register to access Input / Output Direction Configuration.
    setPinInputOutputStateA = 0x00 # Pin direction register A. 0 = Output.
    setPinInputOutputStateB = 0x01 # Pin direction register B. 1 = Inputs.

    # Register to Output Latches
    setOutputStateA  = 0x14 # Register for outputs A
    setOutputStateB  = 0x15 # Register for outputs B

    # Register for Input
    GPIOA  = 0x12 # Register for inputs A
    GPIOB  = 0x13 # Register for inputs B


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
    # bus.write_byte_data(v.Device003,setPinInputOutputStateA,0x80)
    #
    #                                                7 6 5 4 3 2 1 0
    # ... tells device C, sets direction for pins    1 0 0 0 0 0 0 0
    # ... the last pin is an input, the others are outputs.

    # From the datasheet: When a bit is set, the corresponding pin becomes an input. When a bit is clear, the corresponding pinbecomes an output.


    #########################################################################################################################################    
    # Set Pin configuration as Input or Output.
    # For our example, Bank A are OUTPUTs, Bank B are INPUTs.
    # The hex at the end translates into an 8 bit binary presentation.  Each bit refers to a pin.
    # Syntax: bus.write_byte_data([device_ID], [Register to set direction for bank Bank A or B], [Direction (0 or 1)] )

    def setPinDirection(self):


        print ("[BOOT]    Setup IO function.")


        # Device A
        self.bus.write_byte_data(v.Device001, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(v.Device001, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        # Device B
        self.bus.write_byte_data(v.Device002, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(v.Device002, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        self.bus.write_byte_data(v.Device003, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(v.Device003, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print ("[BOOT]    Setup IO function. Done. \n\n")
        # DEBUG end


    #########################################################################################################################################    
    # Procedure to invert light state.  Fixed to light A for this test.
    # TODO: design a method to invert generically based on which light chosen, OR duplicate for each lighting circuit status.
    # CircuitID is GPIO Pin we want to change the state of.

    def room_light_circuit_A_status_INVERT(self, CircuitID):
        
        
        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print ("[ACTION]  LIGHT Status Change.")
        # DEBUG endprint

        if not v.room_light_circuit_A_status:
            self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0xFF) 
            self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0xFF) 
            self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0x00) 

            # DEBUG - Verbose announcer.
            if v.debug_verbose:
                print ("[ACTION]  Turn ALL LIGHTs ON.")
                # DEBUG endprint

            v.room_light_circuit_A_status = True
        
        else:
            self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0xFF)

            # DEBUG - Verbose announcer.
            if v.debug_verbose:
                print ("[ACTION]  Turn ALL LIGHTs OFF.")
                # DEBUG endprint
                
            v.room_light_circuit_A_status = False



    #########################################################################################################################################    
    # Turn the selected outputs according to switch request. Takes a hex input and passes it directly on.
    # TODO we currently ignore the CircuitID and set all 3 remote outputs the same as part of the test setup early stage dev.

    def actionSwitch(self, DeviceID, OutputStateChange):
        
        
        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print ("[ACTION]  LIGHT Status Change :", OutputStateChange)
        # DEBUG endprint

        # TODO Change this to the specific device being switched.
        self.bus.write_byte_data(DeviceID, self.setOutputStateB, OutputStateChange)




    #########################################################################################################################################    
    # setGPIOStartTest
    # Test.

    def setGPIOStartTest(self):
        
        # Set output all 7 output bits to 0
        print("[DEBUG]   Test outputs 0.")
        self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0x00)
        print("[DEBUG]   Test outputs 0... done.")

        time.sleep(v.surgeDelay)
        # Set output all 7 output bits to 1
        print("[DEBUG]   Setting all outputs.")
        self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0xFF)
        print("[DEBUG]   Setting all outputs... done.")


        time.sleep(v.surgeDelay)
        # Set output all 7 output bits to 0
        print("[DEBUG]   Test outputs 0.")
        self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0x00)
        print("[DEBUG]   Test outputs 0... done.")
        
        while False: # Debug - turn all outputs high or low.


            time.sleep(v.surgeDelay)
            print("[DEBUG]   Setting all outputs. ON")
            self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0xFF)
            self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0xFF)
            self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0xFF)
            print("[DEBUG]   Setting all outputs... ON done.")

            time.sleep(v.surgeDelay)
            print("[DEBUG]   Setting all outputs.")
            self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0x00)
            print("[DEBUG]   Setting all outputs... done.")




    #########################################################################################################################################    
    # setGPIOStartStat
    # The "Pre-Startup / Power failure / BMS Failure" state of controls is determined by the local relay configuration.  For the safety of the site users, power is 
    # directed to the primary room lights in the Normally Closed "NC" (normally connected or ON) state, with secondary (effect or supplementary) lighting wired to the
    # Normally Open "NO" (Normally Disconnected or OFF) state.  This configuration means building users have sufficient basic light in the event of a BMS failure.
    # However, it also means we have to determine and invert the control we send to the local relays to effect the demand.

    def setGPIOStartState(self):
        
        # Set output all 7 output bits to 0
        print("[BOOT]    Setting all outputs.")
        self.bus.write_byte_data(v.Device001, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(v.Device002, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(v.Device003, self.setOutputStateB, 0x00)

        # DEBUG - Verbose announcer.
        if v.debug_verbose:
            print ("[BOOT]    Setting all outputs... done.")
        # DEBUG end
            



    #########################################################################################################################################    
    # lookForTriggers
    def lookForTriggers(self, selectedDevice, MySwitchCurrentState):

        # Pause in loop to allow OS Recovery and debug
        time.sleep(v.debounceDelay)

        # Sometimes, the I2C interface fails.  This can be due to interference, poor connection or other reasons.  Without error handling, the system will fail
        # which is quite undesirable.  As such, we TRY every connection to prevent failure. In the event of I2C failure, we tally the issue and return FALSE.
        # The program then returns to the loop, which will result in it trying again,  It will continue to try and fail in the event of a permanent fault.
        # TODO: We should report repetitive errors to the site manager.  But for now, we'll just repeat attempt.
        Try:

            # Read state of GPIOB register
            v.MySwitch = self.bus.read_byte_data(selectedDevice, self.GPIOA)
            # print("A input state:", v.MySwitch) # Debug print after first read.
        
            # Check if the switch states have changed.  TODO This is really simply code for test. 
            # If the state is different to the last actioned request, proceed to qualify the trigger.
            if not v.MySwitch == MySwitchCurrentState:


                ########################################################################
                # Software EMF Interference and Debounce filter.
                #
                # A trigger was acknowledged.  Action a software debounce to check for electrical interference or accidental trigger. We do this by:

                # DEBUG - Verbose announcer.
                if v.debug_verbose:
                    print ("\n\n[TRIGGER] A new trigger was acknowledged but not yet put through our interference / debounce filter") # Dev code
                # DEBUG end

                # 1. Pausing for a moment so if this trigger was found as a result of momentary spike or interference, it has time to end (so the pause it acts as a software filter)..
                time.sleep(v.debounceDelay)

                # 2. Then we read the input again to check the reading is the same as the trigger.
                v.MySwitchDebounceReadA = self.bus.read_byte_data(selectedDevice, self.GPIOA)
                
                # 3. We then pause again, just in case the second read was also accidental.
                time.sleep(v.debounceDelay)

                # 4. Read again to check the reading is the same as the trigger.  A deliberate and intended trigger will persist, whilst noise is likely to be inconsistent, so
                # this technique should filter unintended triggers out.
                v.MySwitchDebounceReadB = self.bus.read_byte_data(selectedDevice, self.GPIOA)
                
                
                # 5. We then pause again, just in case the second read was also accidental.
                time.sleep(v.debounceDelay)

                # 6. Read again to check the reading is the same as the trigger.  A deliberate and intended trigger will persist, whilst noise is likely to be inconsistent, so
                # this technique should filter unintended triggers out.
                v.MySwitchDebounceReadC = self.bus.read_byte_data(selectedDevice, self.GPIOA)
                
                # 5. Now we compare the 4 reads.  If the trigger identified is the same on every read, action the trigger, else it was probably electrical noise, so ignore.
                # Because the reads are done so closely together, (speed in fractions of a second) - no multiple trigger state changes could possibly occur.  Importantly, what
                # we mere mortals consider fast is an age both in computer terms and EMF interference, so it's easy to spot.
                # If there is enough interference to fool this filter - it's time to rework the electronics and interfacing!
                if v.MySwitch == v.MySwitchDebounceReadA and v.MySwitch == v.MySwitchDebounceReadB and v.MySwitch == v.MySwitchDebounceReadC:

                    # If we reach here, we believe the trigger was genuine.

                    # DEBUG - Verbose announcer.
                    if v.debug_verbose:
                        print ("[TRIGGER] A new trigger was acknowledged and passed the interference filter. SET changeCircuitState TRUE.") # Dev code
                    # DEBUG end

                    # Update the Circuit State.
                    v.changeCircuitState = True
                
                else:
                    # We want to keep a tally of triggers that do not pass our debounce check.  This information will help us determine if there is excess interference causing false triggers
                    v.debounceFail = v.debounceFail + 1

        except:
            v.I2CFault = v.I2CFault + 1
            print("I2C Read Error:", sys.exc_info()[0], " Comms Error:", v.I2CFault)


