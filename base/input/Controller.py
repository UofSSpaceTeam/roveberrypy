from pygame import joystick

class Controller:
	def __init__(self, controllerIndex): # connect to xbox controller
		self.leftJoystickXDeadzone = 0.2
		self.leftJoystickYDeadzone = 0.2
		self.rightJoystickXDeadzone = 0.2
		self.rightJoystickYDeadzone = 0.2
		self.triggerDeadzone = 0.1
		joystick.init()
		self.controller = None
		self.isConnected = False
		try:
			self.controller = joystick.Joystick(controllerIndex)
			self.controller.init()
			self.isConnected = True
		except:
			pass
	
	def getAxes(self):  # returns a tuple of all axis data (-1.0 to 1.0)
		if not self.isConnected:
			return None
		leftJoystickX = self.controller.get_axis(0)
		leftJoystickY = -self.controller.get_axis(1)
		rightJoystickX = self.controller.get_axis(4)
		rightJoystickY = -self.controller.get_axis(3)
		trigger = -self.controller.get_axis(2)
		if(leftJoystickX < self.leftJoystickXDeadzone
		and leftJoystickX > -self.leftJoystickXDeadzone):
			leftJoystickX = 0
		if(leftJoystickY < self.leftJoystickYDeadzone
		and leftJoystickY > -self.leftJoystickYDeadzone):
			leftJoystickY = 0
		if(rightJoystickX < self.rightJoystickXDeadzone
		and rightJoystickX > -self.rightJoystickXDeadzone):
			rightJoystickX = 0
		if(rightJoystickY < self.rightJoystickYDeadzone
		and rightJoystickY > -self.rightJoystickYDeadzone):
			rightJoystickY = 0
		if(trigger < self.triggerDeadzone
		and trigger > -self.triggerDeadzone):
			trigger = 0
		if leftJoystickX > 1.0:
			leftJoystickX = 1.0
		if leftJoystickX < -1.0:
			leftJoystickX = -1.0
		if leftJoystickY > 1.0:
			leftJoystickY = 1.0
		if leftJoystickY < -1.0:
			leftJoystickY = -1.0
		if rightJoystickX > 1.0:
			rightJoystickX = 1.0
		if rightJoystickY > 1.0:
			rightJoystickY = 1.0
		if rightJoystickX < -1.0:
			rightJoystickX = -1.0
		if rightJoystickY < -1.0:
			rightJoystickY = -1.0
		if trigger > 1.0:
			trigger = 1.0
		if trigger < -1.0:
			trigger = -1.0
		return (leftJoystickX, leftJoystickY, rightJoystickX, rightJoystickY, trigger)
	
	def getButtons(self):	# returns the boolean state of all buttons
		if not self.isConnected:
			return None
		buttonA = self.controller.get_button(0)
		buttonB = self.controller.get_button(1)
		buttonX = self.controller.get_button(2)
		buttonY = self.controller.get_button(3)
		buttonLB = self.controller.get_button(4)
		buttonRB = self.controller.get_button(5)
		buttonBack = self.controller.get_button(6)
		buttonStart = self.controller.get_button(7)
		buttonLeftJoystick = self.controller.get_button(8)
		buttonRightJoystick = self.controller.get_button(9)
		return (buttonA, buttonB, buttonX, buttonY, buttonLB, buttonRB, buttonBack,
		buttonStart, buttonLeftJoystick, buttonRightJoystick)
	
	def getDPad(self):	# returns the x and y states of the D Pad buttons
		if not self.isConnected:
			return None
		return self.controller.get_hat(0)	# format is (x, y): -1, 0, or 1

