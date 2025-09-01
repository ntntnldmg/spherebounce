from lib.blink import *
from lib.text import *
from lib.wall import *


class Footer:
	def __init__(self):
		self.score = Text("0000000",
			FOOTER_FONT,
			FOOTER_COLOR,
			FOOTER_SCORE_POSITION
		)
		self.time = Text("00:00:000",
			FOOTER_FONT,
			FOOTER_COLOR,
			FOOTER_TIME_POSITION
		)
		self.blink = Blink(FOOTER_BLINK_ONTIME, FOOTER_BLINK_OFFTIME)
	
	def update(self, score, t):
		self.score.new_label(str(score).zfill(FOOTER_SCORE_DIGITS))
		self.time.new_label(time_to_string(t))
	
	def update_gameover(self, dt):
		self.blink.update(dt)
	
	def render(self, screen, energytank, walltank, drawing):
		self.render_frame(screen)
		self.score.render(screen)
		self.time.render(screen)
		energytank.render(screen)
		walltank.render(screen, drawing)
	
	def render_gameover(self, screen):
		self.render_frame(screen)
		self.score.render(screen)	
		if self.blink.is_on():
			self.time.render(screen)

	def render_frame(self, screen):
		draw.rect(screen,
			FOOTER_BGCOLOR,
			(0, PLAY_AREA_SIZE + HEADER_HEIGHT, PLAY_AREA_SIZE, FOOTER_HEIGHT)
		)
		draw.line(screen,
			FOOTER_COLOR,
			(0, int(PLAY_AREA_SIZE + HEADER_HEIGHT + FOOTER_LINE/2)),
			(PLAY_AREA_SIZE, int(PLAY_AREA_SIZE + HEADER_HEIGHT + FOOTER_LINE/2)),
			FOOTER_LINE
		)

