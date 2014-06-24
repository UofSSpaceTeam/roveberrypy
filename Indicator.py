import pygame

	# class definition
	
class Indicator:
	def __init__(self, function, (args), label, position):
		self.function = function
		self.args = args
		self.label = label
		self.position = position
		self.active = False
		self.font = pygame.font.Font(None, 20)
		self.label = self.font.render(self.label, 1, (255, 255, 255))

	def getColor(self):	# returns the color of the button (3-tuple)
		if self.active:
			return (0, 255, 0)
		else:
			return (255, 0, 0)

	def draw(self, screen): # redraw the button with centered label
		pygame.draw.rect(screen, (10, 10, 10), (self.position[0] - 2, self.position[1] - 2, 18, 18))
		pygame.draw.rect(screen, self.getColor(), (self.position[0], self.position[1], 14, 14))
		screen.blit(self.label, (self.position[0] + 20, self.position[1] + 1))

	def refresh(self):	# call boolean function to determine state
		if self.function(self.args):
			self.active = True
		else:
			self.active = False

