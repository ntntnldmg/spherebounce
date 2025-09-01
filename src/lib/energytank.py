from lib.helper import *


class Energytank:
	def __init__(self):
		self.remaining = MAX_ENERGY
		self.sfx_damage = Sound(PATH_DAMAGE_SFX)
		self.sfx_restore = Sound(PATH_RESTORE_SFX)
		self.unmute()
	
	def restore(self, sphere, value):
		is_restored = False
		if not sphere.is_safe and self.remaining < MAX_ENERGY:
			self.remaining = min(self.remaining+value, MAX_ENERGY)
			play_panned(self.sfx_restore, sphere.position.x)
			is_restored = True
		return is_restored
	
	def damage(self, sphere, value):
		if not sphere.is_safe:
			self.remaining -= value
			sphere.protect()
			play_panned(self.sfx_damage, sphere.position.x)
		return self.remaining <= 0
	
	def mute(self):
		self.sfx_damage.set_volume(0)
		self.sfx_restore.set_volume(0)
	
	def unmute(self):
		self.sfx_damage.set_volume(VOLUME_DAMAGE_SFX)
		self.sfx_restore.set_volume(VOLUME_RESTORE_SFX)

	def render(self, screen):
		draw.rect(screen,
			FOOTER_COLOR,
			(
				FOOTER_ENERGY_TANK_POSITION.x,
				FOOTER_ENERGY_TANK_POSITION.y - FOOTER_BAR_LINE/2 - FOOTER_TANK_LINE,
				ENERGY_TANK_LENGTH + FOOTER_TANK_LINE*2 + FOOTER_TANK_PADDING*2,
				FOOTER_BAR_LINE + FOOTER_TANK_LINE*2 + FOOTER_TANK_PADDING*2
			),
			FOOTER_TANK_LINE
		)
		draw.line(screen,
			ENERGY_COLOR,
			(
				FOOTER_ENERGY_TANK_POSITION.x + FOOTER_TANK_LINE + FOOTER_TANK_PADDING,
				FOOTER_ENERGY_TANK_POSITION.y
			),
			(
				FOOTER_ENERGY_TANK_POSITION.x + FOOTER_TANK_LINE + self.remaining,
				FOOTER_ENERGY_TANK_POSITION.y
			),
			FOOTER_BAR_LINE
		)
		
