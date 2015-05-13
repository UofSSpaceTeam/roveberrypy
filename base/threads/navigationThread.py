# -*- coding: UTF-8 -*-
import baseMessages as messages
import threading
from Queue import Queue
import time
import math
import pickle
from unicodeConvert import convert

class Marker():
	def __init__(self, name, lat, lon):
		self.name = name
		self.location = [lat, lon]
		self.renderPos = None
		self.selected = False

class NavigationThread(threading.Thread):
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
		
		self.latScale = 111132 - 559.8 * math.cos(2 *
			math.radians(self.mapCenter[0])) + 1.175 * math.cos(4 *
			math.radians(self.mapCenter[0]))
		self.lonScale = math.radians(6371000 *
			math.cos(math.radians(self.mapCenter[0])))
		
		self.imageSize = [1, 1]
		self.windowSize = [0, 0]
		self.mapRenderSize = [1, 1]
		self.zoom = 1.0
		self.mapRenderPos = [0, 0]
		
		self.roverLocation = self.mapBottomLeft
		self.roverSpeed = 0 # m / min
		self.roverDirection = 0
		self.roverRenderPos = self.getRenderPos(self.roverLocation)
		self.towerLocation = self.mapBottomLeft
		self.towerRenderPos = self.getRenderPos(self.towerLocation)
		self.markers = []
		self.displayStatus = "vector"
		self.printMode = "Dd"
		self.roverStatusText = ""
		self.destStatusText = ""
	
	def run(self):
		while True:
			while self.mailbox.empty():
				time.sleep(0.1)
			while not self.mailbox.empty():
				data = self.mailbox.get()
				# print data
				if "roverGPS" in data:
					# (lat, lon, speed, direction)
					# speed in meters / minute
					self.roverLocation = data["roverGPS"][0:2]
					self.roverSpeed = data["roverGPS"][2]
					self.roverDirection = data["roverGPS"][3]
				
				if "towerGPS" in data:
					print data["towerGPS"]
					self.towerLocation = data["towerGPS"]
					
				if "imageSize" in data:
					self.imageSize = data["imageSize"]
					
				if "resize" in data:
					self.windowSize = data["resize"]
				
				if "newMarker" in data:
					md = data["newMarker"]
					try:
						if not isinstance(data["newMarker"][1], tuple): # Dd
							self.markers.append(Marker(md[0], float(md[1]),
								float(md[2])))
						elif len(data["newMarker"][1]) == 2: # DMm
							latD = int(md[1][0])
							latM = float(md[1][1])
							lonD = int(md[2][0])
							lonM = float(md[2][1])
							self.markers.append(Marker(md[0],
								latD + cmp(latD, 0) * latM / 60.0,
								lonD + cmp(lonD, 0) * lonM / 60.0))
						elif len(data["newMarker"][1]) == 3: # DMS
							latD = int(md[1][0])
							latM = int(md[1][1])
							latS = float(md[1][2])
							lonD = int(md[2][0])
							lonM = int(md[2][1])
							lonS = float(md[2][2])
							self.markers.append(Marker(md[0],
								latD + cmp(latD, 0) * (latM / 60.0 +
								latS / 3600.0),
								lonD + cmp(lonD, 0) * (lonM / 60.0 +
								lonS / 3600.0)))
					except ValueError:
						pass
					
				if "chooseMarker" in data:
					self.clearSelection()
					if data["chooseMarker"] != "Base":
						for mk in self.markers:
							if mk.name == data["chooseMarker"]:
								mk.selected = True
								break
				
				if "removeMarker" in data:
					for mk in self.markers:
						if mk.name == data["removeMarker"]:
							self.markers.remove(mk)
							break
				
				if "loadMarkers" in data:
					try:
						wptFile = open(data["loadMarkers"])
						unpickler = pickle.Unpickler(wptFile)
						self.markers = unpickler.load()
						wptFile.close()
					except Exception:
						pass
				
				if "saveMarkers" in data:
					try:
						wptFile = open(data["saveMarkers"], "w")
						pickler = pickle.Pickler(wptFile)
						pickler.dump(self.markers)
						wptFile.close()
					except Exception:
						pass
				
				if "printMode" in data:
					self.printMode = data["printMode"]
				
				if "displayToggle" in data:
					if self.displayStatus == "vector":
						self.displayStatus = "location"
					else:
						self.displayStatus = "vector"
					
				if "scroll" in data:
					self.viewCenter[1] += data["scroll"][0] * getXScale()
					self.viewCenter[0] += data["scroll"][1] * getYScale()
				
				if "click" in data:
					if data["click"][2] == "right": # move
						self.viewCenter = self.getActualPos(data["click"][0:2])
					elif data["click"][2] == "left":
						self.select(data["click"][0:2])
					elif data["click"][2] == "middle": # testing
						self.roverLocation = self.getActualPos(data["click"][0:2])
					elif data["click"][2] == "scrollup":
						self.zoom /= 1.2
					elif data["click"][2] == "scrolldown":
						self.zoom *= 1.2
				
				if "snap" in data:
					if data["snap"] == "rover":
						if self.roverLocation is not None:
							self.viewCenter = self.roverLocation
					elif data["snap"] == "tower":
						self.viewCenter = list(self.towerLocation)

			self.mapRenderSize[0] = self.imageSize[0] * self.zoom
			self.mapRenderSize[1] = self.imageSize[1] * self.zoom
			self.mapRenderPos = self.getMapPos(self.viewCenter)
			self.roverRenderPos = self.getRenderPos(self.roverLocation)
			self.towerRenderPos = self.getRenderPos(self.towerLocation)
			
			for mk in self.markers:
				mk.renderPos = self.getRenderPos(mk.location)
			
			if self.displayStatus == "vector":
				self.roverStatusText = ("Rover: " +
					str(int(self.roverSpeed)) + "m/min, HDG " +
					str(int(self.roverDirection)) + "°")
				self.destStatusText = ""
				for mk in self.markers:
					if mk.selected:
						self.destStatusText = (str(mk.name) + ": " +
							str(int(self.getDistance(self.roverLocation,
							mk.location))) + "m @ " +
							str(int(self.getDirection(self.roverLocation,
							mk.location))) + "°")
				if self.destStatusText == "":
					self.destStatusText = ("Base: " +
							str(int(self.getDistance(self.roverLocation,
							self.towerLocation))) + "m, HDG " +
							str(int(self.getDirection(self.roverLocation,
							self.towerLocation))) + "°")
			elif self.displayStatus == "location":
				destLoc = None
				for mk in self.markers:
					if mk.selected:
						destLoc = mk.location
						break
				if destLoc is None:
					destLoc = self.towerLocation
				if self.printMode == "Dd":
					roverString = ("%.6f" % self.roverLocation[0] + ", %.6f" %
						self.roverLocation[1])
					destString = "%.6f" % destLoc[0] + ", %.6f" % destLoc[1]
				elif self.printMode == "DMm":
					roverString = self.toMinutes(self.roverLocation)
					destString = self.toMinutes(destLoc)
				elif self.printMode == "DMS":
					roverString = self.toDMS(self.roverLocation)
					destString = self.toDMS(destLoc)
				self.roverStatusText = "Rover: " + roverString
				self.destStatusText = ""
				for mk in self.markers:
					if mk.selected:
						self.destStatusText = str(mk.name) + ": " + destString
						break
				if self.destStatusText == "":
					self.destStatusText = "Base: " + destString
			self.parent.mailbox.put({"updateMap":""})
	
	# lat, lon -> meters
	def getDistance(self, a, b):
		dy = (b[0] - a[0]) * self.latScale
		dx = (b[1] - a[1]) * self.lonScale
		return math.hypot(dx, dy)
	
	# lat, lon -> degrees, heading
	def getDirection(self, a, b):
		dy = (b[0] - a[0]) * self.latScale
		dx = (b[1] - a[1]) * self.lonScale
		hdg = math.degrees(math.atan2(dy, dx))
		hdg = (90 - hdg) % 360.0
		return hdg
	
	# check if we are clicking on a waypoint
	# input in pixels
	def select(self, (x, y)):
		for mk in self.markers:
			if abs(x - mk.renderPos[0]) < 6 and abs(y - mk.renderPos[1]) < 6:
				for other in self.markers:
					other.selected = False
				mk.selected = True
				return
		if (abs(x - self.towerRenderPos[0]) < 6 and
		abs(y - self.towerRenderPos[1]) < 6):
			self.clearSelection()
	
	def clearSelection(self):
		for mk in self.markers:
			mk.selected = False
	
	# float -> DMm string
	def toMinutes(self, (lat, lon)):
		result = str(int(abs(lat))) + "° "
		minutes = (abs(lat) % 1.0) * 60.0
		result += "%.4f" % minutes + "\' "
		if lat > 0:
			result += "N, "
		else:
			result += "S, "
		result += str(int(abs(lon))) + "° "
		minutes = (abs(lon) % 1.0) * 60.0
		result += "%.4f" % minutes + "\' "
		if lon > 0:
			return result + "E"
		else:
			return result + "W"
	
	# float -> DMS string
	def toDMS(self, (lat, lon)):
		result = str(int(abs(lat))) + "° "
		minutes = (abs(lat) % 1.0) * 60.0
		seconds = (abs(minutes) % 1.0) * 60.0
		result += str(int(minutes)) + "\' " + "%.2f" % seconds + "\" "
		if lat > 0:
			result += "N, "
		else:
			result += "S, "
		result += str(int(abs(lon))) + "° "
		minutes = (abs(lon) % 1.0) * 60.0
		seconds = (abs(minutes) % 1.0) * 60.0
		result += str(int(minutes)) + "\' " + "%.2f" % seconds + "\" "
		if lon > 0:
			return result + "E"
		else:
			return result + "W"
	
	# input is pixels, output is lat, lon
	def getActualPos(self, (x, y)):
		return (self.viewCenter[0] + (y - self.windowSize[1] / 2) *
			self.getYScale(), self.viewCenter[1] + (x - self.windowSize[0] / 2)
			* self.getXScale())
	
	# input is lat, lon, output is pixels
	def getRenderPos(self, (lat, lon)):
		return((lon - self.mapBottomLeft[1]) / self.getXScale() +
			self.mapRenderPos[0], (lat - self.mapBottomLeft[0]) / self.getYScale()
			+ self.mapRenderPos[1])
	
	# locate bottom-left corner of map image in the app
	def getMapPos(self, (lat, lon)):
		return (self.windowSize[0] / 2 - (lon - self.mapBottomLeft[1]) /
		self.getXScale(), self.windowSize[1] / 2 - (lat -
		self.mapBottomLeft[0]) / self.getYScale())
	
	# degrees per rendered pixel
	def getXScale(self):
		return ((self.mapTopRight[1] - self.mapBottomLeft[1])
			/ self.mapRenderSize[0])
	
	def getYScale(self):
		return ((self.mapTopRight[0] - self.mapBottomLeft[0])
			/ self.mapRenderSize[1])

