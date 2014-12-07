#Import all of the thread modules
from threads.communicationThread import communicationThread
from threads.inputThread import inputThread
from threads.navigationThread import navigationThread
from threads.panelThread import panelThread

#Import modules needed for GUI communication
from config.settingsDefinition import settings_json
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
		self.root_widget = Builder.load_file('gui\kivygui.kv')
		self.main = self.root_widget.get_screen('app')
		self.nav = self.root_widget.get_screen('nav')
		self.settings_cls = SettingsWithTabbedPanel
		for key, val in self.main.ids.items():
			print("key={0}, val={1}".format(key, val))
		Clock.schedule_interval(self.displayQueue, 0.1)
		Clock.schedule_interval(self.main.updateTime, 1)
		return self.root_widget
	
	# Button handler based off button.func property
	def buttonHandler(self, func):
		if(func == 'ac'):
			print('Arm Camera Selected')
			self.main.ids.ArmCam.ind = (0, 1, 0, 1)
			self.main.ids.DriveCam.ind = (1, 0, 0, 1)
			
		if(func == 'dc'):
			print('Drive Camera Selected')
			self.main.ids.ArmCam.ind = (1, 0, 0, 1)
			self.main.ids.DriveCam.ind = (0, 1, 0, 1)
		
		#Default action
		if(func == 'none'):
			print('Info: Button has no function')
			
		if(func == 'Navigation'):
			print('Navigation Window')
	
	def changeScreen(self):
		if(self.root_widget.current_screen.name == 'app'):
			self.root_widget.transition = SlideTransition(direction="left")
			self.root_widget.current = 'nav'
		elif(self.root_widget.current_screen.name == 'nav'):
			self.root_widget.transition = SlideTransition(direction="right")
			self.root_widget.current = 'app'
			
	#test to display an amt of Queue items on label
	def displayQueue(self, amt):
		if not self.mailbox.empty():
			#self.ltb2.l_text
			data = str(self.mailbox.get())
			print(data)
		else:
			pass
			#print("no data in queue")
	
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
		References an internal ini file and some json code elsewhere
		=========================================================================================
	'''
	def get_application_config(self):
		return super(KivyGuiApp, self).get_application_config('%(appdir)s/config/config.ini')
	
	def build_config(self, config):
		config.setdefaults('example', {
			'boolexample': False,
			'numericexample': 10,
			'optionsexample': 'option2',
			'stringexample': 'some_string',
			'pathexample': '~'})

	def build_settings(self, settings):
		settings.add_json_panel('Settings', self.config, data=settings_json)

	def on_config_change(self, config, section, key, value):
		print config, section, key, value

#Main App
KivyGuiApp().run()
