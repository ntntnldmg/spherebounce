from lib.text import *


class Header:
	def __init__(self):
		self.text = [
			Text(
				HEADER_LABELS[i][0],
				HEADER_FONT,
				HEADER_COLOR,
				HEADER_LABEL_POSITIONS[i]
			) for i in range(len(HEADER_LABELS))
		]
		self.sfx_select = Sound(PATH_SELECT_SFX)
		self.unmute()
	
	def select(self, mouse_position):
		for i in range(len(self.text)):
			if self.text[i].x - HEADER_PADDING <= mouse_position.x \
			 <= self.text[i].x + self.text[i].get_width() + HEADER_PADDING and \
			 self.text[i].y - HEADER_PADDING <= mouse_position.y \
			 <= self.text[i].y + self.text[i].get_height() + HEADER_PADDING:
				self.sfx_select.play()
				return i
		return -1
	
	def switch_label(self, label_index, option_index):
		self.text[label_index].new_label(HEADER_LABELS[label_index][option_index])
	
	def mute(self):
		self.sfx_select.set_volume(0)
	
	def unmute(self):
		self.sfx_select.set_volume(VOLUME_SELECT_SFX)
	
	def render(self, screen):
		self.render_frame(screen)
		for t in self.text:
			t.render(screen)

	def render_gameover(self, screen):
		self.render_frame(screen)
		
	def render_frame(self, screen):
		draw.rect(screen,
			HEADER_BGCOLOR,
			(0, 0, PLAY_AREA_SIZE, HEADER_HEIGHT)
		)
		draw.line(screen,
			HEADER_COLOR,
			(0, int(HEADER_HEIGHT - HEADER_LINE - 1)),
			(PLAY_AREA_SIZE, int(HEADER_HEIGHT - HEADER_LINE - 1)),
			HEADER_LINE
		)

