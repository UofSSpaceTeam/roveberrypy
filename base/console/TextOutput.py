import pygame

class TextOutput():
	
	def __init__(self, label, fontSize, fontcolor, rect, maxLines):
		self.label = label
		self.fontSize = fontSize
		self.fontcolor = fontcolor
		self.rect = rect
		self.maxLines = maxLines
		self.innerRect = (rect[0] + 2, rect[1] + 18, rect[2] - 4, rect[3] - 20)
		self.hOffset = self.innerRect[0] + 5
		self.vOffset = self.innerRect[1] + self.fontSize / 5
		self.labelFont = pygame.font.Font(None, 22)
		self.consoleFont = pygame.font.Font(None, self.fontSize)
		self.list = []
		self.lastMessage = None
	
	def write(self, text):
		if text == "\n" or text == self.lastMessage or text == None or text == "None":
			return
		elif(len(text) > 60): # split long messages
			self.write(text[:60])
			self.write(text[60:])
		else:
			self.list.append(text)
			if(len(self.list) > self.maxLines):
				self.list.remove(self.list[0])
		self.lastMessage = text

	def draw(self, screen):
		pygame.draw.rect(screen, (100, 100, 100), self.rect)
		pygame.draw.rect(screen, (0, 0, 0), self.innerRect)
		label = self.labelFont.render(self.label, 1, (255, 255, 255))
		labelSize = label.get_size()
		labelXPosition = self.rect[0] + 0.5 * (self.rect[2] - labelSize[0])
		screen.blit(label, (labelXPosition, self.rect[1] + 1))
		lineIndex = 0
		for msg in self.list:
			msg = self.consoleFont.render(msg, 1, self.fontcolor)
			screen.blit(msg, (self.hOffset, self.vOffset + (lineIndex * self.fontSize * 0.7)))
			lineIndex = lineIndex + 1

