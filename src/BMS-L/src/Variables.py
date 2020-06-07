#!/usr/bin/python3
#

#########################################################################################################################################    
# Variables.py
# 
# BMS-L
# (c) 2020 Leighton Electronics
# 
# Description :         Building Management System Lighting Control Interface trials.
#
# Status :              25 - Start code interfacing tests and principle functions.
#
# Version History

# 2020/06/06 1523 v0.06 PME - Separate functions in to modules.


#########################################################################################################################################    
# Create class.


print (" [BOOT] Variables") # never prints



#########################################################################################################################################    
# Define Variables

# Debug verbose screen print
debug_verbose = True

# Switch types and settings.
print (" [BOOT] ... Setup Switch types and settings.")

# Switch Types
Latch = 0
Momentary = 1
Timer = 2
Movement = 3
on = 1
off = 2
debounceFail = 0
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
Device001Output0 = on
Device001Output1 = off
Device001Output2 = off
Device001Output3 = off
Device001Output4 = off
Device001Output5 = off
Device001Output6 = off
Device001Output7 = off

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
Device002Output0 = on
Device002Output1 = off
Device002Output2 = off
Device002Output3 = off
Device002Output4 = off
Device002Output5 = off
Device002Output6 = off
Device002Output7 = off

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
Device003Output0 = on
Device003Output1 = off
Device003Output2 = off
Device003Output3 = off
Device003Output4 = off
Device003Output5 = off
Device003Output6 = off
Device003Output7 = off

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
Device004Output0 = on
Device004Output1 = off
Device004Output2 = off
Device004Output3 = off
Device004Output4 = off
Device004Output5 = off
Device004Output6 = off
Device004Output7 = off

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
Device005Output0 = on
Device005Output1 = off
Device005Output2 = off
Device005Output3 = off
Device005Output4 = off
Device005Output5 = off
Device005Output6 = off
Device005Output7 = off

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
Device006Output0 = on
Device006Output1 = off
Device006Output2 = off
Device006Output3 = off
Device006Output4 = off
Device006Output5 = off
Device006Output6 = off
Device006Output7 = off

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
Device007Output0 = on
Device007Output1 = off
Device007Output2 = off
Device007Output3 = off
Device007Output4 = off
Device007Output5 = off
Device007Output6 = off
Device007Output7 = off

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
Device008Output0 = on
Device008Output1 = off
Device008Output2 = off
Device008Output3 = off
Device008Output4 = off
Device008Output5 = off
Device008Output6 = off
Device008Output7 = off

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
Device009Output0 = on
Device009Output1 = off
Device009Output2 = off
Device009Output3 = off
Device009Output4 = off
Device009Output5 = off
Device009Output6 = off
Device009Output7 = off

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
Device010Output0 = on
Device010Output1 = off
Device010Output2 = off
Device010Output3 = off
Device010Output4 = off
Device010Output5 = off
Device010Output6 = off
Device010Output7 = off



# DEBUG - Verbose announcer.
if debug_verbose:
    print (" [BOOT] ... Setup Switch types and settings. DONE \n")
# DEBUG end



# Software variables.
print (" [BOOT] ... Setup default variables.")

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
PrintOnce = True
debounceDelay = 0.02


# DEBUG - Verbose announcer.
if debug_verbose:
    print (" [BOOT] ... Setup default variables. DONE \n")
# DEBUG end


