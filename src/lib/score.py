from lib.collectible import *
from lib.wall import *


class Score:
	def __init__(self):
		self.total = 0
		self.combo = 0
		self.streak = 0	#total bounces in between
		self.series = 0 #collected after single bounce
		self.last = Point(-1,-1) #last bounce position
		self.sfx_collect = Sound(PATH_COLLECT_SFX)
		self.sfx_expire = Sound(PATH_EXPIRE_SFX)
		self.unmute()
	
	def bounce(self, wall, position):
		if wall.level > 0:
			self.combo = self.combo*LEVEL_MULTIPLICATORS[wall.level] + wall.score()
			self.series = 0
		else:
			self.reset()
		self.last = position
	
	def collect(self, collectible, velocity):
		play_panned(self.sfx_collect, collectible.position.x)
		score = BASE_SCORE
		score += self.combo
		score += collectible.score()
		if not self.last == (-1,-1):
			score += p2p_dist(self.last, collectible.position) \
			 / sqrt(2*PLAY_AREA_SIZE**2) * RANGE_BONUS
		score = int(score * velocity * (1 + self.series*SERIES_MULTIPLICATOR) \
		 * (1 + self.streak*STREAK_MULTIPLICATOR))
		self.total += score
		self.streak += 1
		self.series += 1
		return score
	
	def expire(self, collectible):
		play_panned(self.sfx_expire, collectible.position.x)
		penalty = min(COLLECTIBLE_EXPIRATION_PENALTY, self.total)
		self.total -= penalty
		return -penalty
	
	def reset(self):
		self.combo = 0
		self.streak = 0
		self.series = 0
		self.last = Point(-1,-1)
		
	def mute(self):
		self.sfx_collect.set_volume(0)
		self.sfx_expire.set_volume(0)
	
	def unmute(self):
		self.sfx_collect.set_volume(VOLUME_COLLECT_SFX)
		self.sfx_expire.set_volume(VOLUME_EXPIRE_SFX)

