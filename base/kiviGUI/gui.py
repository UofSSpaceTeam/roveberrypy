import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class Canvas(GridLayout):
	def __init__(self, **kwargs):
		super(Canvas, self).__init__(**kwargs)
		self.cols = 2
		self.add_widget(CameraFeeds())
        
class CameraFeeds(GridLayout):
	def __init__(self, **kwargs):
		super(CameraFeeds, self).__init__(**kwargs)
		self.cols = 1
		self.add_widget(Button(text='Front Camera'))
		self.add_widget(Button(text='Arm Camera'))

class Gui(App):
	def build(self):
		return Canvas()


if __name__ == '__main__':
   Gui().run()