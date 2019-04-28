class Player:
	def __init__(self, x, y, power=0):
		self.x = x
		self.y = y
		self.power = power
		self.boll = 1
		self.lucky = 5
		self.allMonsters = 0
		self.bollHere = 0
		self.enemy = {}
