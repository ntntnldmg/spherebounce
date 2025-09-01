from lib.click import *
from lib.wall import *


class Walltank:
	def __init__(self):
		self.remaining = WALL_TANK_LENGTH
		self.walls = []
		self.is_drawing = False
	
	def draw(self, click):
		if self.remaining > MIN_WALL_LENGTH:
			if click.t > 0:
				if not self.is_drawing:
					self.walls.append(Wall())
					self.walls[-1].set_A(click.position)
					self.is_drawing = True
				else:
					self.walls[-1].set_B(click.now(), self.remaining)
			elif self.is_drawing:
				valid = self.walls[-1].finish()
				if valid:
					self.remaining -= self.walls[-1].length()
				else:
					self.walls.remove(self.walls[-1])
				self.is_drawing = False

	def delete(self, click):
		for wall in self.walls:
			if wall.circle_collision(click.position, CLICK_RADIUS) and wall.t >= 0:
				self.remaining += wall.length()
				self.walls.remove(wall)
	
	def update(self, dt):
		for wall in self.walls:
			wall.update(dt)
	
	def render_walls(self, screen):
		for wall in self.walls:
			wall.render(screen)

	def render(self, screen, drawing):
		draw.rect(screen,
			FOOTER_COLOR,
			(
				FOOTER_WALL_TANK_POSITION.x,
				FOOTER_WALL_TANK_POSITION.y - FOOTER_BAR_LINE/2 - FOOTER_TANK_LINE,
				WALL_TANK_LENGTH + FOOTER_TANK_LINE*2 + FOOTER_TANK_PADDING*2,
				FOOTER_BAR_LINE + FOOTER_TANK_LINE*2 + FOOTER_TANK_PADDING*2
			),
			FOOTER_TANK_LINE
		)
		draw.line(screen,
			WALL_COLORS[0],
			(
				FOOTER_WALL_TANK_POSITION.x + FOOTER_TANK_LINE + FOOTER_TANK_PADDING,
				FOOTER_WALL_TANK_POSITION.y
			),
			(
				FOOTER_WALL_TANK_POSITION.x + FOOTER_TANK_LINE + self.remaining,
				FOOTER_WALL_TANK_POSITION.y
			),
			FOOTER_BAR_LINE
		)
		draw.line(screen,
			WALL_DRAW_COLOR,
			(
				FOOTER_WALL_TANK_POSITION.x + FOOTER_TANK_LINE + FOOTER_TANK_PADDING \
				 + self.remaining - drawing,
				FOOTER_WALL_TANK_POSITION.y
			),
			(
				FOOTER_WALL_TANK_POSITION.x + FOOTER_TANK_LINE + self.remaining,
				FOOTER_WALL_TANK_POSITION.y
			),
			FOOTER_BAR_LINE
		)

