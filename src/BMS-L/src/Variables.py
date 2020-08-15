#!/usr/bin/python3
#

#########################################################################################################################################    
# Variables.py
# LIBRARY - MEMORY
# 
# BMS-L
# (c) 2020 Leighton Electronics
# 
# Description :         Record of all variables in use.
#
# Status :              25 - Start code interfacing tests and principle functions.
#
# Version History

# 2020/06/06 1523 v0.06 PME - Separate functions in to modules.


#########################################################################################################################################    
# Create class.


print ("[BOOT]    Variables")



#########################################################################################################################################    
# Define Variables

# Debug verbose screen print
debug_verbose = True

# Switch types and settings.
print ("[BOOT]    Setup Switch types and settings.")

# Switch Types
Latch = 0
Momentary = 1
Timer = 2
Movement = 3
on = 1
off = 2
debounceFail = 0
surgeDelay = 0.25
RunProgramPause = 0
# Device and Switch / sensor

# Device 001
Network = 0
Device001 = 0x20 # I2C Device address (A0-A2)
Device001Input0 = Latch
Device001Input1 = Latch
Device001Input2 = Latch
Device001Input3 = Latch
Device001Input4 = Latch
Device001Input5 = Latch
Device001Input6 = Latch
Device001Input7 = Latch

# Default Circuit Startup State.
Device001Output0 = 0
Device001Output1 = 0
Device001Output2 = 0
Device001Output3 = 0
Device001Output4 = 0
Device001Output5 = 0
Device001Output6 = 0
Device001Output7 = 0

# Input to Output mappings
Device001Output0Inputs = [0]
Device001Output1Inputs = [1]
Device001Output2Inputs = [2]
Device001Output3Inputs = [3]
Device001Output4Inputs = [4]
Device001Output5Inputs = [5]
Device001Output6Inputs = [6]
Device001Output7Inputs = [7]

# Device Array
Device001InputArray = [Device001Output0, Device001Output1, Device001Output2, Device001Output3, Device001Output4, Device001Output5, Device001Output6, Device001Output7]
Device001OutputArray = [Device001Output0, Device001Output1, Device001Output2, Device001Output3, Device001Output4, Device001Output5, Device001Output6, Device001Output7]


# Device 002
Network = 0
Device002 = 0x21 # I2C Device address (A0-A2)
Device002Input0 = Latch
Device002Input1 = Latch
Device002Input2 = Latch
Device002Input3 = Latch
Device002Input4 = Latch
Device002Input5 = Latch
Device002Input6 = Latch
Device002Input7 = Latch

# Default Circuit Startup State.
Device002Output0 = 0
Device002Output1 = 0
Device002Output2 = 0
Device002Output3 = 0
Device002Output4 = 0
Device002Output5 = 0
Device002Output6 = 0
Device002Output7 = 0

# Input to Output mappings
Device002Output0Inputs = [0]
Device002Output1Inputs = [1]
Device002Output2Inputs = [2]
Device002Output3Inputs = [3]
Device002Output4Inputs = [4]
Device002Output5Inputs = [5]
Device002Output6Inputs = [6]
Device002Output7Inputs = [7]

# Device Array
Device002InputArray = [Device002Output0, Device002Output1, Device002Output2, Device002Output3, Device002Output4, Device002Output5, Device002Output6, Device002Output7]
Device002OutputArray = [Device002Output0, Device002Output1, Device002Output2, Device002Output3, Device002Output4, Device002Output5, Device002Output6, Device002Output7]


# Device 003
Network = 0
Device003 = 0x22 # Device address (A0-A2) Address of MCP23017 being accessed.  Address can be changed to 1 of 8 options by setting pins A0, A1 and A2.
Device003Input0 = Latch
Device003Input1 = Latch
Device003Input2 = Latch
Device003Input3 = Latch
Device003Input4 = Latch
Device003Input5 = Latch
Device003Input6 = Latch
Device003Input7 = Latch

# Default Circuit Startup State.
Device003Output0 = 0
Device003Output1 = 0
Device003Output2 = 0
Device003Output3 = 0
Device003Output4 = 0
Device003Output5 = 0
Device003Output6 = 0
Device003Output7 = 0

# Input to Output mappings
Device003Output0Inputs = [0]
Device003Output1Inputs = [1]
Device003Output2Inputs = [2]
Device003Output3Inputs = [3]
Device003Output4Inputs = [4]
Device003Output5Inputs = [5]
Device003Output6Inputs = [6]
Device003Output7Inputs = [7]

# Device Array
Device003InputArray = [Device003Output0, Device003Output1, Device003Output2, Device003Output3, Device003Output4, Device003Output5, Device003Output6, Device003Output7]
Device003OutputArray = [Device003Output0, Device003Output1, Device003Output2, Device003Output3, Device003Output4, Device003Output5, Device003Output6, Device003Output7]


# Device 004
Network = 0
Device004 = 0x23
Device004Input0 = Latch
Device004Input1 = Latch
Device004Input2 = Latch
Device004Input3 = Latch
Device004Input4 = Latch
Device004Input5 = Latch
Device004Input6 = Latch
Device004Input7 = Latch

# Default Circuit Startup State.
Device004Output0 = 0
Device004Output1 = 0
Device004Output2 = 0
Device004Output3 = 0
Device004Output4 = 0
Device004Output5 = 0
Device004Output6 = 0
Device004Output7 = 0

# Input to Output mappings
Device004Output0Inputs = [0]
Device004Output1Inputs = [1]
Device004Output2Inputs = [2]
Device004Output3Inputs = [3]
Device004Output4Inputs = [4]
Device004Output5Inputs = [5]
Device004Output6Inputs = [6]
Device004Output7Inputs = [7]

# Device Array
Device004InputArray = [Device004Output0, Device004Output1, Device004Output2, Device004Output3, Device004Output4, Device004Output5, Device004Output6, Device004Output7]
Device004OutputArray = [Device004Output0, Device004Output1, Device004Output2, Device004Output3, Device004Output4, Device004Output5, Device004Output6, Device004Output7]


# Device 005
Network = 0
Device005 = 0x24
Device005Input0 = Latch
Device005Input1 = Latch
Device005Input2 = Latch
Device005Input3 = Latch
Device005Input4 = Latch
Device005Input5 = Latch
Device005Input6 = Latch
Device005Input7 = Latch

# Default Circuit Startup State.
Device005Output0 = 0
Device005Output1 = 0
Device005Output2 = 0
Device005Output3 = 0
Device005Output4 = 0
Device005Output5 = 0
Device005Output6 = 0
Device005Output7 = 0

# Input to Output mappings
Device005Output0Inputs = [0]
Device005Output1Inputs = [1]
Device005Output2Inputs = [2]
Device005Output3Inputs = [3]
Device005Output4Inputs = [4]
Device005Output5Inputs = [5]
Device005Output6Inputs = [6]
Device005Output7Inputs = [7]

# Device Array
Device005InputArray = [Device005Output0, Device005Output1, Device005Output2, Device005Output3, Device005Output4, Device005Output5, Device005Output6, Device005Output7]
Device005OutputArray = [Device005Output0, Device005Output1, Device005Output2, Device005Output3, Device005Output4, Device005Output5, Device005Output6, Device005Output7]

# Device 006
Network = 0
Device006 = 0x25
Device006Input0 = Latch
Device006Input1 = Latch
Device006Input2 = Latch
Device006Input3 = Latch
Device006Input4 = Latch
Device006Input5 = Latch
Device006Input6 = Latch
Device006Input7 = Latch
# Default Circuit Startup State.
Device006Output0 = 0
Device006Output1 = 0
Device006Output2 = 0
Device006Output3 = 0
Device006Output4 = 0
Device006Output5 = 0
Device006Output6 = 0
Device006Output7 = 0

# Input to Output mappings
Device006Output0Inputs = [0]
Device006Output1Inputs = [1]
Device006Output2Inputs = [2]
Device006Output3Inputs = [3]
Device006Output4Inputs = [4]
Device006Output5Inputs = [5]
Device006Output6Inputs = [6]
Device006Output7Inputs = [7]

# Device Array
Device006InputArray = [Device006Output0, Device006Output1, Device006Output2, Device006Output3, Device006Output4, Device006Output5, Device006Output6, Device006Output7]
Device006OutputArray = [Device006Output0, Device006Output1, Device006Output2, Device006Output3, Device006Output4, Device006Output5, Device006Output6, Device006Output7]


# Device 007
Network = 0
Device007 = 0x26
Device007Input0 = Latch
Device007Input1 = Latch
Device007Input2 = Latch
Device007Input3 = Latch
Device007Input4 = Latch
Device007Input5 = Latch
Device007Input6 = Latch
Device007Input7 = Latch

# Default Circuit Startup State.
Device007Output0 = 0
Device007Output1 = 0
Device007Output2 = 0
Device007Output3 = 0
Device007Output4 = 0
Device007Output5 = 0
Device007Output6 = 0
Device007Output7 = 0

# Input to Output mappings
Device007Output0Inputs = [0]
Device007Output1Inputs = [1]
Device007Output2Inputs = [2]
Device007Output3Inputs = [3]
Device007Output4Inputs = [4]
Device007Output5Inputs = [5]
Device007Output6Inputs = [6]
Device007Output7Inputs = [7]

# Device Array
Device007InputArray = [Device007Output0, Device007Output1, Device007Output2, Device007Output3, Device007Output4, Device007Output5, Device007Output6, Device007Output7]
Device007OutputArray = [Device007Output0, Device007Output1, Device007Output2, Device007Output3, Device007Output4, Device007Output5, Device007Output6, Device007Output7]


# Device 008
Network = 0
Device008 = 0x27
Device008Input0 = Latch
Device008Input1 = Latch
Device008Input2 = Latch
Device008Input3 = Latch
Device008Input4 = Latch
Device008Input5 = Latch
Device008Input6 = Latch
Device008Input7 = Latch

# Default Circuit Startup State.
Device008Output0 = 0
Device008Output1 = 0
Device008Output2 = 0
Device008Output3 = 0
Device008Output4 = 0
Device008Output5 = 0
Device008Output6 = 0
Device008Output7 = 0

# Input to Output mappings
Device008Output0Inputs = [0]
Device008Output1Inputs = [1]
Device008Output2Inputs = [2]
Device008Output3Inputs = [3]
Device008Output4Inputs = [4]
Device008Output5Inputs = [5]
Device008Output6Inputs = [6]
Device008Output7Inputs = [7]

# Device Array
Device008InputArray = [Device008Output0, Device008Output1, Device008Output2, Device008Output3, Device008Output4, Device008Output5, Device008Output6, Device008Output7]
Device008OutputArray = [Device008Output0, Device008Output1, Device008Output2, Device008Output3, Device008Output4, Device008Output5, Device008Output6, Device008Output7]


# Device 009
Network = 1
Device009 = 0x20 # I2C Device address (A0-A2)
Device009Input0 = Latch
Device009Input1 = Latch
Device009Input2 = Latch
Device009Input3 = Latch
Device009Input4 = Latch
Device009Input5 = Latch
Device009Input6 = Latch
Device009Input7 = Latch

# Default Circuit Startup State.
Device009Output0 = 0
Device009Output1 = 0
Device009Output2 = 0
Device009Output3 = 0
Device009Output4 = 0
Device009Output5 = 0
Device009Output6 = 0
Device009Output7 = 0

# Input to Output mappings
Device009Output0Inputs = [0]
Device009Output1Inputs = [1]
Device009Output2Inputs = [2]
Device009Output3Inputs = [3]
Device009Output4Inputs = [4]
Device009Output5Inputs = [5]
Device009Output6Inputs = [6]
Device009Output7Inputs = [7]

# Device Array
Device009InputArray = [Device009Output0, Device009Output1, Device009Output2, Device009Output3, Device009Output4, Device009Output5, Device009Output6, Device009Output7]
Device009OutputArray = [Device009Output0, Device009Output1, Device009Output2, Device009Output3, Device009Output4, Device009Output5, Device009Output6, Device009Output7]


# Device 010
Network = 1
Device010 = 0x21 # I2C Device address (A0-A2)
Device010Input0 = Latch
Device010Input1 = Latch
Device010Input2 = Latch
Device010Input3 = Latch
Device010Input4 = Latch
Device010Input5 = Latch
Device010Input6 = Latch
Device010Input7 = Latch

# Default Circuit Startup State.
Device010Output0 = 0
Device010Output1 = 0
Device010Output2 = 0
Device010Output3 = 0
Device010Output4 = 0
Device010Output5 = 0
Device010Output6 = 0
Device010Output7 = 0

# Input to Output mappings
Device010Output0Inputs = [0]
Device010Output1Inputs = [1]
Device010Output2Inputs = [2]
Device010Output3Inputs = [3]
Device010Output4Inputs = [4]
Device010Output5Inputs = [5]
Device010Output6Inputs = [6]
Device010Output7Inputs = [7]

# Device Array
Device010InputArray = [Device010Output0, Device010Output1, Device010Output2, Device010Output3, Device010Output4, Device010Output5, Device010Output6, Device010Output7]
Device010OutputArray = [Device010Output0, Device010Output1, Device010Output2, Device010Output3, Device010Output4, Device010Output5, Device010Output6, Device010Output7]


# Device ID Array
DeviceIdArray = [Device001, Device002, Device003, Device004, Device005, Device006, Device007, Device008, Device009, Device010]
if debug_verbose:
    print ("[DeviceIdArray]    Device IDs: [", DeviceIdArray, "] \n")
# DEBUG end


# DEBUG - Verbose announcer.
if debug_verbose:
    print ("[BOOT]    Setup Switch types and settings. DONE \n")
# DEBUG end



# Software variables.
print ("[BOOT]    Setup default variables.")

deviceTally = 3
changeCircuitState = False
MySwitchCurrentState = 0
MySwitch = 0
inputBusStatus = 0x00

room_light_circuit_A = 0x00
room_light_circuit_A_status = False

room_light_circuit_B = 0x01
room_light_circuit_B_status = False

room_light_circuit_C = 0x02
room_light_circuit_A_status = False

toggler = 0
actionTally = 0
I2CFault = 0
PrintOnce = True
debounceDelay = 0.02


# DEBUG - Verbose announcer.
if debug_verbose:
    print ("[BOOT]    Setup default variables. DONE \n")
# DEBUG end


