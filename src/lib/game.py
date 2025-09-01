from lib.click import *
from lib.collectible import *
from lib.energytank import *
from lib.footer import *
from lib.header import *
from lib.obstacle import *
from lib.score import *
from lib.sphere import *
from lib.walltank import *


class Game:
	def __init__(self):
		display.init()
		display.set_caption(GAME_TITLE)
		self.screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.header = Header()
		self.footer = Footer()
		self.txts = []
		self.txt_paused = Text(
			PAUSED_OVERLAY_LABEL,
			PAUSED_OVERLAY_FONT,
			PAUSED_OVERLAY_COLOR,
			PAUSED_OVERLAY_POSITION
		)
		self.txt_gameover = Text(
			GAMEOVER_OVERLAY_LABEL,
			GAMEOVER_OVERLAY_FONT,
			GAMEOVER_OVERLAY_COLOR,
			GAMEOVER_OVERLAY_POSITION
		)
		self.sfx_bgm = Sound(PATH_BGM)
		self.bgm_volume = VOLUME_BGM
		self.sfx_bgm.set_volume(self.bgm_volume)
		self.sphere = Sphere()
		self.collectibles = []
		self.obstacles = []
		self.closecalls = []
		self.energytank = Energytank()
		self.walltank = Walltank()
		self.score = Score()
		self.stage = 0
		self.over = False
		self.out = False
		self.time = 0
		self.starttime = 0
		self.pausetime = -1
		self.stagetime = 0
		self.click = Click()
	
	def start(self):
		self.time = get_ticks()
		self.starttime = self.time
		self.stagetime = self.time
		self.next_stage()
		self.sfx_bgm.play(-1)
		self.loop()
		self.sfx_bgm.stop()
		self.ending()
		quit()
	
	def check_gameover(self):
		self.over = self.energytank.remaining <= 0
		for e in event.get():
			if e.type is QUIT:
				self.over = True
				self.out = True
	
	def mouse_input(self, dt):
		if self.click.check(dt):
			if self.pausetime == -1:
				self.walltank.delete(self.click)
			self.menu_input()
		if self.pausetime == -1:
			self.walltank.draw(self.click)
	
	def pause(self):
		self.pausetime = get_ticks()
		self.txts.append(self.txt_paused)
		self.bgm_volume = VOLUME_BGM_PAUSED
		if self.sfx_bgm.get_volume() > 0:
			self.sfx_bgm.set_volume(self.bgm_volume)
		self.header.switch_label(1, 1)
	
	def unpause(self):
		self.starttime += get_ticks() - self.pausetime
		self.pausetime = -1
		self.txts.remove(self.txt_paused)
		self.bgm_volume = VOLUME_BGM
		if self.sfx_bgm.get_volume() > 0:
			self.sfx_bgm.set_volume(self.bgm_volume)
		self.header.switch_label(1, 0)
	
	def mute(self):
		self.sfx_bgm.set_volume(0)
		self.sphere.mute()
		self.energytank.mute()
		self.score.mute()
		self.header.mute()
		self.header.switch_label(0, 1)
	
	def unmute(self):
		self.sfx_bgm.set_volume(self.bgm_volume)
		self.sphere.unmute()
		self.energytank.unmute()
		self.score.unmute()
		self.header.unmute()
		self.header.switch_label(0, 0)
	
	def menu_input(self):
		selection = self.header.select(self.click.position)
		if selection == 0:
			if self.sfx_bgm.get_volume() == 0:
				self.unmute()
			else:
				self.mute()
		elif selection == 1:
			if self.pausetime == -1:
				self.pause()
			else:
				self.unpause()
		elif selection == 2:
			self.over = True
	
	def any_collision(self, position, radius):
		is_collision = False
		for collectible in self.collectibles:
			if p2p_dist(position, collectible.position) \
			 < radius + collectible.radius:
				is_collision = True
		for obstacle in self.obstacles:
			if p2p_dist(position, obstacle.position) \
			 < radius + obstacle.radius:
				is_collision = True
		return is_collision
	
	def add_collectible(self, preview=0):
		while True:
			new = Collectible(preview)
			if not self.any_collision(new.position, new.radius):
				self.collectibles.append(new)
				break
	
	def add_obstacle(self):
		while True:
			new = Obstacle()
			if not self.any_collision(new.position, new.radius):
				self.obstacles.append(new)
				break
	
	def replace_collectible(self, collectible):
		for i in range(len(self.collectibles)):
			self.collectibles[i].preview = max(0, self.collectibles[i].preview-1)
		self.add_collectible(COLLECTIBLE_PREVIEW_AMOUNT)
		self.collectibles.remove(collectible)
	
	def replace_obstacle(self, obstacle):
		self.obstacles.remove(obstacle)
		self.add_obstacle()
	
	def collision_collectible(self):
		for collectible in self.collectibles:
			if not collectible.preview and \
			 p2p_dist(self.sphere.position, collectible.position) \
			 < SPHERE_RADIUS + collectible.radius:
				self.show_change(self.score.collect(collectible, self.sphere.score()), \
				 collectible.position)
				self.replace_collectible(collectible)
	
	def collision_obstacle(self):
		for obstacle in self.obstacles:
			if not obstacle.preview and \
			 p2p_dist(self.sphere.position, obstacle.position) \
			 < SPHERE_RADIUS + obstacle.radius:
				self.score.reset()
				self.replace_obstacle(obstacle)
				return self.energytank.damage(self.sphere, OBSTACLE_DAMAGE)
		return 0
	
	def close_call(self):
		for obstacle in self.obstacles:
			if not obstacle.preview:
				if obstacle not in self.closecalls and \
				 p2p_dist(self.sphere.position, obstacle.position) \
				 <= SPHERE_RADIUS + obstacle.radius + CLOSECALL_SIZE:
					self.closecalls.append(obstacle)
				elif obstacle in self.closecalls and \
				 p2p_dist(self.sphere.position, obstacle.position) \
				 > SPHERE_RADIUS + obstacle.radius + CLOSECALL_SIZE:
					self.closecalls.remove(obstacle)
					if self.energytank.restore(self.sphere, CLOSECALL_RESTORE):
						self.replace_obstacle(obstacle)
						self.txts.append(
							Text(CLOSECALL_OVERLAY_LABEL,
								CLOSECALL_OVERLAY_FONT,
								CLOSECALL_OVERLAY_COLOR,
								obstacle.position,
								CLOSECALL_OVERLAY_TIME
							)
						)
	
	def collision_edge(self):
		impact = 1
		if self.sphere.position.x <= SPHERE_RADIUS:
			self.sphere.bounce(0)
			self.sphere.position.x = SPHERE_RADIUS+impact
		elif self.sphere.position.x >= PLAY_AREA_SIZE-SPHERE_RADIUS:
			self.sphere.bounce(0)
			self.sphere.position.x = PLAY_AREA_SIZE-SPHERE_RADIUS-impact
		elif self.sphere.position.y <= SPHERE_RADIUS:
			self.sphere.bounce(pi/2)
			self.sphere.position.y = SPHERE_RADIUS+impact
		elif self.sphere.position.y >= PLAY_AREA_SIZE-SPHERE_RADIUS:
			self.sphere.bounce(pi/2)
			self.sphere.position.y = PLAY_AREA_SIZE-SPHERE_RADIUS-impact
		else:
			return False
		self.score.reset()
		return self.energytank.damage(self.sphere, EDGE_DAMAGE)
	
	def collision_wall(self):
		for wall in self.walltank.walls:
			if wall.t >= 0 and \
			 wall.circle_collision(self.sphere.position, SPHERE_RADIUS):
				self.score.bounce(wall, self.sphere.position)
				self.sphere.bounce(wall.angle)
				self.walltank.remaining += wall.length()
				self.walltank.walls.remove(wall)
	
	def update_elements(self, dt):
		self.sphere.update(dt)
		self.sphere.move(dt)
		for collectible in self.collectibles:
			if collectible.update(dt):
				self.show_change(self.score.expire(collectible), collectible.position)
				self.replace_collectible(collectible)
		for obstacle in self.obstacles:
			if obstacle.update(dt):
				self.replace_obstacle(obstacle)
		self.walltank.update(dt)
		for txt in self.txts:
			if txt.update(dt):
				self.txts.remove(txt)
	
	def update_display(self, dt):
		self.screen.fill(PLAY_AREA_BGCOLOR)
		draw.rect(self.screen,
			EDGE_COLOR,
			(0, HEADER_HEIGHT, PLAY_AREA_SIZE, PLAY_AREA_SIZE),
			EDGE_LINE
		)
		for collectible in self.collectibles:
			collectible.render(self.screen)
		for obstacle in self.obstacles:
			obstacle.render(self.screen)
		self.sphere.render(self.screen)
		self.walltank.render_walls(self.screen)
		for txt in self.txts:
			txt.render(self.screen)
		self.header.render(self.screen)
		if len(self.walltank.walls) > 0 and self.walltank.walls[-1].t == -1 and \
		 self.walltank.walls[-1].valid:
			self.footer.render(self.screen,
				self.energytank,
				self.walltank,
				self.walltank.walls[-1].length()
			)
		else:
			self.footer.render(self.screen,
				self.energytank,
				self.walltank,
				0
			)
		display.flip()
	
	def ending(self):
		self.sphere.is_safe = True
		self.sphere.blink.t = -1
		while not self.out:
			for e in event.get():
				if e.type is QUIT:
					self.out = True
			self.collision_edge()
			dt = get_ticks()-self.time
			self.time = get_ticks()
			self.sphere.move(dt)
			self.footer.update_gameover(dt)
			self.screen.fill(PLAY_AREA_BGCOLOR)
			self.sphere.render(self.screen)
			self.txt_gameover.render(self.screen)
			self.header.render_gameover(self.screen)
			self.footer.render_gameover(self.screen)
			display.flip()
	
	def next_stage(self):
		self.stage += 1
		self.sphere.velocity = START_VELOCITIES[self.stage]
		self.sphere.accelation = ACCELERATIONS[self.stage]
		self.collectibles.clear()
		self.obstacles.clear()
		self.closecalls.clear()
		for i in range(STAGE_COLLECTIBLE_AMOUNTS[self.stage]):
			self.add_collectible()
		for i in range(COLLECTIBLE_PREVIEW_AMOUNT):
			self.add_collectible(i+1)
		for i in range(STAGE_OBSTACLE_AMOUNTS[self.stage]):
			self.add_obstacle()
		self.txts.append(
			Text(STAGE_OVERLAY_LABEL + str(self.stage),
				STAGE_OVERLAY_FONT,
				STAGE_OVERLAY_COLOR,
				STAGE_OVERLAY_POSITION,
				STAGE_OVERLAY_TIME
			)
		)
	
	def loop(self):
		while not self.over:
			self.check_gameover()
			if self.pausetime == -1:
				self.collision_edge()
				self.collision_obstacle()
				self.collision_collectible()
				self.collision_wall()
				self.close_call()
			dt = get_ticks()-self.time
			self.time = get_ticks()
			if self.stage <= len(STAGE_DURATIONS) and \
			 self.time >= self.stagetime + STAGE_DURATIONS[self.stage-1]:
				self.next_stage()
				self.stagetime = self.time
			self.mouse_input(dt)
			if self.pausetime == -1:
				self.update_elements(dt)
				self.footer.update(self.score.total, self.time-self.starttime)
			self.update_display(dt)
	
	def show_change(self, dscore, position):
		self.txts.append(
			Text("+" + str(dscore),
				ADD_SCORE_OVERLAY_FONT,
				ADD_SCORE_OVERLAY_COLOR,
				position,
				ADD_SCORE_OVERLAY_TIME
			) if dscore >= 0
			else Text(str(dscore),
				SUBTRACT_SCORE_OVERLAY_FONT,
				SUBTRACT_SCORE_OVERLAY_COLOR,
				position,
				SUBTRACT_SCORE_OVERLAY_TIME
			)
		)

