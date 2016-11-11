from serial.tools import list_ports
import serial
import time
from interface import *
import msgpack
from ctypes import *

def SendPacket(payload, len):
	crc = pycrc16(payload, len)
	msg = []
	if len <= 256:
		msg.append(2)
		msg.append(len)
	else:
		msg.append(3)
		msg.append(int(len/(2**8)))
		msg.append(len&0xFF)
	msg.extend(payload)
	
	msg.append(int(crc.value/(2**8)))
	
	msg.append(crc.value&0xFF)
	msg.append(3)
	print(msg)
	b_msg = bytes(msg)
	print(b_msg)
	return b_msg



cycle = -10000
while(True):
	ports = list_ports.comports()
	for port in ports:	
		b_cycle = pyint32tobytes(cycle)
		payload = [8]
		payload.extend(b_cycle)
		
		with serial.Serial(port.device, timeout = 1) as ser:
			msg = SendPacket(payload, len(payload))
			ser.write(msg)
			ser.readline()
			#ser.write(SendPacket([4],1))
			data = ser.readline()
			print(data)