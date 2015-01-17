########################################################################
#Framework for Kivy interface
#Need way to take user input to toggle between streams, stop, start, etc.
#######################################################################

import subprocess

#Script on Pi as testPicture.py
def TakePicture():
	command = "raspistill -o scriptPic.jpg -t 2 -w 1920 -h 1080 -q 100"
	print("Taking picture")
	print(command)
	subprocess.call(command, shell = True)
	
#Script on Pi as testStream.py	
def StartStreamHQ():
	command = '''LD_LIBRARY_PATH=/home/pi/mjpg_streamer ./mjpg_streamer/mjpg_streamer –o “output_http.so -w ./www” –i “input _raspicam.so –x 320 –y 240 –fps 10 –ex auto -quality 10” &'''
	print("Starting HQ stream")
	print(command)
	subprocess.call(command, shell = True)
	
def StartStreamLQ():
	command = '''LD_LIBRARY_PATH=/home/pi/mjpg_streamer ./mjpg_streamer/mjpg_streamer –o “output_http.so -w ./www” –i “input _raspicam.so –x 320 –y 240 –fps 20 –ex auto -quality 5” &'''
	print("Starting LQ stream")
	print(command)
	subprocess.call(command, shell = True)
	
#Script on Pi as stopStream.py	
def StopStream():
	command = "killall -s SIGINT mjpg_streamer"
	print("Stopping stream")
	print(command)
	subprocess.call(command, shell = True)
	
	
################################################

streamNumber = int(raw_input('Enter a stream to view (1= HQ Video, 2= LQ Video, 3= Picture: '))

if streamNumber == "1":
	StartStreamHQ()
	stopKey = int(raw_input('To stop the stream press 0'))
	
	if stopKey == 0: #message will not appear, but typing 0 will kill stream
			StopStream()
			
elif streamNumber == "2":
	StartStreamLQ()
	stopKey = int(raw_input('To stop the stream press 0'))
	
	if stopKey == 0: #message will not appear, but typing 0 will kill stream
			StopStream()
	
elif streamNumber == "3":
	TakePicture()
	
else
	Print "That is not a valid input"
	
	