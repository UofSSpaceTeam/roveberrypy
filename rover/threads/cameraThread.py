import roverMessages
import threading
from Queue import Queue
import time
import subprocess
import os

class CameraThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.mailbox = Queue()

	def run(self):
		while True:
			data = self.mailbox.get()
			if "vidsource" in data:
				self.setVideoSource(data["vidsource"])
			if "picture" in data:
				if data["picture"] == "take"
					self.takePicture()
				else:
					
			if "stop" in data:
				self.stopStreams()

	# change / reload / deactivate a video stream
	def setVideoSource(self, camera):
		self.stopStreams()
		if camera == "drive" or camera == "turret":
			self.startPiCam(camera)
		elif camera == "arm":
			self.startUSBCam()

	# Basic photo taking (stops video)
	# Possibly might want to GPS tag them for plotting on a map
	def takePicture(self):
		print("taking picture")
		timestamp = str(time.time()) % 10000
		command = ("raspistill -o /home/root/" + timestamp + ".jpg"
			"-t 2 -w 1920 -h 1080 -q 100")
		self.stopStreams()
		subprocess.Popen(command, shell = True)

	# Starts PiCam
	# ToDo: Optimize quality, use Multiplexer
	# Probably not final location for mjpg_streamer
	def startPiCam(self, camera):
		if camera == "drive":
			pass # set multiplexer
		elif camera == "turret":
			pass # set multiplexer
		command = ("LD_LIBRARY_PATH=/root/mjpgStreamer && "
			"/root/mjpgStreamer/./mjpg_streamer -o \"output_http.so"
			"-p 40000 -w ./www\" -i \"input_raspicam.so -x 320 -y 240"
			"-fps 15 -ex night\" &")
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	# Starts USB/Arm Cam
	# ToDo: Optimize quality
	def startUSBCam(self):
		command = ("LD_LIBRARY_PATH=/root/mjpgStreamer && "
			"/root/mjpgStreamer/./mjpg_streamer -o \"output_http.so"
			"-p 40000 -w ./www\" -i \"input_uvc.so\" &")
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	#Stops the streams nicely and allows them to clean up resources
	def stopStreams(self):
		command = "killall -s SIGINT mjpg_streamer"
		subprocess.Popen(command, shell = True)
		time.sleep(2)

