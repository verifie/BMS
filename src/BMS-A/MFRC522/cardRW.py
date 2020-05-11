#!/usr/bin/python3
#

#########################################################################################################################################    
# cardRW.py
# 
# RFID Project
# (c) 2020 Leighton Electronics
# 
# Description :         RFID Raspberry Pi / Python 3 / RFID-RC522 - Writer.
#
# Status :              25 - Start
#
# Version History
# 2020/05/11 1443 v1.01 PME - Combine Read Write and increment an element on each scan.
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
print("|  |\  \ |  |`   |  ||  '--'  /      R e a d   /   W r i t e r .")
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
import time

# Setup default variables.
continue_reading = True
scan_count = 0
scan_delay = 1
rfid_card_data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
rfid_card_sector = 8
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] # This is the default key for authentication
data = []

# Define rfid elements.
sstandard_data = hex(254)
print("StandardData = ", sstandard_data)

standard_data = 0x00

# Read existing RFID sector data into our rfid_card_data_xx fields.
for i in range (0,16):
    rfid_card_data[i] = standard_data

print ("Standard data in rfid_card_data array (pre card read): ", rfid_card_data)


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
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        print ("\n")

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            print ("Authenticated OK, now read sector [ ", rfid_card_sector, " ]")
            rfid_card_data = MIFAREReader.MFRC522_Read(rfid_card_sector)


            # Read existing RFID sector data into our rfid_card_data_new fields.
            for i in range (0,16):
                rfid_card_data_new[i] = rfid_card_data[i]
            
            # Increment element 7 by 1
            rfid_card_data[7] = rfid_card_data[7] + 1

            # Print card data.
            for i in range(0, 16):
                print ("  - Show rfid_card_data [", i, "]:      ", rfid_card_data[i])





            print ("Sector ", rfid_card_sector, " will now be overwritten with data: [", rfid_card_data, "]")
            # Write the data
            MIFAREReader.MFRC522_Write(rfid_card_sector, rfid_card_data)
            print ("\n")


            print ("Re-reading sector [ ", rfid_card_sector, " ]")
            rfid_card_data = MIFAREReader.MFRC522_Read(rfid_card_sector)
            
            # Print card data.
            for i in range(0, 16):
                print ("  - Show rfid_card_data [", i, "]:      ", rfid_card_data[i])



            # Stop
            MIFAREReader.MFRC522_StopCrypto1()


            # Add a time delay to avoid reading the same card tens of times on each presentation.  scan_delay is configured at the start of this program.
            time.sleep (scan_delay)

            #print ("stopcrypto")
            MIFAREReader.MFRC522_StopCrypto1()

        else:
            print ("Authentication error!")

        print("\n\n")

        # Increment run time scan counter.  NOTE this becomes reset to zero on each program run time stop and restart.
        scan_count = scan_count + 1
        print ("Scan Count :", scan_count, "\n\n")
        print ("---------------------------------------------------------------------------------------------------------------\n\n")
