import roverMessages
import threading
import json
from Queue import Queue
import time
from unicodeConvert import convert

class cameraThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "cameraThread"
		self.exit = False
		self.mailbox = Queue()
		self.debug = False
		self.activeCamera = None

	def run(self):
		while not self.exit:
			while not self.mailbox.empty():
				data = self.mailbox.get()
				if "vidsource" in data:
					self.setVideoSource(data["vidsource"])
				elif "picture" in data:
					self.takePicture(data["picture"])


	# change / reload / deactivate a video stream
	# camera can be none, drive, turret, or arm
	def setVideoSource(self, camera):
		if camera == "none" or self.activeCamera != None:
			self.stopStreams()
			time.sleep(0.5)
		if camera == "drive" or camera == "turret":
			self.startPiCam(camera)
		elif camera == "arm"
			self.startUSBCam()


	# Basic photo taking (stops video)
	# ToDo: filenames, uploading to GUI
	# Possibly might want to GPS tag them for plotting on a map
	def takePicture(self, camera):
		if self.activeCamera != None
			self.stopStreams()
			time.sleep(0.5)

		command = "raspistill -o scriptPic.jpg -t 2 -w 1920 -h 1080 -q 100"
		if self.debug:
			print("Taking picture")
		subprocess.Popen(command, shell = True)


	# Starts PiCam
	# ToDo: Optimize quality, use Multiplexer
	# Probably not final location for mjpg_streamer
	def startPiCam(self, camera):
		if camera == "drive":
			pass # set multiplexer
		elif camera == "turret":
			pass # set multiplexer
		self.activeCamera = camera

		command = ('''LD_LIBRARY_PATH=/home/pi/mjpgStreamer && '''
			'''/home/pi/mjpgStreamer/./mjpg_streamer -o "output_http.so -w ./www" '''
			'''-i "input_raspicam.so -x 320 -y 240 -fps 15 -ex night" &''')

		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/home/pi/mjpg_streamer"), shell = True)

		if self.debug:
			print("Starting PiCam stream (" + camera + ")")


	# Starts USB/Arm Cam
	# ToDo: Optimize quality
	def startUSBCam(self):
		self.activeCamera = "arm"

		command = ('''LD_LIBRARY_PATH=/home/pi/mjpgStreamer && '''
			'''/home/pi/mjpgStreamer/./mjpg_streamer -o "output_http.so -w ./www" '''
			'''-i "input_uvc.so" &''')

		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/home/pi/mjpg_streamer"), shell = True)

		if self.debug:
			print("Starting USB camera stream")

	#Stops the streams nicely and allows them to clean up resources
	def stopStreams(self):
		self.activeCamera = None
		command = "killall -s SIGINT mjpg_streamer"
		if self.debug:
			print("Stopping streams")
		subprocess.Popen(command, shell = True)


	def stop(self):
		self.exit = True

