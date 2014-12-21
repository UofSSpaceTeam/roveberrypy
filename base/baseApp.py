#Import all of the thread modules
from threads.communicationThread import communicationThread
from threads.inputThread import inputThread
from threads.navigationThread import navigationThread
from threads.panelThread import panelThread

#Import modules needed for GUI communication
from config.settingsDefinition import general_json, navigation_json
import config.baseMessages
import json
from Queue import Queue
import time
import threads.unicodeConvert

#imports for Kivy GUI
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.lang import Builder

from kivy.core.window import Window
Window.size = (1000,600)
from kivy.clock import Clock



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
	


class KivyGuiApp(App):
	def build(self):
		#Load up application settings
		self.settings_cls = SettingsWithTabbedPanel
		self.follow_rover = self.config.get('navigation', 'follow_rover')
		self.map_img = self.config.get('navigation', 'map_path')
		self.scale_factor = 1
		self.map_tr = (float(convert(self.config.get('navigation', 'tr_lon'))), float(convert(self.config.get('navigation', 'tr_lat'))))
		self.map_bl = (float(convert(self.config.get('navigation', 'bl_lon'))), float(convert(self.config.get('navigation', 'bl_lat'))))
		print(self.map_tr)
		print(self.map_bl)
		self.position_gps = (-106.628067,52.139176)
		self.map_scale = (1,1)
		
		#Set up application
		self.title = 'USST Rover Application'
		self.root_widget = Builder.load_file('gui\kivygui.kv')
		self.main = self.root_widget.get_screen('app')
		self.nav = self.root_widget.get_screen('nav')
		self.map_scale = ((self.map_tr[0] - self.map_bl[0])/self.nav.ids.map.map_size[0], (self.map_tr[1] - self.map_bl[1])/self.nav.ids.map.map_size[1])
		self.nav.ids.map.position = ((self.position_gps[0]-self.map_bl[0])/self.map_scale[0],(self.position_gps[1]-self.map_bl[1])/self.map_scale[1])
		print(self.nav.ids.map.position)
		print(self.map_scale)
		
		#Debug: list all of our named widgets on each screen
		for key, val in self.main.ids.items():
			print("key={0}, val={1}".format(key, val))
		for key, val in self.nav.ids.items():
			print("key={0}, val={1}".format(key, val))
			
		#Start our clock/threads for the GUI
		Clock.schedule_interval(self.displayQueue, 0.1)
		Clock.schedule_interval(self.main.updateTime, 1)
		Clock.schedule_interval(self.autoRecenterMap, 2)
		
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
		
		#Moves map to show rover.. kinda buggy but usable
		if(func == 'on_map'):
			pos = self.nav.ids.map.position
			print pos
			size = self.nav.ids.map.size
			print self.nav.ids.map.map_size
			zoom = self.nav.ids.map.zoom
			self.nav.ids.scroll_map.scroll_x = pos[0]*zoom/(size[0])
			self.nav.ids.scroll_map.scroll_y = pos[1]*zoom/(size[1])
		
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
			#self.ltb2.l_text
			data = str(self.mailbox.get())
			print(data)
		else:
			pass
			#print("no data in queue")
		
	#Calls to re-center map... auto press button? (if enabled)
	def autoRecenterMap(self, dt):
		if(self.follow_rover == '1'):
			self.buttonHandler('on_map')
	
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
		self.commThread.sendPort = 8001
		self.commThread.receivePort = 8000
		self.commThread.sendInterval = 0.25
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
			'boolexample': False,
			'numericexample': 10,
			'optionsexample': 'option2',
			'stringexample': 'some_string',
			'pathexample': '~'})
		config.setdefaults('navigation', {
			'follow_rover': False,
			'tr_lat': 52.139176,
			'tr_lon': -106.618917,
			'bl_lat': 52.127204,
			'bl_lon': -106.647735,
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