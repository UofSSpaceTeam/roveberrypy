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
from kivy.lang import Builder
#Turn off fullscreen - alternatively use 'fake' for borderless
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
from kivy.core.window import Window
Window.size = (800,500)
#Scheduler (for GUI related threading)
from kivy.clock import Clock

#import refrenced GUI components
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

convert = threads.unicodeConvert.convert
	
class KivyGuiApp(App):
	def build(self):
		#Set up clock to run function as 'threads'
		Clock.schedule_interval(self.displayQueue, 0.1)
		#build gui layout
		self.root = Builder.load_file('gui/gui.kv')
		return self.root
	
	# Button handler based off button.func property
	def buttonHandler(self, func):
		if(func == 'ac'):
			print('Arm Camera Selected')
			
		if(func == 'dc'):
			print('Drive Camera Selected')
		
		#Default action
		if(func == 'none'):
			print('Info: Button has no function')
			
	#test to display an amt of Queue items on label
	def displayQueue(self, amt):
		if not self.mailbox.empty():
			#self.ltb2.l_text
			data = str(self.mailbox.get())
			self.applayout.func1()
			#print(data)
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
