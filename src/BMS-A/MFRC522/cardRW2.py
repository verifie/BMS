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



# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()



#########################################################################################################################################    
# Create class.


class bmsa(object):


    #########################################################################################################################################    
    # Program Functions:


    #########################################################################################################################################    
    # Setup default variables.

    print (" Setup default variables.")

    debugModeStatus = True
    continue_reading = True
    access_request = False
    scan_count = 0
    scan_delay = 1
    standard_data = 0x00
    rfid_card_data = [standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data]
    rfid_card_data_new = [standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data,standard_data]

    rfid_card_sector = 8
    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF] # This is the default key for authentication
    data = []

    # Define rfid elements.
    sstandard_data = hex(254)
    print("StandardData = ", sstandard_data)
    print ("Standard data in rfid_card_data array (pre card read): ", rfid_card_data)


    print (" Setup default variables.. done!")







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

        #print (" scanForCards")

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
                        print ("  - Show rfid_card_data [", i, "]:      ", self.rfid_card_data[i])
                    print("\n\n")

                # Set a variable on function exit to trigger ongoing code.
                self.access_request = True

            else:
                print ("Authentication error!")


        #print (" scanForCards... done!")


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

        print ("\n\n createNewCardData")
        # Read existing RFID sector data into our rfid_card_data_new fields.
        for i in range (0,16):
            self.rfid_card_data_new[i] = self.rfid_card_data[i]

        # Increment element 7 by 1
        self.rfid_card_data_new[7] = self.rfid_card_data[7] + 1


        print (" createNewCardData.. done! \n\n")


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

        print ("\n\n writeNewCardDataToCard")
        
        # If debugMode is ON, Print data to screen.
        if self.debugModeStatus:
            print ("Sector ", self.rfid_card_sector, " will now be overwritten with data: [", self.rfid_card_data_new, "]")

        # Write the data
        MIFAREReader.MFRC522_Write(self.rfid_card_sector, self.rfid_card_data_new)
        print ("\n")

        print (" writeNewCardDataToCard.. done! \n\n")


    def readCardData(self):

        print ("\n\n readCardData")

        print ("Re-reading sector [ ", self.rfid_card_sector, " ]")
        self.rfid_card_data = MIFAREReader.MFRC522_Read(self.rfid_card_sector)

        print (" readCardData.. done! \n\n")


    def endCardRead(self):

        print ("\n\n endCardRead")

        # Stop
        MIFAREReader.MFRC522_StopCrypto1()

        print (" endCardRead.. done! \n\n")


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


rfid = bmsa()


# Replace rfid initialisation function with direct code here in the run program to avoid creating an object of a class in a class called by a function - which feels very messy and didnt work.
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

#rfid.setupDataVariables() # This is now just setup in the class.

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
continue_reading = True
while continue_reading:
    
    rfid.scanForCards()

    # Check if authenticated. 
    
    if rfid.access_request:

        print("  rfid.access_request True. ")


        print("  calling : rfid.createNewCardData")
        rfid.createNewCardData()

        print("  calling : writeNewCardDataToCard")
        rfid.writeNewCardDataToCard()

        print("  calling : readCardData")
        rfid.readCardData()

        print("  calling : endCardRead")
        rfid.endCardRead()

        print("  calling : incrementScanCounter")
        rfid.incrementScanCounter()

        print("  calling : timeDelay")
        rfid.timeDelay()

        
        print("  set rfid.access_request False to end the access session.")
        rfid.access_request = False
        
        print("  rfid.access_request True... done ")

# END OF RUN PROGRAM
#########################################################################################################################################    

