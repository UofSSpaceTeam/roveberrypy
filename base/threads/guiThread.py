import baseMessages
import threading
import json
from Queue import Queue
import time
import unicodeConvert

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
Window.size = (430,330)
from kivy.uix.videoplayer import VideoPlayer

convert = unicodeConvert.convert

class guiThread(threading.Thread):		
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "guiThread"
		self.exit = False
		self.mailbox = Queue()
		self.KivyGuiApp().run()
	
	def run(self):
		while not self.exit:
			time.sleep(0.01)

	def stop(self):
		self.exit = True
		
	class KivyGuiApp(App):
		def build(self):
			self.bind(on_stop=exit)
			self.root = Builder.load_file('gui/gui.kv')
			return self.root
			
		def buttonHandler(self, func):
			if(func == 'ac'):
				print('Arm Camera Selected')
				
			if(func == 'dc'):
				print('Drive Camera Selected')
			
			if(func == 'none'):
				print('Info: Button has no function')
				
			
		#Event handler binded at build to manage issues with unloading pygame
		#When closing kivy app.
		#Really not sure if this works properly
		def exit(self):
			print('exiting')
			guiThread.stop()
		