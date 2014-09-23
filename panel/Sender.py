import json
import sys
import pygame
import random
from ButtonClass import button


pygame.init()
screen = pygame.display.set_mode((600,400))
b = button()
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit(None)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse = pygame.mouse.get_pos()
			if b.mask.collidepoint(mouse):
				b.press()
		elif event.type == pygame.MOUSEBUTTONUP:
			b.unpress()
	
	screen.fill((36,150,7))
	b.draw(screen)
	pygame.display.update()