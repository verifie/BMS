#!/usr/bin/python3
#

#########################################################################################################################################    
# RemoteGPIO
# 
# BMS-L
# (c) 2020 Leighton Electronics
# 
# Description :         Building Management System Lighting Control Interface trials.
#
# Status :              25 - Start code interfacing tests and principle functions.
#
# Version History
# 2020/06/07 v0.00 PME - Initial creation of module and transfer of functions from the main program.


#########################################################################################################################################    
# Import External Libraries.
import smbus



#########################################################################################################################################    
# Initiate class.
class RemoteGPIO(object):

    def __init__(self):
        print ("init RemoteGPIO") # never prints


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
    # Set Pin configuration as Input or Output.
    # For our example, Bank A are OUTPUTs, Bank B are INPUTs.
    # The hex at the end translates into an 8 bit binary presentation.  Each bit refers to a pin.
    # Syntax: bus.write_byte_data([device_ID], [Register to set direction for bank Bank A or B], [Direction (0 or 1)] )

    def setPinDirection(self):


        print ("[BOOT] ... Setup IO function. \n\n")


        # Device A
        self.bus.write_byte_data(self.Device001, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(self.Device001, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        # Device B
        self.bus.write_byte_data(self.Device002, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(self.Device002, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        self.bus.write_byte_data(self.Device003, self.setPinInputOutputStateA, 0xFF)            # All set to inputs for TEST.   Hex 0xFF = (11111111)
        self.bus.write_byte_data(self.Device003, self.setPinInputOutputStateB, 0x00)            # All set to outputs for TEST.  Hex 0x00 = (00000000)

        # DEBUG - Verbose announcer.
        if self.debug_verbose:
            print ("[BOOT] ... Setup IO function. Done. \n\n")
        # DEBUG end


    #########################################################################################################################################    
    # Procedure to invert light state.  Fixed to light A for this test.
    # TODO: design a method to invert generically based on which light chosen, OR duplicate for each lighting circuit status.
    # CircuitID is GPIO Pin we want to change the state of.

    def room_light_circuit_A_status_INVERT(self, CircuitID):
        
        
        # DEBUG - Verbose announcer.
        if self.debug_verbose:
            print ("[DEBUG] ACTION : LIGHT Status Change. \n\n")
        # DEBUG endprint

        if not self.room_light_circuit_A_status:
            self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0xFF) 
            self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0xFF) 
            self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0x00) 

            # DEBUG - Verbose announcer.
            if self.debug_verbose:
                print ("[DEBUG]   -- Turn ALL LIGHTs ON")
                # DEBUG endprint

            self.room_light_circuit_A_status = True
        
        else:
            self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0xFF)

            # DEBUG - Verbose announcer.
            if self.debug_verbose:
                print ("[DEBUG]   -- Turn ALL LIGHTs OFF")
                # DEBUG endprint
                
            self.room_light_circuit_A_status = False




    #########################################################################################################################################    
    # setGPIOStartTest
    # Test.

    def setGPIOStartTest(self):
        
        # Set output all 7 output bits to 0
        print("[DEBUG] Test outputs 0.")
        self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0x00)
        print("[DEBUG]Test outputs 0... done.")

        time.sleep(1)
        # Set output all 7 output bits to 1
        print("[DEBUG] Setting all outputs.")
        self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0xFF)
        print("[DEBUG] Setting all outputs... done.")

        time.sleep(1)
        # Set output all 7 output bits to 0
        print("[DEBUG] Test outputs 0.")
        self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0x00)
        print("[DEBUG] Test outputs 0... done.")

        time.sleep(1)
        # Set output all 7 output bits to 1
        print("[DEBUG] Setting all outputs.")
        self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0xFF)
        self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0xFF)
        print("[DEBUG] Setting all outputs... done.")

        time.sleep(1)
        # Set output all 7 output bits to 0
        print("[DEBUG] Test outputs 0.")
        self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0x00)
        print("[DEBUG] Test outputs 0... done.")
        
        while False: # Debug - turn all outputs high or low.

            time.sleep(0.5)
            print("[DEBUG] Setting all outputs. ON")
            self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0xFF)
            self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0xFF)
            self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0xFF)
            print("[DEBUG] Setting all outputs... ON done.")
            time.sleep(0.5)
            print("[DEBUG] Setting all outputs.")
            self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0x00)
            self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0x00)
            print("[DEBUG] Setting all outputs... done.")




    #########################################################################################################################################    
    # setGPIOStartStat
    # The "Pre-Startup / Power failure / BMS Failure" state of controls is determined by the local relay configuration.  For the safety of the site users, power is 
    # directed to the primary room lights in the Normally Closed "NC" (normally connected or ON) state, with secondary (effect or supplementary) lighting wired to the
    # Normally Open "NO" (Normally Disconnected or OFF) state.  This configuration means building users have sufficient basic light in the event of a BMS failure.
    # However, it also means we have to determine and invert the control we send to the local relays to effect the demand.

    def setGPIOStartState(self):
        
        # Set output all 7 output bits to 0
        print("[BOOT] : Setting all outputs.")
        self.bus.write_byte_data(self.Device001, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device002, self.setOutputStateB, 0x00)
        self.bus.write_byte_data(self.Device003, self.setOutputStateB, 0x00)

        # DEBUG - Verbose announcer.
        if self.debug_verbose:
            print ("[BOOT] : Setting all outputs... done.")
        # DEBUG end
            

