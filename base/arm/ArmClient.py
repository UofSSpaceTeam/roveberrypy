import socket
import time

class ArmClient: # class for arm control
	def __init__(self, IP, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.IP = IP
		self.port = port
		self.commandPanBase = "#AB" # spin base left / right
		self.commandLiftWrist = "#AL" # translate wrist joint up/down
		self.commandMoveWrist = "#AM" # translate wrist joint in/out
		self.commandTiltWrist = "#AW" # rotate wrist joint up/down
		self.commandPanHand = "#AP" # move gripper left/right
		self.commandTwistHand = "#AH" # twist gripper cw/ccw
		self.commandGripper = "#AG" # open or close gripper
		self.commandActuators = "#AT" # controls both actuators
		self.commandArmOn = "#ARX"	#connects arm power
		self.commandArmOff = "#AKX"	#disconnects arm power
	
	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(1.0)
		try:
			self.socket.connect((self.IP, self.port))
		except:
			pass
	
	def panBase(self, speed):
		try:
			self.socket.send(self.commandPanBase + chr(speed))
		except:
			pass
	
	def liftWrist(self, speed):
		try:
			self.socket.send(self.commandLiftWrist + chr(speed))
		except:
			pass
	
	def moveWrist(self, speed):
		try:
			self.socket.send(self.commandMoveWrist + chr(speed))
		except:
			pass
	
	def tiltWrist(self, speed):
		try:
			self.socket.send(self.commandTiltWrist + chr(speed))
		except:
			pass
	
	def panHand(self, speed):
		try:
			self.socket.send(self.commandPanHand + chr(speed))
		except:
			pass
	
	def twistHand(self, speed):
		try:
			self.socket.send(self.commandTwistHand + chr(speed))
		except:
			pass
	
	def gripper(self, speed):
		try:
			self.socket.send(self.commandGripper + chr(speed))
		except:
			pass
	
	def actuators(self, actuator1, actuator2):
		try:
			self.socket.send(self.commandActuators + chr(actuator1) + chr(actuator2))
		except:
			pass
	
	def ConnectArmPower(self):
		try:
			self.socket.send(self.commandArmOn)
		except:
			pass
	
	def DisconnectArmPower(self):
		try: 
			self.socket.send(self.commandArmOff)
		except:
			pass
	
	def test(self):
		try:
			self.socket.settimeout(0.05)
			self.socket.send("TST")
			return True
		except:
			return False

