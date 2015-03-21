# Main base station control application, run with Kivy.

# global setup
configPath = "%(appdir)s/gui/config.ini"
windowSize = (1024, 600)

# python imports
import sys
sys.dont_write_bytecode = True
import os
import time
import json
import time
import logging

# thread imports
from threads.communicationThread import CommunicationThread
from threads.inputThread import InputThread
from threads.navigationThread import NavigationThread
from threads.panelThread import PanelThread
import baseMessages
from threads.unicodeConvert import convert
from Queue import Queue

# Do pre-import kivy setup
from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
#Config.set("graphics", "resizable", 0)

# kivy imports
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
from gui.settingsDefinition import *

# In code references of Kv widgets

class TelemetryScreen(Screen):
	def updateTime(self, *args):
		self.ids.mission.clock_text = time.asctime()


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


class BaseApp(App):
	def build(self):
		# more settings
		#logging.getLogger("kivy").disabled = True
		self.use_kivy_settings = False
		self.settings_cls = SettingsWithTabbedPanel

		# navigation stuff
		#self.roverPosition
		#self.basePosition
		self.mapImagePath = self.config.get("navigation", "map_path")
		mapTopRight = (float(convert(self.config.get("navigation", "tr_lon"))),
			float(convert(self.config.get("navigation", "tr_lat"))))
		mapBottomLeft = (float(convert(self.config.get("navigation", "bl_lon"))),
			float(convert(self.config.get("navigation", "bl_lat"))))

		# set up application screens
		Window.size = windowSize
		self.title = "USST Rover Application"

		# build widget tree
		self.root = Builder.load_file("gui/app.kv")

		# screen manager
		self.sm = self.root.ids.sm
		self.sm.current = "splash"
		self.sm.transition = NoTransition()
		
		# more navigation stuff
		self.mapImage = self.sm.get_screen("navigation").ids.image
		self.mapScale = ((mapTopRight[0] - mapBottomLeft[0]) / self.mapImage.width,
			(mapTopRight[1] - mapBottomLeft[1]) / self.mapImage.height)

		# Start our clock/threads for the GUI
		# Clock.schedule_interval(self.telemetryScreen.updateTime, 1)
		# self.telemetryScreen.ids.videoPlayer.bind(on_load = self.videoEndCallback)

		# return the root widget
		return self.root


	def display_settings(self, settings):
		self.prevScreen = self.sm.current
		sc = self.sm.get_screen("settings")
		sc.clear_widgets()
		sc.add_widget(settings)
		self.sm.current = "settings"


	def close_settings(self, *largs):
		self.changeScreen(self.prevScreen)


	def stopVideo(self, name):
		screen = self.sm.get_screen(name)
		screen.video.unload()
		screen.remove_widget(screen.video)
		screen.video = None


	def startVideo(self, name):
		screen = self.sm.get_screen(name)
		video = Video(source = "http://c-cam.uchicago.edu/mjpg/video.mjpg",
			state = "play")
		video.size = (0, 0)
		video.allow_stretch = True
		video.keep_ratio = True
		screen.video = video
		screen.add_widget(video)


	# Chooses animation and changes the screen
	def changeScreen(self, name):
		curScreen = self.sm.current_screen.name
		if curScreen == "turret" or curScreen == "drive" or curScreen == "arm":
			self.stopVideo(curScreen)
			print "stopped" + curScreen
		if curScreen != name:
			self.sm.current = name
		if name == "turret" or name == "drive" or name == "arm":
			self.startVideo(name)


	def zoomOut(self):
		map = self.sm.get_screen("navigation").ids.map
		if map.zoom >= 0.1:
			map.zoom /= 1.4
	
	def zoomIn(self):
		map = self.sm.get_screen("navigation").ids.map
		if map.zoom <= 3.0:
			map.zoom *= 1.4

	# Calls to manage video transparency when loading and switching screens
	def videoEndCallback(self, obj):
		print "Video Callback!"


	# sets up threads at startup
	def on_start(self):
		self.mailbox = Queue()
		self.startThreads()
		

	def startThreads(self):
		myPort = int(convert(self.config.get("communication", "myPort")))
		roverIP = convert(self.config.get("communication", "roverIP"))
		roverPort = int(convert(self.config.get("communication", "roverPort")))
		commThread = CommunicationThread(self, myPort, roverIP, roverPort)
		inputThread = InputThread(self)
		navThread = NavigationThread(self)
		panelThread = PanelThread(self)
		commThread.start()
		inputThread.start()
		navThread.start()
		panelThread.start()


	def on_stop(self):
		print("stopping")
		os._exit(0)


	def get_application_config(self):
		return super(BaseApp, self).get_application_config(configPath)


	def build_config(self, config):
		config.setdefaults("control", {
			"drive_mode": "Two Stick"})

		config.setdefaults("navigation", {
			"tr_lat": 52.139176,
			"tr_lon": -106.618917,
			"bl_lat": 52.127204,
			"bl_lon": -106.647735,
			"optionsexample": "option2",
			"stringexample": "some_string",
			"map_path": "gui/resource/campusmap.jpg"})

		config.setdefaults("communication", {
			"myPort": 35000,
			"roverIP": "192.168.0.100",
			"roverPort": 35000})


	def build_settings(self, settings):
		settings.add_json_panel("Control", self.config,
			data = control_json)
		settings.add_json_panel("Comms", self.config,
			data = communication_json)
		settings.add_json_panel("Navigation", self.config,
			data = navigation_json)


	#This function is called on pressing a button in config
	def on_config_change(self, config, section, key, value):
		value = convert(value) #damn unicode...
		print(key, value)


# Start the application
BaseApp().run()

