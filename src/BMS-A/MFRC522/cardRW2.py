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
# 2020/05/11 0734 v1.02 PME - Convert code into Object Oriented Code structure in preparation for application development.
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


#########################################################################################################################################    
# Import Libraries.

import RPi.GPIO as GPIO
import MFRC522
import signal
import time







#########################################################################################################################################    
# Program Functions:



#########################################################################################################################################    
# Setup default variables.
def setupDataVariables(self):
    self.debugModeStatus = True
    self.continue_reading = True
    self.scan_count = 0
    self.scan_delay = 1
    self.standard_data = 0x00
    self.rfid_card_data = [standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data]
    self.rfid_card_data_new = [standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data]

    self.rfid_card_sector = 8
    self.key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] # This is the default key for authentication
    self.data = []

    # Define rfid elements.
    sstandard_data = hex(254)
    print("StandardData = ", sstandard_data)
    print ("Standard data in rfid_card_data array (pre card read): ", rfid_card_data)





# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()



def prepareRfidReader():
    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()




#########################################################################################################################################    
# Function: scanForCards
# 
# Description :         Undertakes a scan for RFID cards.
#
# Dependencies:         Raspberry Pi, RFID Reader.
# Inputs :              self.rfid_card_sector
# Data Outputs:         self.rfid_card_data : card data if found.
#
# Status :              25 - Start
#
# Version History
# 2020/05/13 0659 v1.01 PME - Move code into a function.
#

def scanForCards(self):
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
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, self.key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            print ("Authenticated OK, now read sector [ ", self.rfid_card_sector, " ]")
            self.rfid_card_data = MIFAREReader.MFRC522_Read(self.rfid_card_sector)

        # Print card data.
        if self.debugModeStatus:
            print("\n\n")
            for i in range(0, 16):
                print ("  - Show rfid_card_data [", i, "]:      ", self.data[i])
            print("\n\n")

    else:
        print ("Authentication error!")






#########################################################################################################################################    
# Function:  createNewCardData
# 
# Description :         Modified existing card data with current scan credentials.  This mitigates duplicated card risk by changing some
#                       card data on every scan.  The card authentication process then checks basic user and access information alongside
#                       the modified data.  Duplicated cards may have the correct user ID and access information, but won't carry the 
#                       most recent scan information.
#
# Dependencies:         Raspberry Pi, RFID Reader.
# Inputs :              self.rfid_card_data
# Data Outputs:         self.rfid_card_data_new
#
# Status :              25 - Start
#
# Version History
# 2020/05/13 0659 v1.01 PME - Move code into a function. Initial version simply increments one element of the data for test / dev purposes.
#

def createNewCardData(self):

    # Read existing RFID sector data into our rfid_card_data_new fields.
    for i in range (0,16):
        self.rfid_card_data_new[i] = self.rfid_card_data[i]

    # Increment element 7 by 1
    self.rfid_card_data_new[7] = self.rfid_card_data[7] + 1




#########################################################################################################################################    
# Function:  writeNewCardDataToCard
# 
# Description :         Writes new data to the card
#
# Dependencies:         Raspberry Pi, RFID Reader.
# Inputs :              self.rfid_card_sector
# Data Outputs:         self.rfid_card_data : card data if found.
#
# Status :              25 - Start
#
# Version History
# 2020/05/13 0659 v1.01 PME - Move code into a function.
#

def writeNewCardDataToCard(self):
    
    # If debugMode is ON, Print data to screen.
    if self.debugModeStatus:
        print ("Sector ", self.rfid_card_sector, " will now be overwritten with data: [", self.rfid_card_data_new, "]")

    # Write the data
    MIFAREReader.MFRC522_Write(self.rfid_card_sector, self.rfid_card_data_new)
    print ("\n")



def readCardData(self):
    print ("Re-reading sector [ ", self.rfid_card_sector, " ]")
    self.rfid_card_data = MIFAREReader.MFRC522_Read(self.rfid_card_sector)



def endCardRead(self):
    # Stop
    MIFAREReader.MFRC522_StopCrypto1()



def incrementScanCounter(self):
    # Increment run time scan counter.  NOTE this becomes reset to zero on each program run time stop and restart.
    self.scan_count = self.scan_count + 1
    print ("Scan Count :", self.scan_count, "\n\n")



def timeDelay(self):
    # Add a time delay to avoid reading the same card tens of times on each presentation.  scan_delay is configured at the start of this program.
    print("Sleeping for ", self.scan_delay, "seconds.")
    time.sleep (self.scan_delay)






#########################################################################################################################################    
# RUN PROGRAM

prepareRfidReader()
setupDataVariables(self)

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    scanForCards()

    # Check if authenticated. 
    if status == MIFAREReader.MI_OK:

        createNewCardData()
        writeNewCardDataToCard()
        writeNewCardDataToCard()
        readCardData()
        endCardRead()
        incrementScanCounter()
        timeDelay(self.scan_delay)

# END OF RUN PROGRAM
#########################################################################################################################################    

