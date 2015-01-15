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
def StartStream():
	command = '''LD_LIBRARY_PATH=/home/pi/mjpg_streamer ./mjpg_streamer/mjpg_streamer –o “output_http.so -w ./www” –i “input _raspicam.so –x 320 –y 240 –fps 16 –ex auto -quality 8” &'''
	print("Starting stream")
	print(command)
	subprocess.call(command, shell = True)
	
#Script on Pi as stopStream.py	
def StopStream():
	command = "killall -s SIGINT mjpg_streamer"
	print("Stopping stream")
	print(command)
	subprocess.call(command, shell = True)
	
	
	
	
