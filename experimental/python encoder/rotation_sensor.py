#File Name: RaspPi_Code
#Project: USST Rover 2015
#Coder(s): Ghazi Sami
#Date Written: 5/11/2015
#Description: This code is designed to obtain the output of the EMS22A Rotation Sensor
#As a Base-10 number between 0 and 1023. The output is continually updated as the rotation changes.

#Import necessary GPIO library
from Tkinter import *
import RPi.GPIO as GPIO

#Set pin numbering mode
GPIO.setmode(GPIO.BCM)

#Initialize pins:

#Set Digital Input (Pin 1 on Sensor) to GND
GPIO.setup(11, GPIO.OUT)  #Set clock pin (#2 on sensor) as an output
#Set Pin #3 to GND
GPIO.setup(7, GPIO.IN) #Set Digital Output (#4 on sensor) as an input
#Set Pin #5 to VCC
GPIO.setup(9, GPIO.OUT)  #Set chip select pin (#6 on sensor) as an output



#Set initial values for clock and chip select:
GPIO.output(11, True) 
GPIO.output(9, False) 

#Run loop
while True:
    #Chip select must be high for a min of 500ns between readings
    GPIO.output(9, True)
    GPIO.output(9, False)

    #Initialize position output to 0:
    pos = 0 ;

    #Read data from clock
    for x in range(0,9):
	#Have clock switch between high and low
	GPIO.output(11, False)
	GPIO.output(11, True)
	
	#Read data from pin
	if GPIO.input(7) == True:
	     b = 1
	else:
	     b = 0
	pos = pos + b * pow(2, 10-(x+1))

    #Run clock again for 7 iterations to allow for lag
    for x in range(0,6):
	GPIO.output(11,False)
	GPIO.output(11,True)
    print pos
