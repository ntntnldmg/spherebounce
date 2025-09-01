from lib.blink import *
from lib.helper import *


class Sphere:
	def __init__(self):
		self.position = Point(SPHERE_START_X, SPHERE_START_Y)
		self.angle = SPHERE_START_ANGLE
		self.velocity = 0
		self.acceleration = 0
		self.is_safe = False
		self.t_safe = 0
		self.blink = Blink(SPHERE_BLINK_ONTIME, SPHERE_BLINK_OFFTIME)
		self.sfx_bounce = Sound(PATH_BOUNCE_SFX)
		self.unmute()
	
	def update(self, dt):
		self.velocity += self.acceleration * dt
		if self.is_safe and self.t_safe < SPHERE_SAFE_TIME:
			self.t_safe += dt
			self.blink.update(dt)
		else:
			self.blink.reset()
			self.is_safe = False
	
	def protect(self):
		self.is_safe = True
		self.t_safe = 0
	
	def move(self, dt):
		self.position.x += dt * self.velocity * sin(self.angle)
		self.position.y -= dt * self.velocity * cos(self.angle)
	
	def bounce(self, wall_angle):
		if self.angle > wall_angle:
			wall_angle += pi
		self.angle = 2*wall_angle - self.angle
		play_panned(self.sfx_bounce, self.position.x)
	
	def mute(self):
		self.sfx_bounce.set_volume(0)
	
	def unmute(self):
		self.sfx_bounce.set_volume(VOLUME_BOUNCE_SFX)
	
	def score(self):
		return (self.velocity/BASE_VELOCITY)**VELOCITY_EXPONENT
	
	def render(self, screen):
		if self.blink.is_on():
			draw.circle(screen,
				SPHERE_COLOR,
				self.position.xy_plus(0, HEADER_HEIGHT),
				SPHERE_RADIUS
			)

