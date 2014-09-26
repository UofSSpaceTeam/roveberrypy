import pygame
import random
import time

class paddle:

	def __init__(self, position, length, color):
		self.position = position
		self.length = length
		self.color = color

	def move(self, amount):
		self.position[1] += amount
		if self.position[1] + self.length / 2 > 400:
			self.position[1] = 400 - self.length / 2
		elif self.position[1] - self.length / 2 < 0:
			self.position[1] = self.length / 2

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.position[0] - 5,
			self.position[1] - self.length / 2, 10, self.length))

class ball:

	def __init__(self, diameter, color):
		self.position = [size[0] / 2, size[1] / 2]
		self.diameter = diameter
		self.color = color
		self.speed = [float(random.choice((-5, 5))), float(random.randint(-1, 1))]
	
	def update(self):
		self.position[0] += int(self.speed[0])
		self.position[1] += int(self.speed[1])
		self.edgeCollide()
		
	def paddleCollide(self, paddle):
		global size
		if (self.position[1] > paddle.position[1] - paddle.length / 2
		and self.position[1] < paddle.position[1] + paddle.length / 2):
			if paddle.position[0] > size[0] / 2: # right paddle
				if self.position[0] >= paddle.position[0] - 10:
					self.speed[0] *= -1.1
					self.speed[1] += random.choice((-1, 1))
				
			elif paddle.position[0] < size[0] / 2: # left paddle
				if self.position[0] <= paddle.position[0] + 10:
					self.speed[0] *= -1.1
					self.speed[1] += random.choice((-1, 1))

	def edgeCollide(self):
		global leftScore
		global rightScore
		global size
		if self.position[1] >= size[1] or self.position[1] <= 0:
			self.speed[1] *= -1
		if self.position[0] >= size[0]:
			leftScore += 1
			self.reset()
		elif self.position[0] <= 0:
			rightScore += 1
			self.reset()

	def reset(self):
		global size
		self.position = [size[0] / 2, size[1] / 2]
		self.speed = [float(random.choice((-5, 5))), float(random.randint(-1, 1))]
		
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, self.position, self.diameter / 2)

leftScore = 0
rightScore = 0
size = (800, 400)

pygame.init()
screen = pygame.display.set_mode(size)
font = pygame.font.Font(None, 36)
label = font.render("PING", 1, (255, 100, 100))

leftPaddle = paddle([20, 200], 70, (220, 0, 0))
rightPaddle = paddle([780, 200], 70, (0, 0, 200))
ball = ball(10, (80, 255, 80))

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()

	keys = pygame.key.get_pressed()
	if keys[pygame.K_q]:
		leftPaddle.move(-5)
	elif keys[pygame.K_a]:
		leftPaddle.move(5)
	
	if keys[pygame.K_o]:
		rightPaddle.move(-5)
	elif keys[pygame.K_l]:
		rightPaddle.move(5)

	ball.paddleCollide(leftPaddle)
	ball.paddleCollide(rightPaddle)
	ball.update()
	scoreboard = font.render(str(leftScore) + "  -  " + str(rightScore), 1, (0, 0, 0))

	screen.fill((80, 80, 80))
	screen.blit(label, (370, 10))
	screen.blit(scoreboard, (370, 40))
	leftPaddle.draw(screen)
	rightPaddle.draw(screen)
	ball.draw(screen)
	pygame.display.update()
	pygame.time.wait(10)

