from lib.helper import *
from lib.point import *


class Wall:
	def __init__(self):
		self.A = Point(-1,-1)
		self.B = Point(-1,-1)
		self.angle = -1
		self.t = -1
		self.level = -1
		self.color = WALL_DRAW_COLOR
		self.valid = False
	
	def length(self):
		if 0 <= self.A.y < PLAY_AREA_SIZE and 0 <= self.B.y < PLAY_AREA_SIZE:
			return p2p_dist(self.A, self.B)
		elif not 0 <= self.A.y < PLAY_AREA_SIZE and not 0 <= self.B.y < PLAY_AREA_SIZE:
			return 0
		else:
			dx = self.B.x - self.A.x
			dy = self.B.y - self.A.y
			if dx == 0:
				if self.A.y < 0:
					self.A.y = 0
				elif self.A.y >= PLAY_AREA_SIZE:
					self.A.y = PLAY_AREA_SIZE-1
				if self.B.y < 0:
					self.B.y = 0
				elif self.B.y >= PLAY_AREA_SIZE:
					self.B.y = PLAY_AREA_SIZE-1
			else:
				m = dy/dx
				b = self.A.y - m*self.A.x
				if self.A.y < 0:
					self.A.x = (0-b)/m
					self.A.y = 0
				elif self.A.y >= PLAY_AREA_SIZE:
					self.A.x = (PLAY_AREA_SIZE-1-b)/m
					self.A.y = PLAY_AREA_SIZE-1
				if self.B.y < 0:
					self.B.x = (0-b)/m
					self.B.y = 0
				elif self.B.y >= PLAY_AREA_SIZE:
					self.B.x = (PLAY_AREA_SIZE-1-b)/m
					self.B.y = PLAY_AREA_SIZE-1
			return p2p_dist(self.A, self.B)
	
	def set_A(self, A):
		self.A = A
	
	def set_B(self, B, max_length):
		self.B = B
		self.valid = MIN_WALL_LENGTH <= self.length() <= max_length
		self.color = WALL_DRAW_COLOR if self.valid else WALL_INVALID_COLOR
	
	def min_y(self):
		return min(self.A.y, self.B.y)
	
	def max_y(self):
		return max(self.A.y, self.B.y)
	
	def sort_nodes(self):
		if self.B.x < self.A.x:
			(self.A.x, self.A.y, self.B.x, self.B.y) = \
			 (self.B.x, self.B.y, self.A.x, self.A.y)
	
	def finish(self):
		if self.valid:
			self.sort_nodes()
			dx = self.B.x - self.A.x
			if dx == 0:
				self.angle = pi
			else:
				dy = self.B.y - self.A.y
				self.angle = pi/2 + atan(dy/dx)
			self.t = 0
			self.level = 0
			self.color = WALL_COLORS[0]
		return self.valid
	
	def update(self, dt):
		if self.t >= 0:
			self.t += dt
			if self.level < len(WALL_TIMES)-1 and self.t >= WALL_TIMES[self.level+1]:
				self.level += 1
				self.color = WALL_COLORS[self.level]
	
	def circle_collision(self, position, radius):
		if self.A.x-radius <= position.x <= self.B.x+radius and \
		 self.min_y()-radius <= position.y <= self.max_y()+radius:
			dx = self.B.x - self.A.x
			dy = self.B.y - self.A.y
			if dx == 0 or dy == 0:
				return True
			else:
				m1 = dy/dx
				b1 = self.A.y - m1*self.A.x
				m2 = -dx/dy
				b2 = position.y - m2*position.x
				ix = (b2-b1) / (m1-m2)
				if ix < self.A.x:
					return p2p_dist(position, self.A) < radius
				elif ix > self.B.x:
					return p2p_dist(position, self.B) < radius
				else:
					return p2p_dist(position, Point(ix,m1*ix+b1)) < radius
		else:
			return False
	
	def score(self):
		return LEVEL_SCORES[self.level] * \
		 (1 + (PRECISE_MULTIPLICATOR-1) * (self.length()<=PRECISE_SIZE))
	
	def render(self, screen):
		if self.B.x >= 0:
			draw.line(screen,
				self.color,
				(self.A.x, self.A.y + HEADER_HEIGHT),
				(self.B.x, self.B.y + HEADER_HEIGHT),
				WALL_LINE
			)

