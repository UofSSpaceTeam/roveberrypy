import smbus
import time

i2c = smbus.SMBus(1)
address = 0x07

blink_list = [0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00]

for i in blink_list:
	i2c.write_byte(address, i)
	time.sleep(1)