# Air-Quality
Measure of Air Quality in Campus of Universidad EAFIT. The system use the sensor OPC-N2 of alphasense and the libraries usbiss and py-opc developed by David H. Hagan (https://github.com/dhhagan)

For the connecttion the system has a couple of Slave and Master

# Master
The receiver in this case. This part includes a XBee 900 and any PC structure, for the present case it was used a Raspberry Pi 3. The file Master.py creates a file to save the frame information received in the Serial port (Xbee tranceiver) and chechk firsteable the frame with the function payload(). The variables to save are PM2.5, PM5, PM10 and Time (correspond to sampling time to sum at the actual time of the system OS). 
For the establishment of the communication the Xbee try to connect to the system several times (It can be changed).

# Slave
Corresponds a sensor system, in this case use a raspberry pi with two main hardwares: the air quality sensor OPC-N2 (using the SPI-USB cable) and a XBee 900 transceiver. For the Xbee case previously required to initialized with XCTU in mode Coordinator (Master) and End Device (Slave), for the present case the physical address of coordinator is 0013A200 408BAAAD.
The file Slave.py read the values of air quality sensor and create a frame using the API XBee protocol to send Master system. Both hardware are connected in Raspberry Pi using USB.
