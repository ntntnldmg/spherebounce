from lib.helper import *


class Click:
	def __init__(self):
		self.t = 0
		self.position = Point(-1,-1)
	
	def now(self):
		return Point(mouse.get_pos()[0], mouse.get_pos()[1]-HEADER_HEIGHT)
	
	def check(self, dt):
		is_click = False
		if mouse.get_pressed()[0]:
			if self.t == 0:
				self.position = self.now()
			self.t += dt
		else:
			if 0 < self.t < MOUSE_HOLDTIME and \
			 p2p_dist(self.now(), self.position) < MOUSE_HOLDSIZE:
				is_click = True
			self.t = 0
		return is_click

