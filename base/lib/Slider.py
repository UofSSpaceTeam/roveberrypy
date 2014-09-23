import pygame
	
class Slider:
	def __init__(self, function, label, default, (xMin, xMax, yPos)):
		self.function = function
		self.label = label
		self.xMin = xMin
		self.xMax = xMax
		self.yPos = yPos
		self.set(default)
		self.font = pygame.font.Font(None, 20)
		self.label = self.font.render(self.label, 1, (255, 255, 255))
		labelSize = self.label.get_size()
		self.labelXPosition = self.xMin + 0.5 * (self.xMax - self.xMin - labelSize[0])
		self.labelYPosition = self.yPos - 23
		self.obj = None
		self.dragging = False

	def draw(self, screen): # redraw the button with centered label
		if self.dragging:
			self.drag()
		pygame.draw.rect(screen, (70, 70, 70), (self.xMin - 10, self.yPos - 25, self.xMax - self.xMin + 20, 40))
		pygame.draw.rect(screen, (0, 0, 0), (self.xMin, self.yPos + 1, self.xMax - self.xMin, 2))
		self.obj = pygame.draw.rect(screen, (100, 100, 250), (self.xPos - 8, self.yPos - 6, 16, 16))
		screen.blit(self.label, (self.labelXPosition, self.labelYPosition))
	
	def set(self, value):
		self.xPos = value * (self.xMax - self.xMin) + self.xMin
		self.function(value)

	def drag(self):	# activate the button
		self.xPos = pygame.mouse.get_pos()[0]
		if self.xPos > self.xMax:
			self.xPos = self.xMax
		elif self.xPos < self.xMin:
			self.xPos = self.xMin
		self.function(float(self.xPos - self.xMin) / float(self.xMax - self.xMin))

