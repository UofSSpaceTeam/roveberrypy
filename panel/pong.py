import json
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((1200,750))

def background(self):
	self.name = "PONG"
	self.position = (50, 50)
	self.color = (255,255,255)
	self.font = pygame.font.Font(None, 72)
	self.label = self.font.render(self.name, 1, (255,255,255))
	self.mask = None
	
def draw(self):
	self.mask = pygame.draw.rect(screen,self.color,self.position)
	screen.blit(self.label,(self.position[0], self.position[1]))
	
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit(None)
	screen.fill((0,0,0))
	self.draw()
	pygame.display.update()

