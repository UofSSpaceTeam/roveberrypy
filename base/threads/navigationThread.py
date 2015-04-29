import baseMessages as messages
import threading
from Queue import Queue
import time
from unicodeConvert import convert

class NavigationThread(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		self.name = "navigationThread"
		self.parent = parent
		self.mailbox = Queue()
		self.ready = False
		self.zoom = 1.0
		self.mapTopRight = parent.settings["mapTopRight"]
		self.mapBottomLeft = parent.settings["mapBottomLeft"]
		self.mapCenter = ((self.mapTopRight[0] + self.mapBottomLeft[0]) / 2,
			(self.mapTopRight[1] + self.mapBottomLeft[1]) / 2)
		self.viewCenter = list(self.mapCenter)
		self.imageSize = [1, 1]
		self.windowSize = [0, 0]
		self.renderSize = [1, 1]
		self.renderPos = [0, 0]

	def run(self):
		while True:
			while self.mailbox.empty():
				time.sleep(0.1)
			changed = False
			while not self.mailbox.empty():
				data = self.mailbox.get()
				if "imageSize" in data:
					changed = True
					self.imageSize = data["imageSize"]
				if "resize" in data:
					changed = True
					self.windowSize = data["resize"]
				if "zoom" in data:
					changed = True
					if data["zoom"] == "+":
						self.zoom *= 1.2
					elif data["zoom"] == "-":
						self.zoom /= 1.2
				if "scroll" in data:
					changed = True
					self.viewCenter[1] += data["scroll"][0] * self.getXScale()
					self.viewCenter[0] += data["scroll"][1] * self.getYScale()
				if "snap" in data:
					changed = True
					if data["snap"] == "center":
						self.viewCenter = list(self.mapCenter)
			if not changed:
				continue
			self.renderSize[0] = self.imageSize[0] * self.zoom
			self.renderSize[1] = self.imageSize[1] * self.zoom
			self.renderPos = self.getRenderPos()
			# print "window: " + str(self.windowSize)
			# print "render size: " + str(self.renderSize)
			# print "center: " + str(self.mapCenter)
			# print "X scale: " + str(self.getXScale())
			# print "Y scale: " + str(self.getYScale())
			# print "view: " + str(self.viewCenter)
			# print "render pos: " + str(self.renderPos)
			self.parent.mailbox.put({"updateMap":""})
		
	# degrees per rendered pixel
	def getXScale(self):
		return((self.mapTopRight[1] - self.mapBottomLeft[1])
			/ self.renderSize[0])
	
	def getYScale(self):
		return((self.mapTopRight[0] - self.mapBottomLeft[0])
			/ self.renderSize[1])
	
	# lat, lon
	def getViewCenter(self):
		# maaaaaaaaath
		return(self.mapBottomLeft[0] + (self.renderPos[1] + self.windowSize[1]
			/ 2) * self.getYScale(), self.mapBottomLeft[1] + (self.renderPos[0]
				+ self.windowSize[0] / 2) * self.getXScale())
	
	# draw offset
	def getRenderPos(self):
		return(self.windowSize[0] / 2 - (self.viewCenter[1] -
			self.mapBottomLeft[1]) / self.getXScale(), self.windowSize[1] / 2 -
			(self.viewCenter[0] - self.mapBottomLeft[0]) / self.getYScale())
			
		