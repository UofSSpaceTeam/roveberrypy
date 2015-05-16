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
			if "takePicture" in data:
				self.takePicture()

	# change / reload / deactivate a video stream
	def setVideoSource(self, camera):
		self.stopStreams()
		if camera == "turret":
			self.startTurretCam()
		elif camera == "arm":
			self.startArmCam()
		elif camera == "drive":
			self.startDriveCam()

	# todo: add gps tag
	def takePicture(self):
		print("taking picture")
		timestamp = str(time.time()) % 10000
		command = ("raspistill -o /home/root/" + timestamp + ".jpg"
			"-t 2 -w 1920 -h 1080 -q 100")
		self.stopStreams()
		subprocess.Popen(command, shell = True)

	def startTurretCam(self):
		command = ("LD_LIBRARY_PATH=/root/mjpgStreamer && "
			"/root/mjpgStreamer/./mjpg_streamer -o \"output_http.so"
			"-p 40000 -w ./www\" -i \"input_raspicam.so -x 320 -y 240"
			"-fps 15 -ex night\" &")
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	def startArmCam(self):
		command = ("LD_LIBRARY_PATH=/root/mjpgStreamer && "
			"/root/mjpgStreamer/./mjpg_streamer -o \"output_http.so"
			"-p 40000 -w ./www\" -i \"input_uvc.so -d /dev/video0\" &")
		print command
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)
	
	def startDriveCam(self):
		command = ("LD_LIBRARY_PATH=/root/mjpgStreamer && "
			"/root/mjpgStreamer/./mjpg_streamer -o \"output_http.so"
			"-p 40000 -w ./www\" -i \"input_uvc.so -d /dev/video1\" &")
		print command
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	#Stops the streams nicely and allows them to clean up resources
	def stopStreams(self):
		command = "killall -s SIGINT mjpg_streamer"
		subprocess.Popen(command, shell = True)
		time.sleep(2)

