# gps-lib - GPS Library for Raspberry Pi

## Synopsis
***
The lib reads the data obtained from a GPS Module connected to the RX-TX pins (not the USB port) of a Raspberry Pi board. It translates the received data and offers to the client application the values of the GPS reading.

## Implemented NMEA Suffixes
***
The lib allows the use of any NMEA suffixes, but just the following NMEA suffixes were implemented partly:

- GGA
- RMC

## Installation
***
First of all, to use library, is needed to disable login via serial port and to disable boot messages on Raspbian.

It can be done through the following tutorial: <http://www.raspberrypi-spy.co.uk/2013/12/free-your-raspberry-pi-serial-port/>

## Contributors
***
If you want to contribute with the project, you can implement any of the remaining NMEA suffixes. To our client application, the implemented suffixes are sufficient, but you can add code to treat the remaining suffixes.
