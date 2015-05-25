########################################################################
#Framework for Kivy interface
#Need way to take user input to toggle between streams, stop, start, etc.
#######################################################################

import subprocess, os

#Script on Pi as testPicture.py
def TakePicture():
	command = "raspistill -o scriptPic.jpg -t 2 -w 1920 -h 1080 -q 100"
	print("Taking picture")
	print(command)
	subprocess.Popen(command, shell = True)
	
#Script on Pi as testStream.py	
def StartStreamHQ():
	command = '''LD_LIBRARY_PATH=/home/pi/mjpgStreamer && /home/pi/mjpgStreamer/./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x 320 -y 240 -fps 15 -ex night" &'''
	print("Starting HQ stream")
	subprocess.Popen(command, env=dict(os.environ, LD_LIBRARY_PATH="/home/pi/mjpg_streamer"), shell = True)
	
def StartStreamLQ():
	command = '''LD_LIBRARY_PATH=/home/pi/mjpgStreamer && /home/pi/mjpgStreamer/./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so -d /dev/video1" &'''
	print("Starting LQ stream")
	subprocess.Popen(command, env=dict(os.environ, LD_LIBRARY_PATH="/home/pi/mjpg_streamer"), shell = True)
	
#Script on Pi as stopStream.py	
def StopStream():
	command = "killall -s SIGINT mjpg_streamer"
	print("Stopping stream")
	print(command)
	subprocess.Popen(command, shell = True)
	
	
################################################

streamNumber = int(raw_input('Enter a stream to view (1= HQ Video, 2= LQ Video, 3= Picture: '))

if streamNumber == 1:
	StartStreamHQ()
	stopKey = int(raw_input('To stop the stream press 0'))
	
	if stopKey == 0: #message will not appear, but typing 0 will kill stream
			StopStream()
			
elif streamNumber == 2:
	StartStreamLQ()
	stopKey = int(raw_input('To stop the stream press 0'))
	
	if stopKey == 0: #message will not appear, but typing 0 will kill stream
			StopStream()
	
elif streamNumber == 3:
	TakePicture()
	
else:
	print "That is not a valid input"
	
	