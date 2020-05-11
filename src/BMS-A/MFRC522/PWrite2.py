#!/usr/bin/python3
#

#########################################################################################################################################    
# PWrite##.py
# 
# RFID Project
# (c) 2020 Leighton Electronics
# 
# Description :         RFID Raspberry Pi / Python 3 / RFID-RC522 - Writer.
#
# Status :              25 - Start
#
# Version History
# 2020/04/25 2211 V1.00 PME - Trial Code.
# 2020/05/10 2133 v1.01 PME - Modifying write to numbers so all 255 except element 3
# 2020/05/11 1443 v1.02 PME - Try to write beyong the 255 suggested limit on array elements.
#

#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.

# Simple print screen introduction
print("")
print("=============================================================================================================================================")
print("")
print(",------. ,------.,--.,------.   ")
print("|  .--. '|  .---'|  ||  .-.  \  ")
print("|  '--'.'|  `--, |  ||  |  \  : ")
print("|  |\  \ |  |`   |  ||  '--'  /      W r i t e r .")
print("`--' '--'`--'    `--'`-------'  ")
print("                                ")
print(" Copyright (c) Leighton Electronics 2020 Onwards. Patent Pending. NO UNAUTHORISED ACCESS PERMITTED. ")
print(" www.LeightonElectronics.co.uk ")
print("")
print("=============================================================================================================================================")
print("")
print("")


# Import Libraries.
import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        print ("\n")

        # Check if authenticated
        if status == MIFAREReader.MI_OK:


            # Variable for the data to write
            data = []

            # Fill the data with 0xFF
            #for x in range(0,16):
            #    data.append(0x0A)


            # PME MOD - Custom writes.
            data.append(0xFF) # Data 01
            data.append(0xFF) # Data 02
            data.append(0xFF) # Data 03
            data.append(0x2A) # Data 04
            data.append(0xFF) # Data 05
            data.append(0xFF) # Data 06
            data.append(0xFF) # Data 07
            data.append(0xFF) # Data 08
            data.append(0xFF) # Data 09
            data.append(0x0A) # Data 10
            data.append(0x0A) # Data 11
            data.append(0xFF) # Data 12
            data.append(0xFF) # Data 13
            data.append(0xFF) # Data 14
            data.append(0x1A7) # Data 15
            data.append(0xFF) # Data 16


            print ("Sector 10 looked like this:")
            # Read block 10
            MIFAREReader.MFRC522_Read(10)
            print ("\n")

            print ("Sector 10 will now be filled with data: [", data"")
            # Write the data
            MIFAREReader.MFRC522_Write(10, data)
            print ("\n")

            print ("It now looks like this:")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(10)
            print ("\n")

            #data = []
            # Fill the data with 0x00
            #for x in range(0,16):
            #    data.append(0x00)

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
        else:
            print ("Authentication error")
