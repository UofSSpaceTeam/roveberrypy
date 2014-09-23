import pygame

class button:

	def __init__(self):
		self.name = "push me"
		self.position = (80,120,80,20)
		self.color = (150,36,7)
		self.font = pygame.font.Font(None,20)
		self.label = self.font.render(self.name, 1, (255,0,255))
		self.mask = None
		
		
	
	def draw(self,screen):
		self.mask = pygame.draw.rect(screen,self.color,self.position)
		screen.blit(self.label,(self.position[0], self.position[1]))
		
	def press(self):
		self.name = "ow"
		self.color = (255,255,255)
		self.label = self.font.render(self.name, 1, (0,255,0))
		
	def unpress(self):
		self.name = "push me"
		self.position = (80,120,80,20)
		self.color = (150,36,7)
		self.font = pygame.font.Font(None,20)
		self.label = self.font.render(self.name, 1, (255,0,255))
		self.mask = None