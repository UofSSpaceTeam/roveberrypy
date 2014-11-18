import urllib
import time

while 1:
	time.sleep(10)
	f = urllib.urlopen("http://192.168.1.101/index.json")
	data = f.read()
	f.close()

	x = data.find('rssi')
	print data[x + 6: x + 14]