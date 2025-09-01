from config import *


class Obstacle:
	def __init__(self, preview=True):
		self.position = Point(
			randint(OBSTACLE_PADDING, PLAY_AREA_SIZE - OBSTACLE_PADDING),
			randint(OBSTACLE_PADDING, PLAY_AREA_SIZE - OBSTACLE_PADDING)
		)
		self.radius = randint(MIN_OBSTACLE_RADIUS, MAX_OBSTACLE_RADIUS)
		self.t = 0
		self.preview = preview
		self.color = OBSTACLE_PREVIEW_COLOR if self.preview else OBSTACLE_COLOR
		self.line = OBSTACLE_PREVIEW_LINE if self.preview else OBSTACLE_LINE
	
	def update(self, dt):
		is_expired = False
		self.t += dt
		if self.t >= OBSTACLE_SCREEN_TIME+OBSTACLE_PREVIEW_TIME:
			is_expired = True
		elif self.preview and self.t >= OBSTACLE_PREVIEW_TIME:
			self.preview = False
			self.color = OBSTACLE_COLOR
			self.line = OBSTACLE_LINE
		return is_expired
	
	def render(self, screen):
		draw.circle(screen,
			self.color,
			self.position.xy_plus(0, HEADER_HEIGHT),
			self.radius,
			self.line
		)

