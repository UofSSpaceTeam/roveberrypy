import threading
from Queue import Queue
import time
import subprocess
import os

class CameraThread(threading.Thread):
	def __init__(self, parent, i2cSemaphore):
		threading.Thread.__init__(self)
		self.parent = parent
		self.name = "Camera"
		self.mailbox = Queue()
		self.i2cSem = i2cSemaphore
		self.cameraPitch = 0
		self.cameraYaw = 0
		self.servoDriver = ServoDriver()

	def run(self):
		while True:
			data = self.mailbox.get()
			if "vidsource" in data:
				self.setVideoSource(data["vidsource"])
			if "takePicture" in data:
				self.takePicture()
			if "cameraMovement" in data:
				change = data["cameraMovement"]
				self.cameraPitch += int(change[1]) * 5
				self.cameraYaw += int(change[0]) * 5
				self.cameraPitch = min(max(self.cameraPitch, -45), 45)
				self.cameraYaw = min(max(self.cameraYaw, -90), 90)
				self.turnCamera(self.cameraPitch, self.cameraYaw)
	
	def turnCamera(self, pitch, yaw)
		try:
			self.i2cSem.acquire()
			servoDriver.setServo(0, int(pitch + self.center[0]))
			servoDriver.setServo(1, int(yaw + self.center[1]))
		except:
			print("couldn't move antenna camera.")
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

