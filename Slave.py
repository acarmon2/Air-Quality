#!/usr/bin/env python2
# The raspi has two connections, usb (/dev/ttyACM0) for air quality sensor and serial
# directly (/dev/ttyAMA0) with the Xbee 900. The Libraries usbiss and opc were developed 
# by https://github.com/dhhagan, the first is to connect the SPI to USB converter and the 
# second one contains the API to cmmunicate with the particle sensor.
import usbiss
import opc
import time
import serial
import datetime
import os
import sys
from contextlib import contextmanager

Address = [0x00,0x13,0xa2,0x00,0x40,0x8b,0xaa,0xad]			# Coordinator address

########################################################################
# control the output
@contextmanager
def silence():
	new_target = open('/dev/null', 'w')
	old_target, sys.stdout = sys.stdout, new_target
	try:
		yield new_target
	finally:
		sys.stdout = old_target

# Function to arrange a frame to explicit addressing command, address for the coordinator network
# rerturn the main array
def frame(Payload):
	Frame = range(0, 100)
	# Init burst and length of packet
	Frame[0] = 0x7e
	Frame[1] = 0
	Frame[2] = 20 + len(Payload)
	# Frame identifier and ID
	Frame[3] = 0x11
	Frame[4] = 0x01
	# Coordinator address
	Frame[5:13] = Address
	# Broadcast and options
	Frame[13] = 0xff
	Frame[14] = 0xfe

	Frame[15] = 0xe8
	Frame[16] = 0xe8
	Frame[17] = 0x00
	Frame[18] = 0x11
	Frame[19] = 0xc1
	Frame[20] = 0x05
	Frame[21] = 0x00
	Frame[22] = 0x00
	# Payload
	Frame[23:(23 + len(Payload))] = Payload
	# Add checksum
	Acc = 0x00
	for k in range(3, (Frame[2]+3)):
		Acc = Acc + Frame[k]
	Frame[23 + len(Payload)] = 0xff - (Acc & 0xff)
	return Frame[0:(24 + len(Payload))]

# Function to init the Xbee in serial port and the particle sensor, if there are an error
# rerturn false
def init():
	try:
		ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout = 1)
		usb = usbiss.USBISS('/dev/ttyACM0', 'spi', spi_mode = 2, freq = 500000)
		alphasense = opc.OPCN2(usb)
		alphasense.on()
		time.sleep(10.0)
		return True
	except:
		return False


########################################################################
# main program
# You need to wait the begin of the particle sensor and the Xbee transceiver, so try
# 10 times to asure the functionality of the system
for k in range(1, 11):
	with silence():
		a = init()
	if(a):
		print "Hardware ready to work"
		break
	else:
		print "Trying to connect the devices " + str(k) + " of 10"
		time.sleep(5.0)

# In connection case get the values of particle sensor and sending by Xbee transceiver
# in the opposite case print negative case
if(a):
	with silence():
		# Create the saving file if the hardware is ready
		#Create the saving values and create news each the time change
		t0 = datetime.datetime.now()
		Name = "OPCN2_"+str(t0.year)+"_"+str(t0.month)+"_"+str(t0.day)+"_"+str(t0.hour)+"_"+str(t0.minute)+"_"+str(t0.second)+".txt"
		FileSave = open(Name, 'w')
		# Again configure the hardware (global object)
		ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout = 1)
		usb = usbiss.USBISS('/dev/ttyACM0', 'spi', spi_mode = 2, freq = 500000)
		alphasense = opc.OPCN2(usb)
		alphasense.on()
		time.sleep(10.0)
		while True:
			# Contruct the data to send. Use the frame construction and 
			# send using Xbee
			Hist = alphasense.histogram()
			Hist['Time'] = str(datetime.datetime.now())
			d0 = str(Hist['PM1']) + " "
			d1 = str(Hist['PM2.5']) + " "
			d2 = str(Hist['PM10']) + " "
			d3 = str(Hist['Time'])
			D = d0 + d1 + d2 + d3
			Dat0 = range(0, len(D))
			for k in range(0, len(D)):
				Dat0[k] = ord(D[k])
			data = frame(Dat0)
			ser.write(serial.to_bytes(data))
			ser.flushInput()
			ser.flushOutput()
			time.sleep(2.0)
			FileSave.write(str(Hist))
			FileSave.write("\n")
			FileSave.flush()
else:
	print "Failed to init the system"
