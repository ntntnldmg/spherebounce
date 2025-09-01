from config import *


class Text:
	def __init__(self, label, font, color, position, duration=-1):
		self.font = font
		self.color = color
		self.position = position
		self.display = self.font.render(label, True, self.color)
		self.x = int(self.position.x - self.display.get_width()/2)
		self.y = int(self.position.y - self.display.get_height()/2)
		self.T = duration
		self.t = 0
	
	def new_label(self, label):
		self.display = self.font.render(label, True, self.color)
		self.x = int(self.position.x - self.display.get_width()/2)
		self.y = int(self.position.y - self.display.get_height()/2)
	
	def update(self, dt):
		is_expired = False
		self.t += dt
		if 0 <= self.T <= self.t:
			is_expired = True
		return is_expired
	
	def render(self, screen):
		screen.blit(self.display, (self.x, self.y + HEADER_HEIGHT))

	def get_width(self):
		return self.display.get_width()
	
	def get_height(self):
		return self.display.get_height()

