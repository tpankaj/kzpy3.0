from kzpy3.utils import *
import serial

ser = serial.Serial('/dev/tty.usbmodem1421',baudrate=115200, timeout=100)

while(True):
	l = ser.readline()
	print l