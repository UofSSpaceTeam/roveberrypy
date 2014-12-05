import serial

comm = serial.Serial(port = 'COM4', baudrate = 9600, timeout = 5)
while 1:
	data = comm.readline(10) #argument is bytes to read if time-out doesn't occur
	print data