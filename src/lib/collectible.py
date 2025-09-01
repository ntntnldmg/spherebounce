from lib.blink import *
from lib.helper import *


class Collectible:
	def __init__(self, preview=0):
		self.position = Point(
			randint(COLLECTIBLE_PADDING, PLAY_AREA_SIZE-COLLECTIBLE_PADDING),
			randint(COLLECTIBLE_PADDING, PLAY_AREA_SIZE-COLLECTIBLE_PADDING)
		)
		self.radius = randint(MIN_COLLECTIBLE_RADIUS, MAX_COLLECTIBLE_RADIUS)
		self.t = 0
		self.blink = Blink(COLLECTIBLE_BLINK_ONTIME, COLLECTIBLE_BLINK_OFFTIME)
		self.preview = preview
	
	def update(self, dt):
		is_expired = False
		if not self.preview:
			self.t += dt
			if self.t >= COLLECTIBLE_SCREEN_TIME:
				is_expired = True
			elif self.t >= COLLECTIBLE_SCREEN_TIME-COLLECTIBLE_BLINK_TIME:
				self.blink.update(dt)
		return is_expired
			
	def score(self):
		bonus = 0
		if not (EDGE_SIZE <= self.position.x <= PLAY_AREA_SIZE-EDGE_SIZE) or \
		 not (EDGE_SIZE <= self.position.y <= PLAY_AREA_SIZE-EDGE_SIZE):
		 	bonus = COLLECTIBLE_EDGE_BONUS
		return (MAX_COLLECTIBLE_RADIUS-self.radius)*COLLECTIBLE_MULTIPLICATOR+bonus
	
	def render(self, screen):
		if self.blink.is_on():
			color = safe_access(COLLECTIBLE_PREVIEW_COLORS, self.preview) \
			 if self.preview else COLLECTIBLE_COLOR
			line = COLLECTIBLE_PREVIEW_LINE if self.preview else COLLECTIBLE_LINE
			draw.circle(screen,
				color,
				self.position.xy_plus(0, HEADER_HEIGHT),
				self.radius,
				line
			)

