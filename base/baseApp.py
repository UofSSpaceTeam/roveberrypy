import sys
sys.dont_write_bytecode = True
import os
import time
import math
import json
from Queue import Queue

from threads.communicationThread import CommunicationThread
from threads.inputThread import InputThread
from threads.navigationThread import *
from threads.teleThread import *

from kivy.config import Config
Config.set("input", "mouse", "mouse,disable_multitouch")
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.graphics import *
from kivy.clock import Clock

from gui.teleWidget import TelemetryWidget

# application python code
class BaseApp(App):	
	def build(self):
		self.settings = json.loads(open("settings.json").read())
		self.mailbox = Queue()
		
		self.commThread = CommunicationThread(self, self.settings["roverIP"],
			self.settings["towerIP"], self.settings["port"])
		self.inputThread = InputThread(self)
		self.navThread = NavigationThread(self)
		self.teleThread = TeleThread(self)
		
		
		Builder.load_file("gui/telemetry.kv")
		Builder.load_file("gui/settings.kv")
		Builder.load_file("gui/nav.kv")
		Builder.load_file("gui/cameras.kv")
		self.root = Builder.load_file("gui/app.kv")
		self.sm = self.root.ids.sm
		self.sm.current = "splash"
		self.sm.transition = NoTransition()
		
		self.commThread.start()
		self.inputThread.start()
		self.navThread.start()
		self.teleThread.start()
		
		Window.size = self.settings["windowSize"]
		self.title = "USST Rover Control Application"
		Window.bind(on_resize=self.windowResized)
		self.activeForm = None
		self.drillUI = None
		self.setupMap()
		self.commThread.mailbox.put({"towerAim":0})
		Clock.schedule_interval(self.checkMail, 0.2)
		return self.root
	
	# read messages in the inbox
	def checkMail(self, *args):
		while not self.mailbox.empty():
			data = self.mailbox.get()
			if "updateMap" in data:
				self.updateMap()
				
	def on_stop(self):
		os._exit(0)
	
	def createForm(self, operation):
		if self.activeForm is not None:
			return
		if operation == "newMarker":
			if self.navThread.printMode == "Dd":
				self.activeForm = NewMarkerFormDd()
			elif self.navThread.printMode == "DMm":
				self.activeForm = NewMarkerFormDMm()
			else: # DMS
				self.activeForm = NewMarkerFormDMS()
			self.sm.current_screen.add_widget(self.activeForm)
		elif operation == "chooseMarker":
			self.activeForm = ChooseMarkerForm()
			for mk in self.navThread.markers:
				btn = Button(text=mk.name)
				btn.bind(on_release=lambda btn:
					self.submitForm(btn.text))
				self.activeForm.ids.list.add_widget(btn)
			self.sm.current_screen.add_widget(self.activeForm)
		elif operation == "removeMarker":
			self.activeForm = RemoveMarkerForm()
			for mk in self.navThread.markers:
				btn = Button(text=mk.name)
				btn.bind(on_release=lambda btn:
					self.submitForm(btn.text))
				self.activeForm.ids.list.add_widget(btn)
			self.sm.current_screen.add_widget(self.activeForm)
		elif operation == "loadMarkers":
			self.activeForm = LoadMarkersForm()
			self.sm.current_screen.add_widget(self.activeForm)
		elif operation == "saveMarkers":
			self.activeForm = SaveMarkersForm()
			self.sm.current_screen.add_widget(self.activeForm)
	
	def submitForm(self, result):
		if self.activeForm is None:
			return
		if result is None:
			pass
		elif isinstance(self.activeForm, NewMarkerForm):
			self.navThread.mailbox.put({"newMarker":result})
		elif isinstance(self.activeForm, ChooseMarkerForm):
			self.navThread.mailbox.put({"chooseMarker":result})
		elif isinstance(self.activeForm, RemoveMarkerForm):
			self.navThread.mailbox.put({"removeMarker":result})
		elif isinstance(self.activeForm, LoadMarkersForm):
			self.navThread.mailbox.put({"loadMarkers":result})
		elif isinstance(self.activeForm, SaveMarkersForm):
			self.navThread.mailbox.put({"saveMarkers":result})
		self.sm.current_screen.remove_widget(self.activeForm)
		self.activeForm = None
		
	
	# Changes or refreshes the screen (tab)
	def changeScreen(self, name):
		if self.activeForm is not None:
			return
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
		Clock.schedule_once(lambda dt: self.startStreamDelay(name), 1)
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

	# informs other threads that the window size has changed
	def windowResized(self, window, width, height):
		self.navThread.mailbox.put({"resize":(width - 60, height - 80)})
	
	def setupMap(self):
		self.navScreen = self.sm.get_screen("navigation")
		self.map = self.navScreen.ids.map
		self.map.size = (Window.size[0] - 60, Window.size[1] - 80)
		self.map.pos = (60, 0)
		self.navThread.mailbox.put({"imageSize":self.map.texture.size})
		Clock.schedule_once(self.updateMap, 1)
	
	# navigation thread informs us a new map is ready
	def updateMap(self, *args):
		self.map.size = self.navThread.mapRenderSize
		self.map.pos[0] = self.navThread.mapRenderPos[0] + 60
		self.map.pos[1] = self.navThread.mapRenderPos[1]
		self.navScreen.roverStatusText = self.navThread.roverStatusText
		self.navScreen.destStatusText = self.navThread.destStatusText
		self.navScreen.printMode = self.navThread.printMode
		self.navScreen.numMarkers = "Num: " + str(len(self.navThread.markers))
		self.map.canvas.after.clear()
		rpos = self.navThread.roverRenderPos
		tpos = self.navThread.towerRenderPos
		base = True
		with self.map.canvas.after:
		# draw markers
			for mk in self.navThread.markers:
				Color(0, 0, 0)
				mpos = mk.renderPos
				Rectangle(pos=(mpos[0] + 54, mpos[1] - 4), size=(10, 10))
				if mk.selected:
					base = False
					self.navScreen.destColor = [0.4, 1, 0.4, 1]
					Color(0, 1, 0)
					Line(points=(rpos[0] + 59, rpos[1] + 1, mpos[0] + 54,
						mpos[1] - 4))
				else:
					Color(1, 1, 0)
				Rectangle(pos=(mpos[0] + 55, mpos[1] - 3), size=(8, 8))
			# draw rover and tower
			hdg = math.radians(self.navThread.roverDirection)
			Color(0, 0, 0)
			Rectangle(pos=(tpos[0] + 54, tpos[1] - 4), size=(10, 10))
			Color(1, 0, 0)
			if base:
				self.navScreen.destColor = [1, 0.4, 0.4, 1]
				Line(points=(tpos[0] + 59, tpos[1] + 1, rpos[0] + 54,
					rpos[1] - 4))
			Rectangle(pos=(tpos[0] + 55, tpos[1] - 3), size=(8, 8))
			Color(0.2, 0.2, 1)
			px = rpos[0] + 59
			py = rpos[1] + 1
			Triangle(points=(px + 10 * math.sin(hdg),
				py + 10 * math.cos(hdg),
				px + 8 * math.sin(hdg + math.pi * 0.75),
				py + 8 * math.cos(hdg + math.pi * 0.75),
				px + 8 * math.sin(hdg + math.pi * 1.25),
				py + 8 * math.cos(hdg + math.pi * 1.25)))			
		
	# handle clicks on the map
	def mapClick(self, pos, button):
		# check if it's actually on the visible potion of the map
		if self.activeForm is not None:
			return
		if pos[0] > 60 and pos[1] < Window.height - 80:
			self.navThread.mailbox.put({"click":(int(pos[0] - 60),
				int(pos[1]), button)})			
				
	## Drive Screen Controls
	def drillMode(self):
		if self.drillUI is None:
			self.drillUI = ExperimentControls()
			self.sm.current_screen.add_widget(self.drillUI)
		else:
			self.sm.current_screen.remove_widget(self.drillUI)
			self.drillUI = None

class TelemetryScreen(Screen):
	pass
			
class NavigationScreen(Screen):
	pass

class NewMarkerForm(Widget):
	pass

class NewMarkerFormDd(NewMarkerForm):
	pass

class NewMarkerFormDMm(NewMarkerForm):
	pass

class NewMarkerFormDMS(NewMarkerForm):
	pass

class ChooseMarkerForm(Widget):
	pass

class RemoveMarkerForm(Widget):
	pass

class LoadMarkersForm(Widget):
	pass

class SaveMarkersForm(Widget):
	pass

class TurretScreen(Screen):
	pass

class DriveScreen(Screen):
	pass
	
class ExperimentControls(Widget):
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

