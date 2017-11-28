#!/usr/bin/env python2
import time
import datetime
import serial
import os
import sys
from contextlib import contextmanager

#############################################################
# Control the output in the screen
@contextmanager
def silence():
    new_target = open('NUL', 'w')
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target

# Function to init the hardware, xbee module
def init():
    try:
        ser = serial.Serial('COM11', baudrate = 9600, timeout = 3)
        return True
    except:
        return False

# Function to extract payload, the length and characteristics of the frame
def payload(frame):
    # Dictionary to save the data
    Values = {}
    # Start delimiter, check if the frame is valid
    if(ord(frame[0]) == 126):
        # Lenght of the receive frame
        L = ord(frame[2])
        # The data between 3 and 20 has the characteristics of the communications and
        # data. d0 contain the payload and split the values and generate
        d0 = frame[21:(L + 3)]
        # frame[L+3] contains the checksum values
        P0 = d0.split()
        Values['PM1'] = float(P0[0])
        Values['PM2.5'] = float(P0[1])
        Values['PM10'] = float(P0[2])
        Values['Time'] = P0[3]+str(" ")+P0[4]
    else:
        # return empty dictionary
        Values = {}
    return Values

#############################################################
# Try to connect the hardware
for k in range(1, 11):
        a = init()
        if(a):
            print "Hardware ready to work"
            break
        else:
            time.sleep(2)
            print "Trying to connect the hardware " + str(k) + " of 10"

# if hardware is ready create the file to save the data
if(a):
        t0 = datetime.datetime.now()
        Name = 'OPCN2_'+str(t0.year)+'_'+str(t0.month)+'_'+str(t0.day)+'_'+str(t0.hour)+'_'+str(t0.minute)+'_'+str(t0.second)+'.txt'
        File = open(Name, 'w')
        ser = serial.Serial('COM11', baudrate = 9600, timeout = 1)
        # Read the value of serial and save
        while True:
            if(ser.inWaiting() > 0):
                Data = ser.readline()
                D0 = payload(Data)
                if(any(D0)):
                    File.write(str(D0))
                    File.write("\n")
                    print D0
                else:
                    print "Error in communication"

