import sys
sys.dont_write_bytecode = True

#Import all of the thread modules
from threads.communicationThread import communicationThread
from threads.inputThread import inputThread
from threads.navigationThread import navigationThread
from threads.panelThread import panelThread

#Import modules needed for GUI communication
import config.baseMessages
import json
from Queue import Queue
import time
import threads.unicodeConvert

#imports for Kivy GUI
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from config.settingsDefinition import general_json, navigation_json
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (1000,600)
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

#imports for OpenGL Loading
from gui.meshLoader.objectRenderer import ObjectRenderer
from kivy.animation import Animation

import time

convert = threads.unicodeConvert.convert

#In code references of Kv widgets
class AppScreen(Screen):
	def updateTime(self, *args):
		self.ids.mission.clock_text = time.asctime()
		
class NavScreen(Screen):
	pass
	
class GuiScreenManager(ScreenManager):
	pass

# Custom 3d Widget	
class BaseView(ObjectRenderer):
	def position(self, angle):
		print(angle)
		Animation(cam_rotation=(+7, 180-angle, 0), cam_translation=(0, 0.35, -2), d=0).start(self)

	def update_lights(self, dt):
		for i in range(self.nb_lights):
			self.light_sources[i] = [self.light_radius, 5, self.light_radius, 1.0]
		for k in self.light_sources.keys():
			if k >= self.nb_lights:
				del(self.light_sources[k])
		
class View(BaseView):
	pass

class KivyGuiApp(App):
	def build(self):
		#Load up application settings
		self.settings_cls = SettingsWithTabbedPanel
		self.follow_rover = self.config.get('navigation', 'follow_rover')
		self.map_img = self.config.get('navigation', 'map_path')
		self.scale_factor = 1
		self.map_tr = (float(convert(self.config.get('navigation', 'tr_lon'))), float(convert(self.config.get('navigation', 'tr_lat'))))
		self.map_bl = (float(convert(self.config.get('navigation', 'bl_lon'))), float(convert(self.config.get('navigation', 'bl_lat'))))
		self.map_size = (float(convert(self.config.get('navigation', 'map_size_x'))), float(convert(self.config.get('navigation', 'map_size_y'))))
		self.position_gps = (-106.628067,52.132756)
		self.map_scale = (1,1)
		self.angle = 0
		
		print("window size")
		print Window.size
		self.window_size = Window.size
		
		#Set up application
		self.title = 'USST Rover Application'
		self.root_widget = Builder.load_file('gui\kivygui.kv')
		self.main = self.root_widget.get_screen('app')
		self.nav = self.root_widget.get_screen('nav')
		self.map_scale = ((self.map_tr[0] - self.map_bl[0])/self.map_size[0], (self.map_tr[1] - self.map_bl[1])/self.map_size[1])
		self.nav.ids.map.position = ((self.position_gps[0]-self.map_bl[0])/self.map_scale[0],(self.position_gps[1]-self.map_bl[1])/self.map_scale[1])
		
		#Debug: list all of our named widgets on each screen
		for key, val in self.main.ids.items():
			print("key={0}, val={1}".format(key, val))
		for key, val in self.nav.ids.items():
			print("key={0}, val={1}".format(key, val))
			
		#Start our clock/threads for the GUI
		Clock.schedule_interval(self.displayQueue, 0.1)
		Clock.schedule_interval(self.main.updateTime, 1)
		Clock.schedule_interval(self.autoRecenterMap, 2)
		Clock.schedule_once(self.main.ids.Ball3d.update_lights, 0)
		
		return self.root_widget
	
	# Button handler based off button.func property
	def buttonHandler(self, func):
		#Camera Buttons
		if(func == 'ac'):
			print('Arm Camera Selected')
			self.main.ids.ArmCam.ind = (0, 1, 0, 1)
			self.main.ids.DriveCam.ind = (1, 0, 0, 1)
			
		if(func == 'dc'):
			print('Drive Camera Selected')
			self.main.ids.ArmCam.ind = (1, 0, 0, 1)
			self.main.ids.DriveCam.ind = (0, 1, 0, 1)
			## Don't think this is working properly
			self.main.ids.videoScreen.source = 'http://10.64.226.70:8080/?action=stream'
			self.main.ids.videoScreen.state = 'play'
		
		#Moves map to show rover.. kinda buggy but usable
		if(func == 'on_map'):
			self.nav.ids.scroll_map.scroll_x = self.nav.ids.map.position[0]*self.nav.ids.map.zoom/(self.nav.ids.map.map_size[0])
			self.nav.ids.scroll_map.scroll_y = self.nav.ids.map.position[1]*self.nav.ids.map.zoom/(self.nav.ids.map.map_size[1])
		
		#Default action (no action)
		if(func == 'none'):
			print('Info: Button has no function')
	
	#Chooses animation and changes the screen
	def changeScreen(self):
		if(self.root_widget.current_screen.name == 'app'):
			self.root_widget.transition = SlideTransition(direction="left")
			self.root_widget.current = 'nav'
		elif(self.root_widget.current_screen.name == 'nav'):
			self.root_widget.transition = SlideTransition(direction="right")
			self.root_widget.current = 'app'
			
	#Debug: test to display an amt of Queue items on label
	def displayQueue(self, dt):
		if not self.mailbox.empty():
			data = str(self.mailbox.get())
			self.main.ids.tele.text = data
			
		else:
			self.main.ids.tele.text = "No Data!"
		
	#Calls to re-center map... auto press button
	def autoRecenterMap(self, dt):
		if(self.follow_rover == '1'):
			self.buttonHandler('on_map')
			
	def turnNavball(self):
		self.angle += 5
		self.main.ids.Ball3d.position(self.angle)
	
	'''
		=========================================================================================
		Main application threads
		Usually this is not to be changed
		See threads folder for code
		=========================================================================================
	'''
	
	def on_start(self):
		#Set up Queue
		self.mailbox = Queue()
			
		#Set up the threads
		self.commThread = communicationThread()
		self.inputThread = inputThread()
		self.navThread = navigationThread()
		self.panelThread = panelThread()
		
		#Any thread configuration options are run here
		self.commThread.sendPort = 31314
		self.commThread.receivePort = 31313
		self.commThread.inputThread = self.inputThread
		self.commThread.navThread = self.navThread
		self.commThread.panelThread = self.panelThread
		self.commThread.guiThread = self
		self.inputThread.commThread = self.commThread
		
		#Load the other threads
		print("starting")
		self.startThreads()
	
	def startThreads(self):
		self.commThread.start()
		self.inputThread.start()
		self.navThread.start()
		self.panelThread.start()

	def stopThreads(self):
		self.inputThread.stop()
		time.sleep(0.2)
		self.commThread.stop()
		self.navThread.stop()
		self.panelThread.stop()
		
	def on_stop(self):
		print('exiting')
		#Unload all threads
		self.stopThreads()
		
	def on_resize(self):
		self.window_size = Window.size
		
	'''
		=========================================================================================
		Configuration
		References an internal ini file generated by a structure defined in json
		
		-- this could probably be moved to another module to make things cleaner
		=========================================================================================
	'''
	def get_application_config(self):
		return super(KivyGuiApp, self).get_application_config('%(appdir)s/config/config.ini')
	
	def build_config(self, config):
		config.setdefaults('general', {
			'test_mode': False,
			'numericexample': 10,
			'drive_mode': 'Two Stick',
			'stringexample': 'some_string',
			'pathexample': '~'})
		config.setdefaults('navigation', {
			'follow_rover': False,
			'tr_lat': 52.139176,
			'tr_lon': -106.618917,
			'bl_lat': 52.127204,
			'bl_lon': -106.647735,
			'map_size_x': 5196,
			'map_size_y': 3605,
			'optionsexample': 'option2',
			'stringexample': 'some_string',
			'map_path': 'gui/campusmap.jpg'})

	def build_settings(self, settings):
		settings.add_json_panel('General', self.config, data=general_json)
		settings.add_json_panel('Navigation', self.config, data=navigation_json)

	def on_config_change(self, config, section, key, value):
		value = convert(value) #damn unicode...
		print(key, value)
		if(key == 'follow_rover'):
			self.follow_rover = value

#Main App
KivyGuiApp().run()