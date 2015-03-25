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

# threading imports
from threads.communicationThread import CommunicationThread
from threads.inputThread import InputThread
from threads.navigationThread import NavigationThread
from threads.panelThread import PanelThread
import baseMessages
from threads.unicodeConvert import convert
from Queue import Queue

# Do pre-import kivy setup
from kivy.config import Config
# get rid of weird touchscreen emulation
Config.set("input", "mouse", "mouse,disable_multitouch")
# disable window resize
# Config.set("graphics", "resizable", 0)

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


# application python code
class BaseApp(App):
	def build(self):
		# disable spamming to console
		#logging.getLogger("kivy").disabled = True
		# disable "kivy" tab in settings
		self.use_kivy_settings = False

		# navigation stuff
		self.mapImagePath = self.config.get("navigation", "map_path")
		mapTopRight = (float(convert(self.config.get("navigation", "tr_lon"))),
			float(convert(self.config.get("navigation", "tr_lat"))))
		mapBottomLeft = (float(convert(self.config.get("navigation", "bl_lon"))),
			float(convert(self.config.get("navigation", "bl_lat"))))

		# set up application window
		Window.size = windowSize
		self.title = "USST Rover Control Application"

		# build widget tree, root gets returned later
		self.root = Builder.load_file("gui/app.kv")

		# screen manager
		self.sm = self.root.ids.sm
		self.sm.current = "splash"
		self.sm.transition = NoTransition()
		
		# Configuration
		self.settings_cls = SettingsWithTabbedPanel

		# more navigation stuff
		self.mapImage = self.sm.get_screen("navigation").ids.image
		self.mapScale = ((mapTopRight[0] - mapBottomLeft[0]) / self.mapImage.width,
			(mapTopRight[1] - mapBottomLeft[1]) / self.mapImage.height)

		# Scheduled events
		# Clock.schedule_interval(self.telemetryScreen.updateTime, 1)

		return self.root


	# redefined to display app settings using screen manager
	def display_settings(self, settings):
		self.prevScreen = self.sm.current
		sc = self.sm.get_screen("settings")
		sc.clear_widgets()
		sc.add_widget(settings)
		self.sm.current = "settings"
		self.title = "Configuration"


	# closing settings returns to previously active screen
	def close_settings(self, *largs):
		self.changeScreen(self.prevScreen)


	# destroy video widget on named screen
	def stopVideo(self, name):
		screen = self.sm.get_screen(name)
		screen.video.unload()
		screen.remove_widget(screen.video)
		screen.video = None


	# create video widget on named screen
	def startVideo(self, name):
		screen = self.sm.get_screen(name)
		video = Video(source = "http://c-cam.uchicago.edu/mjpg/video.mjpg",
			state = "play")
		video.size = (0, 0)
		video.allow_stretch = True
		video.keep_ratio = True
		screen.video = video
		# add new video player
		screen.add_widget(video)
		# bring controls to front
		controls = screen.ids.controls
		screen.remove_widget(controls)
		screen.add_widget(controls)


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

	# get still camera image from given camera
	def takePicture(self, camera):
		self.commThread.mailbox.put({"picture":camera})

	# draw map smaller
	def zoomOut(self):
		map = self.sm.get_screen("navigation").ids.map
		if map.zoom >= 0.1:
			map.zoom /= 1.4


	# draw map bigger
	def zoomIn(self):
		map = self.sm.get_screen("navigation").ids.map
		if map.zoom <= 3.0:
			map.zoom *= 1.4


	# sets up threads at startup
	def on_start(self):
		self.mailbox = Queue()
		myPort = int(convert(self.config.get("communication", "myPort")))
		roverIP = convert(self.config.get("communication", "roverIP"))
		roverPort = int(convert(self.config.get("communication", "roverPort")))
		self.commThread = CommunicationThread(self, myPort, roverIP, roverPort)
		self.inputThread = InputThread(self)
		self.navThread = NavigationThread(self)
		self.panelThread = PanelThread(self)
		self.commThread.start()
		
		# Temporary until we decide on a better solution
		self.inputThread.start()
		self.inputThread.mode = self.config.get('control', 'drive_mode')
		msg = {}
		msg["dMode"] = self.inputThread.mode == ("Two Stick")
		msg["aMode"] = self.inputThread.mode == ("Arm")
		self.commThread.mailbox.put(msg)
		
		self.navThread.start()
		self.panelThread.start()


	# automatically destroys threads on exit
	def on_stop(self):
		print("stopping")
		os._exit(0)


	# loads app config file on startup
	def get_application_config(self):
		return super(BaseApp, self).get_application_config(configPath)


	# creates a new config file if none exists
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
			"roverIP": "192.168.1.103",
			"roverPort": 35001})


	# reads config JSON to populate settings tab
	def build_settings(self, settings):
		settings.add_json_panel("Control", self.config,
			data = control_json)
		settings.add_json_panel("Comms", self.config,
			data = communication_json)
		settings.add_json_panel("Navigation", self.config,
			data = navigation_json)


	# This function is called on pressing a button in config
	def on_config_change(self, config, section, key, value):
		value = convert(value) #damn unicode...
		# print(key, value)
		if(key == "drive_mode"):
			self.inputThread.mode = value
			msg = {}
			msg["dMode"] = self.inputThread.mode == ("Two Stick")
			msg["aMode"] = self.inputThread.mode == ("Arm")
			self.commThread.mailbox.put(msg)
				


# Start the application
BaseApp().run()

