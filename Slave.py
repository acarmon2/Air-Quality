#!/usr/bin/env python2
# The raspi has two connections, usb (/dev/ttyACM0) for air quality sensor and serial
# directly (/dev/ttyAMA0) with the Xbee 900
import usbiss
import opc
import time
import serial

AddressM = "\x00\x13\xA2\x00\x40\x13\xA2\x00"
Broadcast

# Port of Xbee 900
ser = serial.Serial(port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
 )

# Configuration of particle sensor
usb = usbiss.USBISS('/dev/ttyACM0', 'spi', spi_mode=2, freq=500000)
alphasense = opc.OPCN2(usb)
alphasense.on()
time.delay(1)
Data = alphasense.histogram()
# Array with the main values and the time, convert to hex
print Data['PM1']
