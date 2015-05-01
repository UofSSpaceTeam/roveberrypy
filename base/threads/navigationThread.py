import baseMessages as messages
import threading
from Queue import Queue
import time
from unicodeConvert import convert

class NavigationThread(threading.Thread):
	
	class Waypoint():
		def __init__(self, name, location, renderPos):
			self.location = location
			self.name = name
			self.renderPos = renderPos
			self.active = False
	
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.name = "navigationThread"
		self.parent = parent
		self.mailbox = Queue()

		self.mapTopRight = parent.settings["mapTopRight"]
		self.mapBottomLeft = parent.settings["mapBottomLeft"]
		self.mapCenter = ((self.mapTopRight[0] + self.mapBottomLeft[0]) / 2,
			(self.mapTopRight[1] + self.mapBottomLeft[1]) / 2)
		self.viewCenter = list(self.mapCenter)
		
		self.imageSize = [1, 1]
		self.windowSize = [0, 0]
		self.mapRenderSize = [1, 1]
		self.zoom = 1.0
		self.mapRenderPos = [0, 0]
		self.cursorRenderPos = [0, 0]
		
		self.roverLocation = self.mapCenter
		self.roverRenderPos = self.getRenderPos(self.roverLocation)
		self.towerLocation = self.mapCenter
		self.towerRenderPos = self.getRenderPos(self.towerLocation)
		self.waypoints = []

	def run(self):
		while True:
			while self.mailbox.empty():
				time.sleep(0.1)
			changed = False
			while not self.mailbox.empty():
				data = self.mailbox.get()
				# print data
				if "roverGPS" in data:
					changed = True
					self.roverLocation = data["gps"]
				
				if "waypoint" in data:
					changed = True
					if data["waypoint"] == "prev":
						pass
					
				if "imageSize" in data:
					changed = True
					self.imageSize = data["imageSize"]
					
				if "resize" in data:
					changed = True
					self.windowSize = data["resize"]
					
				if "scroll" in data:
					changed = True
					self.viewCenter[1] += data["scroll"][0] * getXScale()
					self.viewCenter[0] += data["scroll"][1] * getYScale()
					
				if "click" in data:
					changed = True
					if data["click"][2] == "left":
						self.viewCenter = self.getActualPos(data["click"][0:2])
					elif data["click"][2] == "right":
						self.waypoints.append(self.Waypoint("#" +
							str(len(self.waypoints)),
							self.getActualPos(data["click"][0:2]),
							data["click"][0:2]))
					elif data["click"][2] == "scrollup":
						self.zoom /= 1.2
					elif data["click"][2] == "scrolldown":
						self.zoom *= 1.2
				
				if "towerGPS" in data:
					changed = True
					self.towerLocation = data["towerGPS"]
				
				if "snap" in data:
					changed = True
					if data["snap"] == "rover":
						if self.roverLocation is not None:
							self.viewCenter = self.roverLocation
					elif data["snap"] == "center":
						self.viewCenter = list(self.mapCenter)

			if not changed:
				continue
			self.mapRenderSize[0] = self.imageSize[0] * self.zoom
			self.mapRenderSize[1] = self.imageSize[1] * self.zoom
			self.mapRenderPos = self.getMapPos(self.viewCenter)
			self.cursorRenderPos = self.getRenderPos(self.viewCenter)
			self.roverRenderPos = self.getRenderPos(self.roverLocation)
			self.towerRenderPos = self.getRenderPos(self.towerLocation)
			for wp in self.waypoints:
				wp.renderPos = self.getRenderPos(wp.location)
			self.parent.mailbox.put({"updateMap":""})
	
	# input is pixels, output is lat, lon
	def getActualPos(self, (x, y)):
		return(self.viewCenter[0] + (y - self.windowSize[1] / 2) *
			self.getYScale(), self.viewCenter[1] + (x - self.windowSize[0] / 2)
			* self.getXScale())
	
	# input is lat, lon, output is pixels
	def getRenderPos(self, (lat, lon)):
		return((lon - self.mapBottomLeft[1]) / self.getXScale() +
			self.mapRenderPos[0], (lat - self.mapBottomLeft[0]) / self.getYScale()
			+ self.mapRenderPos[1])
	
	# locate bottom-left corner of map image in the app
	def getMapPos(self, (lat, lon)):
		return(self.windowSize[0] / 2 - (lon - self.mapBottomLeft[1]) /
		self.getXScale(), self.windowSize[1] / 2 - (lat -
		self.mapBottomLeft[0]) / self.getYScale())
	
	# degrees per rendered pixel
	def getXScale(self):
		return((self.mapTopRight[1] - self.mapBottomLeft[1])
			/ self.mapRenderSize[0])
	
	def getYScale(self):
		return((self.mapTopRight[0] - self.mapBottomLeft[0])
			/ self.mapRenderSize[1])

