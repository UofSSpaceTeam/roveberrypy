import serial

stream = serial.Serial('COM5', 9600, timeout = 2)

startByte = '@'
escapeByte = '$'
endByte = '~'

message = "hello world"

def check(message):
	sum = 0x00
	for i in range(0,len(message)):
		sum ^= ord(message[i])
	return chr(sum)

def messageGet():
	read = False
	buffer = True
	messageBuffer = ''
	while buffer:
		if stream.inWaiting() > 0:
			byte = stream.read(1)
			if byte == startByte:
				read = True
				length = int(stream.read(2))
			elif byte == endByte:
				if (length != len(messageBuffer)):
					print "invalid length"
					messageBuffer = None
				buffer = False
			else:
				if read == True:
					messageBuffer += byte
					
	return messageBuffer
	
def messageSend(message):
	stream.write(startByte)
	stream.write(str(len(message)))
	stream.write(message)
	stream.write(endByte)
	
while 1:
	print messageGet()