#Import all of the thread modules
from threads.communicationThread import communicationThread
from threads.inputThread import inputThread
from threads.navigationThread import navigationThread
from threads.panelThread import panelThread

#Import modules needed for GUI communication
import baseMessages
import json
from Queue import Queue
import time
import threads.unicodeConvert

#imports for Kivy GUI
import kivy
#Import modules needed to load the kv language file
from kivy.app import App
from kivy.lang import Builder
#Turn off fullscreen - alternatively use 'fake' for borderless
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
#Import modules needed to make a window (Resizeable)
from kivy.core.window import Window
Window.size = (800,500)
#Import scheduler
from kivy.clock import Clock

convert = threads.unicodeConvert.convert
	
class KivyGuiApp(App):
	def build(self):
		#Set up clock to run functions at a schedule (seconds)
		Clock.schedule_interval(self.displayQueue, 1)
		#build GUI from kv
		self.root = Builder.load_file('gui/gui.kv')
		return self.root
		
	def buttonHandler(self, func):
		if(func == 'ac'):
			print('Arm Camera Selected')
			
		if(func == 'dc'):
			print('Drive Camera Selected')
		
		if(func == 'none'):
			print('Info: Button has no function')
			
	#test to display an amt of Queue items on label
	def displayQueue(self, amt):
		if not self.mailbox.empty():
			self.ltb2.l_text = str(self.mailbox.get())
		else:
			print("no data in queue")
	
	def on_start(self):
		##Set up Queue
		self.mailbox = Queue()
			
		##Set up the threads
		# make each top-level thread
		self.commThread = communicationThread()
		self.inputThread = inputThread()
		self.navThread = navigationThread()
		self.panelThread = panelThread()
		
		# configure threads
		self.commThread.sendPort = 8001
		self.commThread.receivePort = 8000
		self.commThread.sendInterval = 0.25
		self.commThread.inputThread = self.inputThread
		self.commThread.navThread = self.navThread
		self.commThread.panelThread = self.panelThread
		self.commThread.guiThread = self
		self.inputThread.commThread = self.commThread
		
		##Load the other threads
		print("starting")
		self.startThreads()
	
	def startThreads(self):
		self.commThread.start()
		self.inputThread.start()
		self.navThread.start()
		self.panelThread.start()

	def stopThreads(self):
		self.inputThread.stop()
		self.commThread.stop()
		self.navThread.stop()
		self.panelThread.stop()
		
	def on_stop(self):
		print('exiting')
		#Unload all threads
		self.stopThreads()

try:
	KivyGuiApp().run()
except:
	KivyGuiApp.stopThreads()
