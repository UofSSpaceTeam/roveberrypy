	
import pygame
	
class Button:

	def __init__(self, function, (args), label, rect, defaultColor, selectedColor):
		self.function = function
		self.args = args
		self.label = label
		self.rect = rect
		self.defaultColor = defaultColor
		self.selectedColor = selectedColor
		self.font = pygame.font.Font(None, 20)
		self.label = self.font.render(self.label, 1, (0, 0, 0))
		labelSize = self.label.get_size()
		self.labelXPosition = self.rect[0] + 0.5 * (self.rect[2] - labelSize[0])
		self.labelYPosition = self.rect[1] + 0.5 * (self.rect[3] - labelSize[1])
		self.selected = False
		self.obj = None
		

	def getColor(self):	# returns the color of the button (3-tuple)
		if self.selected:
			return self.selectedColor
		else:
			return self.defaultColor

	def draw(self, screen): # redraw the button with centered label
		self.obj = pygame.draw.rect(screen, self.getColor(), self.rect)
		screen.blit(self.label, (self.labelXPosition, self.labelYPosition))

	def press(self):	# activate the button
		self.function(self.args)

