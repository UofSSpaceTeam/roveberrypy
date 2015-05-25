import threading
from Queue import Queue
import time
import subprocess
import os
from ServoDriver import ServoDriver

class CameraThread(threading.Thread):
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "Camera"
		self.mailbox = Queue()
		self.i2cSem = i2cSemaphore
		self.cameraPitch = 0
		self.cameraYaw = 0
		try:
			self.servoDriver = ServoDriver() # throws if no I2C connection
		except:
			self.servoDriver = None
			print "CameraThread: ServoDriver not available"

	def run(self):
		while True:
			data = self.mailbox.get()
			if "vidsource" in data:
				self.setVideoSource(data["vidsource"])
			if "takePicture" in data:
				self.takePicture()
			if "cameraMovement" in data:
				change = data["cameraMovement"]
				self.cameraPitch += int(change[0]) * -5
				self.cameraYaw += int(change[1]) * 10
				self.cameraPitch = min(max(self.cameraPitch, -180), 180)
				self.cameraYaw = min(max(self.cameraYaw, -180), 180)
				self.turnCamera(self.cameraPitch, self.cameraYaw)
	
	def turnCamera(self, pitch, yaw):
		if self.servoDriver == None:
			return
		try:
			self.i2cSem.acquire()
			p1 = int(28*pitch/3 + 1690)
			p2 = int(115*yaw/36 + 1400)
			print p1, p2
			self.servoDriver.setServo(0, p1)
			self.servoDriver.setServo(1, p2)
		except:
			print("couldn't move antenna camera.")
			raise
		self.i2cSem.release()

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
		timestamp = str(time.time() % 10000)
		command = ("raspistill -o /root/" + str(timestamp) + ".jpg -t 2 -w 1920 -h 1080 -q 100")
		self.stopStreams()
		subprocess.Popen(command, shell = True)

	def startTurretCam(self):
		command = ('''LD_LIBRARY_PATH=/root/mjpgStreamer && /root/mjpgStreamer/./mjpg_streamer -o "output_http.so -p 40000 -w ./www" -i "input_raspicam.so -x 320 -y 240 -fps 15 -ex night" &''')
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	def startArmCam(self):
		command = ("LD_LIBRARY_PATH=/root/mjpgStreamer && "
			"/root/mjpgStreamer/./mjpg_streamer -o \"output_http.so "
			"-p 40000 -w ./www\" -i \"input_uvc.so -d /dev/video1 "
			"-y -r 320x240 -f 10 -q 15\"")
		print command
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)
	
	def startDriveCam(self):
		command = ('''LD_LIBRARY_PATH=/root/mjpgStreamer && /root/mjpgStreamer/./mjpg_streamer -o "output_http.so -p 40000 -w ./www" -i "input_uvc.so -d /dev/video0" &''')
		print command
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	#Stops the streams nicely and allows them to clean up resources
	def stopStreams(self):
		command = "killall -s SIGINT mjpg_streamer"
		subprocess.Popen(command, shell = True)
		time.sleep(2)

