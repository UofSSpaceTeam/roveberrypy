import roverMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert

convert = unicodeConvert.convert

class cameraThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "cameraThread"
		self.exit = False
		self.mailbox = Queue()
		self.debug = False

	def run(self):
		while not self.exit:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				# Do something to process the data
				
	# Basic photo taking
	# ToDo: filenames, uploading to GUI
	# Possibly might want to GPS tag them for plotting on a map
	def TakePicture(self):
		command = "raspistill -o scriptPic.jpg -t 2 -w 1920 -h 1080 -q 100"
		if self.debug:
			print("Taking picture")
		subprocess.Popen(command, shell = True)
	
	
	# Starts PiCam
	# ToDo: Optimize quality, use Multiplexer
	# Probably not final location for mjpg_streamer
	def StartPiCam(self):
		command = '''LD_LIBRARY_PATH=/home/pi/mjpgStreamer && /home/pi/mjpgStreamer/./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x 320 -y 240 -fps 15 -ex night" &'''
		if self.debug:
			print("Starting PiCam stream")
		subprocess.Popen(command, env=dict(os.environ, LD_LIBRARY_PATH="/home/pi/mjpg_streamer"), shell = True)
	
	
	# Starts USB/Arm Cam
	# ToDo: Optimize quality
	def StartUSBCam(self):
		command = '''LD_LIBRARY_PATH=/home/pi/mjpgStreamer && /home/pi/mjpgStreamer/./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so" &'''
		if self.debug:
			print("Starting LQ stream")
		subprocess.Popen(command, env=dict(os.environ, LD_LIBRARY_PATH="/home/pi/mjpg_streamer"), shell = True)
	
	
	#Stops the streams nicely and allows them to clean up resources
	def StopStream(self):
		command = "killall -s SIGINT mjpg_streamer"
		if self.debug:
			print("Stopping stream")
		subprocess.Popen(command, shell = True)

	
	def stop(self):
		self.exit = True