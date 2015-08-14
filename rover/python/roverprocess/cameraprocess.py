from roverprocess import RoverProcess

import time
import subprocess
import os
from libs.servo.ServoDriver import ServoDriver

class CameraProcess(RoverProcess):

	def setup(self, args):
		self.i2cSem = args["sem"]
		self.cameraPitch = 0
		self.cameraYaw = 0
		self.resX = 1280
		self.resY = 720
		self.framerate = 25
		try:
			self.servoDriver = ServoDriver() # throws if no I2C connection
		except:
			self.servoDriver = None
			print "CameraThread: ServoDriver not available"
	
	def loop(self):
		self.cameraPitch = min(max(self.cameraPitch, -180), 180)
		self.cameraYaw = min(max(self.cameraYaw, -180), 180)
		self.turnCamera(self.cameraPitch, self.cameraYaw)
		time.sleep(0.1)
	
	def messageTrigger(self, message):
		RoverProcess.messageTrigger(self, message)
		if "videoState" in message:
				self.setVideoSource(data["videoState"])
				
		if "CamUp" in message:
			self.cameraPitch += 5
			print "camup"
		if "CamDown" in message:
			self.cameraPitch -= 5
		if "CamLeft" in message:
			self.cameraYaw += 10
		if "CamRight" in message:
			self.cameraYaw -= 10
			
			
			
	
	def cleanup(self):
		RoverProcess.cleanup(self)
	
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

	
	def setVideoSource(self, camera):
		self.stopStreams()
		time.sleep(2)
		if camera == "startMastVideo":
			self.startTurretCam()
		elif camera == "startArmVideo":
			self.startArmCam()
		elif camera == "startDriveVideo":
			self.startDriveCam()
		elif camera == "stop":
			self.stopStreams()

	def startTurretCam(self):
		command = ('''LD_LIBRARY_PATH=/root/mjpgStreamer && /root/mjpgStreamer/./mjpg_streamer -o "output_http.so -p 40000 -w ./www" -i "input_raspicam.so -x %d -y %d -fps %d -ex night" &''') %(self.fps, self.resX, self.resY)
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	def startArmCam(self):
		command = ('''LD_LIBRARY_PATH=/root/mjpgStreamer && /root/mjpgStreamer/./mjpg_streamer -o "output_http.so -p 40000 -w ./www" -i "input_uvc.so -d /dev/video1 -r %dx%d" &''')  %(self.resX, self.resY)
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)
	
	def startDriveCam(self):
		command = ('''LD_LIBRARY_PATH=/root/mjpgStreamer && /root/mjpgStreamer/./mjpg_streamer -o "output_http.so -p 40000 -w ./www" -i "input_uvc.so -d /dev/video2 -r %dx%d -fps %d" &''')  %(self.fps, self.resX, self.resY)
		subprocess.Popen(command, env = dict(os.environ,
			LD_LIBRARY_PATH = "/root/mjpgStreamer"), shell = True)

	#Stops the streams nicely and allows them to clean up resources
	def stopStreams(self):
		command = "killall -s SIGINT mjpg_streamer"
		subprocess.Popen(command, shell = True)
		time.sleep(2)
	
	# additional functions go here

