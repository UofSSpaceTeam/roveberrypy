# Main base station control application, run with Kivy.

# python imports
import sys
sys.dont_write_bytecode = True
import os
import time
import json
import logging

# threading imports
from threads.communicationThread import CommunicationThread
from threads.inputThread import InputThread
from threads.navigationThread import NavigationThread
from threads.panelThread import PanelThread
import baseMessages
from threads.unicodeConvert import convert
from Queue import Queue

# kivy imports
# get rid of weird touchscreen emulation
from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

# application python code
class BaseApp(App):	
	def build(self):		
		# read startup settings from file
		global settings
		settings = json.loads(open("settings.json").read())
		self.settings = settings # just an alias
		
		# set up threads
		self.mailbox = Queue()
		self.commThread = CommunicationThread(self, settings["roverIP"],
			settings["towerIP"], settings["port"])
		self.inputThread = InputThread(self)
		self.navThread = NavigationThread(self)
		self.panelThread = PanelThread(self)
		
		# build widget tree, root gets returned later
		self.root = Builder.load_file("gui/app.kv")
		
		# screen manager
		self.sm = self.root.ids.sm
		self.sm.current = "splash"
		self.sm.transition = NoTransition()
		
		# start threads
		self.commThread.start()
		self.inputThread.start()
		self.navThread.start()
		self.panelThread.start()
		
		# set up application window
		Window.size = settings["windowSize"]
		self.title = "USST Rover Control Application"
		Window.bind(on_resize=self.windowResized)
		
		# set up map
		self.map = None
		self.markers = None
		self.roverPosition = None
		self.setupMap()
		
		# Scheduled events
		Clock.schedule_interval(self.checkMail, 0.5)
		
		return self.root		
	
	# read messages in the inbox
	def checkMail(self, *args):
		while not self.mailbox.empty():
			data = self.mailbox.get()
			if "updateMap" in data:
				self.updateMap()
	
	def on_stop(self):
		os._exit(0)
	
	# Changes or refreshes the screen (tab)
	def changeScreen(self, name):
		curScreen = self.sm.current_screen.name
		if curScreen == "turret" or curScreen == "drive" or curScreen == "arm":
			self.stopVideo(curScreen)
		if curScreen != name:
			self.sm.current = name
		if name == "turret" or name == "drive" or name == "arm":
			self.startVideo(name)
		if name == "splash":
			self.title = "USST Rover Control Application"
		if name == "settings":
			self.title = "Settings"
		elif name == "telemetry":
			self.title = "Telemetry"
		elif name == "turret":
			self.title = "Turret Camera"
		elif name == "drive":
			self.title = "Drive Camera"
		elif name == "arm":
			self.title = "Arm Camera"
		elif name == "navigation":
			self.title = "Navigation"
		elif name == "image":
			self.title = "Image Analysis"
	
	# create video widget on named screen
	def startVideo(self, name):
		# Begin the camera feed
		self.commThread.mailbox.put({"vidsource":name})
		screen = self.sm.get_screen(name)
		video = Video()
		video.id = "stream"
		video.size = (0, 0)
		video.allow_stretch = True
		video.keep_ratio = True
		# Need asynchronous loading so the pi can keep up
		Clock.schedule_once(lambda dt: self.startStreamDelay(name), 2)
		screen.video = video
		# add new video player
		screen.add_widget(video)
		# bring controls to front
		controls = screen.ids.controls
		screen.remove_widget(controls)
		screen.add_widget(controls)	
	
	# destroy video widget on named screen
	def stopVideo(self, name):
		screen = self.sm.get_screen(name)
		screen.video.unload()
		screen.remove_widget(screen.video)
		screen.video = None
		
	def startStreamDelay(self, name):
		screen = self.sm.get_screen(name)
		# Right now this crashes if we spam the video buttons?
		if screen.video is not None:
			screen.video.source = "http://192.168.1.103:40000/?action=stream"
			screen.video.state = "play"

	# get still camera image from given camera
	def takePicture(self, camera):
		self.commThread.mailbox.put({"picture":camera})

	# informs other threads that the window size has changed
	def windowResized(self, window, width, height):
		self.navThread.mailbox.put({"resize":(width - 60, height - 50)})
	
	def setupMap(self):
		self.map = self.sm.get_screen("navigation").ids.map
		self.map.size = (Window.size[0] - 60, Window.size[1] - 50)
		self.map.pos = (30, 0)
		self.navThread.mailbox.put({"imageSize":self.map.texture.size})
	
	# navigation thread informs us a new map is ready
	def updateMap(self):
		self.map.size = self.navThread.renderSize
		self.map.pos[0] = self.navThread.renderPos[0] + 30
		self.map.pos[1] = self.navThread.renderPos[1]
# End of BaseApp class

# In code references of Kv widgets

class TelemetryScreen(Screen):
	def updateTime(self, *args):
		pass
		#self.ids.mission.clock_text = time.asctime()

class NavigationScreen(Screen):
	pass

class TurretScreen(Screen):
	pass

class DriveScreen(Screen):
	pass

class ArmScreen(Screen):
	pass

class ImageScreen(Screen):
	pass

class SettingsScreen(Screen):
	pass

class SplashScreen(Screen):
	pass

# Start the application
BaseApp().run()

