import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
        BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
import time

class TelemetryWidget(Widget):
	
	points1 = ListProperty([])
	points2 = ListProperty([])
	points3 = ListProperty([])
	points4 = ListProperty([])
	points5 = ListProperty([])
	points6 = ListProperty([])
	points7 = ListProperty([])
	points8 = ListProperty([])
	points9 = ListProperty([])	
	
	dt = NumericProperty(0)
	x_pos = NumericProperty(0)
	
	data1 = NumericProperty(0)
	data2 = NumericProperty(0)
	data3 = NumericProperty(0)
	data4 = NumericProperty(0)
	data5 = NumericProperty(0)
	data6 = NumericProperty(0)
	data7 = NumericProperty(0)
	data8 = NumericProperty(0)
	data9 = NumericProperty(0)
	
	
	max_data1 = NumericProperty(0)
	max_data2 = NumericProperty(0)
	max_data3 = NumericProperty(0)
	max_data4 = NumericProperty(0)
	max_data5 = NumericProperty(0)
	max_data6 = NumericProperty(0)
	max_data7 = NumericProperty(0)
	max_data8 = NumericProperty(0)
	max_data9 = NumericProperty(0)
	
	avg_data1 = NumericProperty(0)
	avg_data2 = NumericProperty(0)
	avg_data3 = NumericProperty(0)
	avg_data4 = NumericProperty(0)
	avg_data5 = NumericProperty(0)
	avg_data6 = NumericProperty(0)
	avg_data7 = NumericProperty(0)
	avg_data8 = NumericProperty(0)
	
	dataSum = [0,0,0,0,0,0,0,0,0]
	
	
	def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
		super(TelemetryWidget, self).__init__(**kwargs)
		baseApp = App.get_running_app()
		

	
	def animate(self, do_animation):
		if do_animation:
				Clock.schedule_interval(self.update_points_animation, 0.1)
		else:
				Clock.unschedule(self.update_points_animation)

	def update_points_animation(self, dt):
		
		cx1 = self.width * 0.05		
		cx2 = self.width * 0.35
		cx3 = self.width * 0.7

		w = self.width * 0.8
		self.dt += dt
		data = {}
		data.update(self.getData())
		self.data1 = data["1"]
		self.dataSum[0] += self.data1 
		self.data2 = data["2"]
		self.dataSum[1] += self.data2
		self.data3 = data["3"]
		#print(self.data3)
		self.dataSum[2] += self.data3
		self.data4 = data["4"]
		self.dataSum[3] += self.data4
		self.data5 = data["5"]
		self.dataSum[4] += self.data5
		self.data6 = data["6"]
		self.dataSum[5] += self.data6
		self.data7 = data["7"]
		self.dataSum[6] += self.data7
		self.data8 = data["8"]
		self.dataSum[7] += self.data8
		#extra list 
		self.data9 = data["8"]
		self.dataSum[8] += self.data9
		
	
		self.drawPoints(self.points1, self.data1,
			self.points2, self.data2, self.points3, self.data3, cx1)
		self.drawPoints(self.points4, self.data4,
			self.points5, self.data5, self.points6, self.data6, cx2)
		self.drawPoints(self.points7, self.data7,
			self.points8, self.data8, self.points9, self.data9, cx3)
		self.x_pos += 1
		
		self.updateMax()
		
		self.avg_data1 = self.getAvg(self.dataSum[0])
		self.avg_data2 = self.getAvg(self.dataSum[1])
		self.avg_data3 = self.getAvg(self.dataSum[2])
		self.avg_data4 = self.getAvg(self.dataSum[3])
		self.avg_data5 = self.getAvg(self.dataSum[4])
		self.avg_data6 = self.getAvg(self.dataSum[5])
		self.avg_data7 = self.getAvg(self.dataSum[6])
		self.avg_data8 = self.getAvg(self.dataSum[7])
	
		
	def drawPoints(self, points1, data1, points2, data2, points3, data3, cx):
	
		cy = self.height * 0.5
		
		if self.x_pos < self.width * 0.25 :
			points1.append(cx + (self.x_pos) )
			points1.append(cy + data1 )
			points2.append(cx + (self.x_pos) )
			points2.append(cy + data2 )
			points3.append(cx + (self.x_pos) )
			points3.append(cy + data3 )
			
		else:
			points1.pop(0)
			points1.pop(0)
			points2.pop(0)
			points2.pop(0)
			points3.pop(0)
			points3.pop(0)
			
			for i in range(0, min(len(points1), len(points2),
				len(points3))):
				if i % 2 == 0:
					points1[i] = points1[i] - 1
					points2[i] = points2[i] - 1
					points3[i] = points3[i] - 1
					
			points1.append(cx + self.width * 0.25  )
			points1.append(cy + data1 )
			points2.append(cx + self.width * 0.25  )
			points2.append(cy + data2 )
			points3.append(cx + self.width * 0.25  )
			points3.append(cy + data3 )

		
	def getData(self):
		#for testing
		data = {}
		#data["1"] = 1 + self.data1 
		#data["2"] = 5 + self.data2
		#data["3"] = 10 + self.data3
		#if self.data1 > 200:
		#		data["1"] = 0
		#if self.data2 > 200:
		#		data["2"] = 0
		#if self.data3 > 200:
		#		data["3"] = 0
		#return data
		
		
		#actual data code
		data["1"] = App.get_running_app().teleThread.gx
		data["2"] = App.get_running_app().teleThread.gy
		data["3"] = App.get_running_app().teleThread.gz
		print(App.get_running_app().teleThread.gz)
		#print(data["3"])
		data["4"] = App.get_running_app().teleThread.ax
		data["5"] = App.get_running_app().teleThread.ay
		data["6"] = App.get_running_app().teleThread.az
		data["7"] = App.get_running_app().teleThread.vout
		data["8"] = App.get_running_app().teleThread.isense
		return data
				
	def updateMax(self):
		if self.data1 > self.max_data1:
			self.max_data1 = self.data1
		if self.data2 > self.max_data2:
			self.max_data2 = self.data2
		if self.data3 > self.max_data3:
			self.max_data3 = self.data3
		if self.data4 > self.max_data4:
			self.max_data4 = self.data4
		if self.data5 > self.max_data5:
			self.max_data5 = self.data5
		if self.data6 > self.max_data6:
			self.max_data6 = self.data6
		if self.data7 > self.max_data7:
			self.max_data7 = self.data7
		if self.data8 > self.max_data8:
			self.max_data8 = self.data8
			
	def getAvg(self, dataSum):
		if self.x_pos != 0:
			return round(float(dataSum) / self.x_pos,2)
