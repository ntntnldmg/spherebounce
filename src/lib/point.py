class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def xy(self):
		return (int(self.x), int(self.y))

	def xy_plus(self, x, y):
		return (int(self.x+x), int(self.y+y))
