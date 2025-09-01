class Blink:
	def __init__(self, t_on, t_off):
		self.t_on = t_on
		self.t_off = t_off
		self.t = -1
	
	def update(self, dt):
		self.t += dt
	
	def reset(self):
		self.t = -1
	
	def is_on(self):
		return self.t == -1 or (self.t % (self.t_off+self.t_on)) >= self.t_off

