import serial

comm = serial.Serial(port = 'COM3', baudrate = 9600, timeout = 5)
data = comm.read(100) #argument is bytes to read if time-out doesn't occur
print data