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
#Config.set("graphics", "resizable", 0)

# kivy imports
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.lang import Builder
from kivy.core.window import Window
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
		self.roverPosition = (100, 100)
		self.basePosition = None
		self.mapImage = self.config.get("navigation", "map_path")
		mapTopRight = (float(convert(self.config.get("navigation", "tr_lon"))),
			float(convert(self.config.get("navigation", "tr_lat"))))
		mapBottomLeft = (float(convert(self.config.get("navigation", "bl_lon"))),
			float(convert(self.config.get("navigation", "bl_lat"))))
		mapSize = (float(convert(self.config.get("navigation", "mapWidth"))),
			float(convert(self.config.get("navigation", "mapHeight"))))
		mapScale = ((mapTopRight[0] - mapBottomLeft[0]) / mapSize[0],
			(mapTopRight[1] - mapBottomLeft[1]) / mapSize[1])

		# set up application screens
		Window.size = windowSize
		self.title = "USST Rover Application"

		# build widget tree
		self.root = Builder.load_file("gui/app.kv")

		# screen manager
		self.sm = self.root.ids.sm
		self.sm.current = "splash"
		self.sm.transition = NoTransition()
		
		# video streams
		self.turretVideo = self.sm.get_screen("turret").ids.videoPlayer

		# Start our clock/threads for the GUI
		# Clock.schedule_interval(self.telemetryScreen.updateTime, 1)
		# self.telemetryScreen.ids.videoPlayer.bind(on_load = self.videoEndCallback)

		# return the root widget
		return self.root


	def refreshSettings(self):
		self.mapImage = self.config.get("navigation", "map_path")
		mapTopRight = (float(convert(self.config.get("navigation", "tr_lon"))),
			float(convert(self.config.get("navigation", "tr_lat"))))
		mapBottomLeft = (float(convert(self.config.get("navigation", "bl_lon"))),
			float(convert(self.config.get("navigation", "bl_lat"))))
		mapSize = (float(convert(self.config.get("navigation", "mapWidth"))),
			float(convert(self.config.get("navigation", "mapHeight"))))
		mapScale = ((mapTopRight[0] - mapBottomLeft[0]) / mapSize[0],
			(mapTopRight[1] - mapBottomLeft[1]) / mapSize[1])


	def display_settings(self, settings):
		self.prevScreen = self.sm.current
		sc = self.sm.get_screen("settings")
		sc.clear_widgets()
		sc.add_widget(settings)
		self.sm.current = "settings"


	def close_settings(self, *largs):
		self.changeScreen(self.prevScreen)


	def stopVideos(self):
		for name in ["arm", "drive", "turret"]:
			player = self.sm.get_screen(name).ids.videoPlayer
			player.state = "stop"
	
	def startVideo(self, name):
		player = self.sm.get_screen(name).ids.videoPlayer
		player.source = "http://c-cam.uchicago.edu/mjpg/video.mjpg"
		player.state = "play"


	# Chooses animation and changes the screen
	def changeScreen(self, name):
		if(self.sm.current_screen.name != name):
			self.sm.current = name
			self.stopVideos()
			if name == "turret" or name == "drive" or name == "arm":
				self.startVideo(name)


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
			"test_mode": False,
			"numericexample": 10,
			"drive_mode": "Two Stick",
			"stringexample": "some_string",
			"pathexample": "~"})

		config.setdefaults("navigation", {
			"follow_rover": True,
			"tr_lat": 52.139176,
			"tr_lon": -106.618917,
			"bl_lat": 52.127204,
			"bl_lon": -106.647735,
			"mapWidth": 5196,
			"mapHeight": 3605,
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

