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
from kivy.app import App

#Turn off fullscreen - alternatively use 'fake' for borderless
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
from kivy.core.window import Window
Window.size = (1000,600)
from kivy.clock import Clock

#import refrenced GUI components
from kivy.uix.floatlayout import FloatLayout



import time

convert = threads.unicodeConvert.convert

#In code references of Kv widgets
class AppLayout(FloatLayout):
	def updateTime(self, *args):
		self.ids.btn2.b_text = time.asctime()

class KivyGuiApp(App):
	kv_directory = 'gui'
	def build(self):
		self.Base = AppLayout()
		for key, val in self.Base.ids.items():
			print("key={0}, val={1}".format(key, val))
		#Set up clock to run function as 'threads'
		Clock.schedule_interval(self.displayQueue, 0.1)
		Clock.schedule_interval(self.Base.updateTime, 1)
		return self.Base
	
	# Button handler based off button.func property
	def buttonHandler(self, func):
		if(func == 'ac'):
			print('Arm Camera Selected')
			self.Base.ids.btn1.ind = (0, 1, 0, 1)
			self.Base.ids.btn2.ind = (1, 0, 0, 1)
			self.Base.ids.videoScreen.eos = True
			
		if(func == 'dc'):
			print('Drive Camera Selected')
			self.Base.ids.btn1.ind = (1, 0, 0, 1)
			self.Base.ids.btn2.ind = (0, 1, 0, 1)
		
		#Default action
		if(func == 'none'):
			print('Info: Button has no function')
			
		if(func == 'Navigation'):
			print('Navigation Window')
			
	#test to display an amt of Queue items on label
	def displayQueue(self, amt):
		if not self.mailbox.empty():
			#self.ltb2.l_text
			data = str(self.mailbox.get())
			print(data)
		else:
			pass
			#print("no data in queue")
	
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

#Main App
KivyGuiApp().run()
