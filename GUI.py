# The main program for controlling the rover from a base station. Requires Python 2.7 and pygame.

import pygame
import socket
import os
import time
import subprocess
import sys
sys.dont_write_bytecode = True # stops .pyc generation in subsequent imports
from Controller import Controller
from Button import Button
from Slider import Slider
from Box import Box
from Indicator import Indicator
from DriveClient import DriveClient
from GPSClient import GPSClient
from CameraClient import CameraClient
from ArmClient import ArmClient
from MastClient import MastClient
from ScienceClient import ScienceClient
from TextOutput import TextOutput

# global constants

IPraspi1 = "192.168.1.103"
IPraspi2 = "192.168.1.104"
IPraspi3 = "192.168.1.105"
IPraspi4 = "192.168.1.106"
# netcat-ed video on port 3001
driveClientPort = 3002
armClientPort = 3003
cameraClientPort = 3000
gpsClientPort = 3005
mastClientPort = 3004
scienceClientPort = 3006
colorWhite = (255, 255, 255)
colorGreen = (0, 240, 0)
colorLightBlue = (100, 100, 250)
colorYellow = (250, 250, 0)

# function definitions

def createButtons():
	global buttonList
	buttonList = []
	camera1Button = Button(camConnect, (1), "Front Camera", (12, 25, 100, 20), colorLightBlue, colorGreen)
	camera2Button = Button(camConnect, (2), "Arm Camera", (12, 55, 100, 20), colorLightBlue, colorGreen)
	camera3Button = Button(camConnect, (3), "Mast Camera", (12, 85, 100, 20), colorLightBlue, colorGreen)
	cameraStopButton = Button(camDisconnect, (0), "Off", (12, 115, 100, 20), colorLightBlue, colorGreen)
	cameraStopButton.selected = True
	mastButton = Button(setMastMode, None, "Mast Only", (12, 174, 100, 20), colorLightBlue, colorGreen)
	moveButton1 = Button(setDriveMode1, None, "1 Stick Drive", (12, 204, 100, 20), colorLightBlue, colorGreen)
	moveButton2 = Button(setDriveMode2, None, "2 Stick Drive", (12, 234, 100, 20), colorLightBlue, colorGreen)
	armButton = Button(setArmMode, None, "Arm", (12, 264, 100, 20), colorLightBlue, colorGreen)
	mastButton.selected = True
	stopButton = Button(stopRover, True, "Stop", (12, 324, 100, 20), colorLightBlue, colorYellow)
	pictureButton = Button(takePicture, None, "Take Picture", (12, 384, 100, 20), colorLightBlue, colorYellow)
	runExperimentButton = Button(runExperiment, None, "Science!", (12, 414, 100, 20), colorLightBlue, colorYellow)
	connectButton = Button(connectClients, None, "Connect All", (1107, 235, 100, 20), colorLightBlue, colorYellow)
	quitButton = Button(quit, None, "Quit", (12, 473, 100, 20), colorLightBlue, colorYellow)
	saveButton = Button(savePosition, None, "Save", (625, 660, 100, 30), colorLightBlue, colorYellow)
	ArmPowerOnButton = Button(ArmOn, None, "Arm Power On", (310, 585, 100, 20), colorLightBlue, colorGreen)
	ArmPowerOffButton = Button(ArmOff, None, "Arm Power Off", (310, 615, 100, 20), colorLightBlue, colorGreen)
	digButton = Button(dig, None, "Dig", (12, 354, 100, 20), colorLightBlue, colorYellow)
	buttonList.append(camera1Button)	# 0
	buttonList.append(camera2Button)	# 1
	buttonList.append(camera3Button)	# 2
	buttonList.append(saveButton)	# 3
	buttonList.append(cameraStopButton)	# 4
	buttonList.append(moveButton1)	# 5
	buttonList.append(armButton)	# 6
	buttonList.append(stopButton)	# 7
	buttonList.append(pictureButton)	# 8
	buttonList.append(runExperimentButton)	# 9
	buttonList.append(connectButton)	# 10
	buttonList.append(quitButton)	# 11
	buttonList.append(moveButton2)	# 12
	buttonList.append(mastButton)	# 13
	buttonList.append(ArmPowerOnButton)	 #14
	buttonList.append(ArmPowerOffButton)	#15
	buttonList.append(digButton)	# 16

def createSliders():
	global sliderList
	sliderList = []
	speedSlider = Slider(setSpeedScale, "Drive Power", 0.35, (150, 285, 595))
	steerSlider = Slider(setSteerScale, "Steer Rate", 0.75, (150, 285, 635))
	sliderList.append(speedSlider) #0
	sliderList.append(steerSlider) #1

def createBoxes():
	global boxList
	boxList = []
	cameraButtonBox = Box("Camera Feeds", (0, 0, 125, 145))
	controlBox = Box("Control Modes", (0, 150, 125, 143))
	actionBox = Box("Rover Actions", (0, 298, 125, 145))
	uiBox = Box("User Interface", (0, 448, 125, 53))
	connectionsBox = Box("Connections", (1095, 0, 125, 265))
	controllerBox = Box("Controller", (1095, 269, 125, 120))
	saveBox = Box("", (615, 650, 120, 50))
	settingsBox = Box("Rover Settings", (130, 544, 295, 156))
	boxList.append(cameraButtonBox)
	boxList.append(controlBox)
	boxList.append(actionBox)
	boxList.append(uiBox)
	boxList.append(uiBox)
	boxList.append(connectionsBox)
	boxList.append(controllerBox)
	boxList.append(settingsBox)
	boxList.append(saveBox)

def createIndicators():
	global indicatorList
	indicatorList = []
	camera1Indicator = Indicator(testClient, cameraRaspi1, "Front Camera", (1106, 30))
	camera2Indicator = Indicator(testClient, cameraRaspi2, "Arm Camera", (1106, 55))
	camera3Indicator = Indicator(testClient, cameraRaspi4, "Mast Camera", (1106, 80))
	mastIndicator = Indicator(testClient, mastControl, "Mast System", (1106, 105))
	driveIndicator = Indicator(testClient, driveControl, "Drive System", (1106, 155))
	armIndicator = Indicator(testClient, armControl, "Arm System", (1106, 130))
	controllerIndicator = Indicator(checkController, None, "Detected", (1114, 293))
	gpsIndicator = Indicator(testClient, gpsClient, "Nav System", (1106, 180))
	scienceIndicator = Indicator(testClient, scienceControl, "Experiment", (1106, 205))
	indicatorList.append(camera1Indicator) #0
	indicatorList.append(camera2Indicator) #1
	indicatorList.append(camera3Indicator) #2
	indicatorList.append(gpsIndicator) #3
	indicatorList.append(driveIndicator) #4
	indicatorList.append(armIndicator) #5
	indicatorList.append(controllerIndicator) #6
	indicatorList.append(mastIndicator) #7
	indicatorList.append(scienceIndicator) #8

def createConsoles(): # set up the info boxes
	global output, gpsDisplay, controllerDisplay
	output = TextOutput("Messages", 17, colorWhite, (740, 544, 350, 156), 11)
	sys.stdout = output
	controllerDisplay = TextOutput("", 17, colorWhite, (1112, 295, 88, 88), 5)
	gpsDisplay = TextOutput("Nav", 17, colorWhite, (615, 544, 120, 108), 7)

def drawButtons():
	for i in buttonList:
		i.draw(screen)

def drawSliders():
	for i in sliderList:
		i.draw(screen)

def drawBoxes():
	for i in boxList:
		i.draw(screen)

def drawIndicators():
	for i in indicatorList:
		i.refresh()
		i.draw(screen)
	for i in range(0, 3):
		if buttonList[i].selected:
			if not indicatorList[i].active:
				camDisconnect(None)
				drawButtons()

def readBaseLocation():
	global baseLocation
	try:
		locationFile = open("location.txt")
		location = locationFile.read()
		location = location.split(",")
		baseLocation = (float(location[0]), float(location[1])) # lat, lon
	except:
		pass

def setDriveMode1(fakeArg): # fakeArg needed for button activated functions
	if indicatorList[4].active:
		stopRover(False);
		buttonList[6].selected = False
		buttonList[12].selected = False
		buttonList[13].selected = False
		buttonList[5].selected = True
		drawButtons()
	
def setDriveMode2(fakeArg):
	if indicatorList[4].active:
		stopRover(False);
		buttonList[5].selected = False
		buttonList[6].selected = False
		buttonList[13].selected = False
		buttonList[12].selected = True
		drawButtons()
	
def setArmMode(fakeArg):
	if indicatorList[5].active:
		stopRover(False);
		buttonList[5].selected = False
		buttonList[12].selected = False
		buttonList[13].selected = False
		buttonList[6].selected = True
		drawButtons()
	
def setMastMode(fakeArg):
	stopRover(False)
	buttonList[5].selected = False
	buttonList[6].selected = False
	buttonList[12].selected = False
	buttonList[13].selected = True
	drawButtons()

def setSpeedScale(newValue):
	global speedScale
	speedScale = newValue

def setSteerScale(newValue):
	global steerScale
	steerScale = newValue

def checkController(fakeArg):
	return controller.isConnected

def updateGPS():
	global roverLocation, baseLocation
	if indicatorList[3].active:
		roverLocation = gpsClient.getPosition()
		if roverLocation != None:
			if int(roverLocation[0]) == 0 and int(roverLocation[1]) == 0: # no fix
				roverLocation = None
	if roverLocation != None:
		gpsDisplay.write("Lat: " + str(int(roverLocation[0])) + "* " + str(round(roverLocation[1], 3)) + "\'")
		gpsDisplay.write("Lon: " + str(int(roverLocation[2])) + "* " + str(round(roverLocation[3], 3)) + "\'")
		gpsDisplay.write("")
		gpsDisplay.write("Lat: " + str(round(roverLocation[0] + roverLocation[1] / 60.0, 5)))
		gpsDisplay.write("Lon: " + str(round(roverLocation[2] + roverLocation[3] / 60.0, 5)))
		gpsDisplay.write("Alt: " + str(int(round(roverLocation[4]))))
		gpsDisplay.write("HDOP: " + str(round(roverLocation[5], 2)))
	gpsDisplay.draw(screen)

def savePosition(fakeArg):
	if roverLocation != None:
		try:
			savefile = open("./savedPoints/" + time.strftime("%m%d%H%M%S", time.localtime()) + ".txt", "w")
			savefile.write("Saved Location Data from " + time.strftime("%m%d%H%M%S", time.localtime()) + "\n")
			savefile.write("Latitude: " + str(roverLocation[0]) + " degrees\n")
			savefile.write("Longitude: " + str(roverLocation[1]) + " degrees\n")
			savefile.write("Altitude: " + str(roverLocation[2]) + " m ASL\n")
			savefile.write("HDOP: " + str(roverLocation[3]))
			savefile.close()
			print("Position information saved.")
		except:
			print("Could not save position information.")

def takePicture(fakeArg):
	global redrawTimer
	camera = 0
	for i in range(0, 3):
		if buttonList[i].selected:
			camera = i + 1
	if camera == 0:
		return
	buttonList[8].selected = True
	drawButtons()
	screen.blit(cameraSplash, (130, 0))
	pygame.display.update()
	camDisconnect(None)
	time.sleep(0.75)
	if camera == 1:
		cameraRaspi1.takePicture()
		time.sleep(2.5)
		camConnect(1)
	elif camera == 2:
		cameraRaspi2.takePicture()
		time.sleep(2.5)
		camConnect(2)
	elif camera == 3:
		cameraRaspi4.takePicture()
		time.sleep(2.5)
		camConnect(3)
	time.sleep(0.75)
	buttonList[8].selected = False
	redrawTimer = pygame.time.get_ticks()
	drawButtons()
	pygame.display.update()
	
def dig(fakeArg):
	if indicatorList[4].active:
		print "digging..."
		driveControl.dig()
		buttonList[16].selected = True
		buttonList[16].draw(screen)
		pygame.display.update()
		time.sleep(2.0)
		print("done")
		buttonList[16].selected = False
		buttonList[16].draw(screen)

def stopRover(setSlider):	# button-based
	try:
		print "rover stopped"
		driveControl.stopMotors()
		armOff()
	except:
		pass
	if setSlider:
		sliderList[0].set(0.0)
		sliderList[0].draw(screen)

def runExperiment(fakeArg):	# button-based
	if indicatorList[8].active:
		scienceControl.runExperiment()

def testClient(client): # button-based
	return client.test()
	
def camConnect(cameraNumber): # button-based
	for cameraButton in buttonList[0:4]:
		if cameraButton.selected:
			return
	if not indicatorList[cameraNumber - 1].active:
		return
	buttonList[4].selected = False
	buttonList[cameraNumber - 1].selected = True
	drawButtons()
	screen.blit(cameraSplash, (130, 0))
	pygame.display.update()
	command = "cam.bat" # EXTERNAL FILE. Needs to be kept up to date.
	subprocess.Popen(str(command), shell=True, stdin=None, stdout=None, stderr=None)
	time.sleep(0.5)
	if(cameraNumber == 1):
		buttonList[0].selected = True
		cameraRaspi1.startCamera()
	elif(cameraNumber == 2):
		buttonList[1].selected = True
		cameraRaspi2.startCamera()
	elif(cameraNumber == 3):
		buttonList[2].selected = True
		cameraRaspi4.startCamera()
	elif(cameraNumber == 0):
		camDisconnect(1)
	redrawTimer = pygame.time.get_ticks()
	drawButtons()

def camDisconnect(fakeArg): # button-based
	if(buttonList[0].selected):
		cameraRaspi1.stopCamera()
	elif(buttonList[1].selected):
		cameraRaspi2.stopCamera()
	elif(buttonList[2].selected):
		cameraRaspi4.stopCamera()
	for cameraButton in buttonList[0:3]:
		cameraButton.selected = False
	buttonList[4].selected = True
	command = "camStop.bat" # EXTERNAL FILE. Needs to be kept up to date.
	subprocess.Popen(str(command), shell=True, stdin=None, stdout=None, stderr=None)
	drawButtons()

def connectClients(fakeArg): # button-based
	buttonList[10].selected = True
	buttonList[10].draw(screen)
	pygame.display.update()
	drawIndicators()
	pygame.display.update()
	if not indicatorList[0].active:
		cameraRaspi1.connect()
	if not indicatorList[1].active:
		cameraRaspi2.connect()
	if not indicatorList[2].active:
		cameraRaspi4.connect()
	if not indicatorList[4].active:
		driveControl.connect()
	if not indicatorList[5].active:
		armControl.connect()
	if not indicatorList[3].active:
		gpsClient.connect()
	if not indicatorList[7].active:
		mastControl.connect()
	if not indicatorList[8].active:
		scienceControl.connect()
	buttonList[10].selected = False
	drawIndicators()
	drawButtons()
	pygame.display.update()

def quit(fakeArg): # button-based
	buttonList[11].selected = True
	buttonList[11].draw(screen)
	pygame.display.update()
	camDisconnect(None)
	stopRover(False)
	ArmOff(None)
	pygame.quit()
	sys.exit(0)

def ArmOn(fakeArg):
	if indicatorList[5].active:
		for i in range(0,5):
			armControl.ConnectArmPower()
			time.sleep(0.01)
		print("Arm On")

def ArmOff(fakeArg):
	for i in range(0,5):
			armControl.DisconnectArmPower()
			time.sleep(0.01)
	print("Arm Off")
	
# program execution starts here

# create communication clients
cameraRaspi1 = CameraClient(IPraspi1, cameraClientPort)
cameraRaspi2 = CameraClient(IPraspi2, cameraClientPort)
cameraRaspi4 = CameraClient(IPraspi4, cameraClientPort)
driveControl = DriveClient(IPraspi1, driveClientPort)
gpsClient = GPSClient(IPraspi1, gpsClientPort)
armControl = ArmClient(IPraspi2, armClientPort)
mastControl = MastClient(IPraspi4, mastClientPort)
scienceControl = ScienceClient(IPraspi3, scienceClientPort)

# set up pygame resources
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20, 20)
pygame.init()
pygame.display.set_caption("USST Rover GUI")
logo = pygame.image.load('./graphics/logo.png')
pygame.display.set_icon(logo)
Clock = pygame.time.Clock()
screen = pygame.display.set_mode((1220, 700), pygame.NOFRAME)
background = pygame.image.load("./graphics/background.jpg")
cameraSplash = pygame.image.load("./graphics/camera.jpg")
screen.blit(background, (130, 0))

# initialize everything
speedScale = 0.0
steerScale = 0.0
roverLocation = None
baseLocation = None
redrawTimer = 0
controllerSendTimer = 0
gpsTimer = 0
armTimer = 0

controller = Controller(0)
createBoxes()
createButtons()
createSliders()
createIndicators()
createConsoles()
drawBoxes()
drawButtons()
drawSliders()
gpsDisplay.draw(screen)
drawIndicators()
readBaseLocation()
camConnect(0)

if not controller.isConnected:
	print("Controller is not detected.")
if baseLocation == None:
	print("Could not read base station position from 'location.txt.'")
else:
	print("Base station location read as (" + str(round(baseLocation[0], 5)) + ", " + str(round(baseLocation[1], 5)) + ").")
	
output.draw(screen)
pygame.display.update()

while True: # main execution loop

	# check scheduled tasks
	if pygame.time.get_ticks() - redrawTimer > 5000: # whole display redraw timer
		redrawTimer = pygame.time.get_ticks()
		screen.blit(background, (130, 0))
		drawBoxes()
		drawButtons()
		drawSliders()
		drawIndicators()
		if controller.isConnected:
			controllerDisplay.draw(screen)
			indicatorList[6].draw(screen)
	
	if pygame.time.get_ticks() - gpsTimer > 2010:
		gpsTimer = pygame.time.get_ticks()
		updateGPS()
		output.draw(screen) # also refresh the message displays
		if controller.isConnected:
			controllerDisplay.write("Left X: " + str(round(axes[0], 2)))
			controllerDisplay.write("Left Y: " + str(round(axes[1], 2)))
			controllerDisplay.write("Right X: " + str(round(axes[2], 2)))
			controllerDisplay.write("Right Y: " + str(round(axes[3], 2)))
			controllerDisplay.write("Trigger: " + str(round(axes[4], 2)))
			controllerDisplay.draw(screen)
			indicatorList[6].draw(screen)
	
	if pygame.time.get_ticks() - armTimer > 250: # control data send timer
		armTimer = pygame.time.get_ticks()
		if controller.isConnected:
			axes = controller.getAxes()
			buttons = controller.getButtons()
			if indicatorList[7].active: # Mast camera control
				dPad = controller.getDPad()
				mastControl.sendData(dPad[0], dPad[1])
			if buttonList[5].selected: # 1 stick drive mode
				if indicatorList[4].active: # connected
					limit = int(speedScale * 127)
					driveControl.sendOneStickData(axes[0] * speedScale * steerScale, axes[1] * speedScale, limit)
				else:
					stopRover(False)
					setMastMode(None)
			elif buttonList[12].selected: # 2 stick drive mode
				if indicatorList[4].active: # connected
					driveControl.sendTwoStickData(axes[1] * speedScale, axes[3] * speedScale)
				else:
					stopRover(False)
					setMastMode(None)
			elif buttonList[6].selected: # arm mode
				# actuators
				speed1 = int(axes[0] * 127) + 127
				speed1 = max(speed1, 0)
				speed1 = min(speed1, 254)
				speed2 = int(axes[1] * 127) + 127
				speed2 = max(speed2, 0)
				speed2 = min(speed2, 254)
				gripperControl = int(axes[4]*127) + 127
				wristPan = int(axes[2] * 40) + 127
				if buttons[0]:
					wristTilt = 127 - int(axes[3] * 45)
				else:
					wristTilt = 127 - int(axes[3] * 20)
				for i in range(0, 4):
					armControl.actuators(speed1, speed2)
					time.sleep(0.01)
					if buttons[0]:
						if buttons[2]:
							armControl.twistHand(187)
							time.sleep(0.01)
						elif buttons[1]:
							armControl.twistHand(47)
							time.sleep(0.01)
					else:
						if buttons[2]:
							armControl.twistHand(167)
							time.sleep(0.01)
						elif buttons[1]:
							armControl.twistHand(87)
							time.sleep(0.01)
					if buttons[0]:
						if buttons[4]:
							armControl.panBase(27)
							time.sleep(0.01)
						elif buttons[5]:
							armControl.panBase(227)
							time.sleep(0.01)
						else:
							armControl.panBase(127)
							time.sleep(0.01)
					else:
						if buttons[4]:
							armControl.panBase(107)
							time.sleep(0.01)
						elif buttons[5]:
							armControl.panBase(147)
							time.sleep(0.01)
						else:
							armControl.panBase(127)
							time.sleep(0.01)
					armControl.gripper(gripperControl)
					time.sleep(0.01)
					armControl.panHand(wristPan)
					time.sleep(0.01)
					armControl.tiltWrist(wristTilt)
					time.sleep(0.01)		
	
	# update UI state, check events
	mouse = pygame.mouse.get_pos()
	Clock.tick(30)	
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit(None)
		elif event.type == pygame.QUIT:
			quit(None)
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse = pygame.mouse.get_pos()
			for button in buttonList:
				if(button.obj.collidepoint(mouse)):
					button.press()
			for slider in sliderList:
				if(slider.obj.collidepoint(mouse)):
					slider.dragging = True
		if event.type == pygame.MOUSEBUTTONUP:
			for slider in sliderList:
				slider.dragging = False
	
	for slider in sliderList:
		if slider.dragging:
			slider.draw(screen)
	
	pygame.display.update()

