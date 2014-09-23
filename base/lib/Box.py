	
import pygame
	
class Box:

	def __init__(self, label, rect):
		self.label = label
		self.rect = rect
		self.font = pygame.font.Font(None, 22)
		self.label = self.font.render(self.label, 1, (255, 255, 255))
		labelSize = self.label.get_size()
		self.labelXPosition = self.rect[0] + 0.5 * (self.rect[2] - labelSize[0])

	def draw(self, screen): # redraw the box and the label text
		pygame.draw.rect(screen, (100, 100, 100), self.rect)
		screen.blit(self.label, (self.labelXPosition, self.rect[1] + 5))

