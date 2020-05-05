#!/usr/bin/python3
#

#########################################################################################################################################    
# RFIDTrialCode.py
# 
# RFID Project
# (c) 2020 Leighton Electronics
# 
# Description :         RFID Raspberry Pi / Python 3 / RFID-RC522.
#
# Status :              25 - Start
#
# Version History
# 2020/04/25 2211 V1.00 PME - Trial Code.
# 2020/05/05 2023 v1.04 PME - Added GIT source code control.  Triggering actions from specific ID cards.
#

# FURTHER COPYRIGHT / LICENSE INFORMATION FROM MFRC522 NFC Example code.
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
#


# Import Libraries.
import RPi.GPIO as GPIO
import MFRC522
import signal
a = 0


# Setup default variables.
continue_reading = True

# Cleanly exit on ctrl-c.
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

# Welcome message
# Simple print screen introduction
print ("")
print ("=============================================================================================================================================")
print ("")
print (",------. ,------.,--.,------.   ")
print ("|  .--. '|  .---'|  ||  .-.  \  ")
print ("|  '--'.'|  `--, |  ||  |  \  : ")
print ("|  |\  \ |  |`   |  ||  '--'  /     R e a d e r . ")
print ("`--' '--'`--'    `--'`-------'  ")
print ("                                ")
print (" Copyright (c) Leighton Electronics 2020 Onwards. Patent Pending. NO UNAUTHORISED ACCESS PERMITTED. ")
print (" www.LeightonElectronics.co.uk ")
print ("")
print ("=============================================================================================================================================")
print ("")
print ("")
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")
print (" ")
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    #print ("scanning for cards")
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    #print ("is a card found?")
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Get the UID of the card
    #print ("get UID")
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        print ("Select the scanned tag")
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        print ("Authenticate")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            for i in range(0, 25):
                print ("authenticated OK, now read sector [ ", i, " ]")
                MIFAREReader.MFRC522_Read(i)
                print (" ")


            #print ("now read 11")
            #MIFAREReader.MFRC522_Read(11)

            #print ("stopcrypto")
            MIFAREReader.MFRC522_StopCrypto1()

        else:
            print ("Authentication error")

        print(" ")
        print(" ")

        
        a = a + 1
        print ("Scan:", a)
        
        print(" ")
