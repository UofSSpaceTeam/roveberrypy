import serial

stream = serial.Serial('COM5', 9600, timeout = 1)

def check(message):
	sum = 0x00
	for i in range(0,len(message)):
		sum ^= ord(message[i])
	return chr(sum)

def messageGet():
	startByte = '@'
	escapeByte = '$'
	endByte = '~'
	read = False
	buffer = True
	messageBuffer = ''
	while buffer == True:
		if stream.inWaiting() > 0:
			byte = stream.read(1)
			
			if byte == startByte:
				read = True
			elif byte == endByte:
				if (stream.read(1) != (check(messageBuffer))):
					messageBuffer = None
				buffer = False
			else:
				if read == True:
					messageBuffer += byte
	return messageBuffer
	
while 1:
	#print stream.read(10)
	print(messageGet())