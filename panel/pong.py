import json
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((1200,750))

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit(None)
	screen.fill((0,0,0))
	pygame.display.update()

