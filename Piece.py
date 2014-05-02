class Piece(object):
	def __init__(self, x=0, y=0, player=0):
		self.x = x
		self.y = y
		self.hp = 100
		self.exp = 0
		self.level = 1
		self.unit_type = "piece"
		self.player = player

	def move(self, x, y):
		self.x += x
		self.y += y

	def setPos(self, x, y):
		self.x = x
		self.y = y

	def setImage(self, image):
		self.image = image

	def getImage(self):
		return self.image

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getHp(self):
		return self.hp

	def setHp(self, hp):
		self.hp = hp

	def getExp(self):
		return self.exp

	def setExp(self, exp):
		self.exp = exp

	def getLevel(self):
		return self.level

	def setLevel(self, lvl):
		self.level = lvl

	def getType(self):
		return self.unit_type

	def levelUp(self):
		self.level += 1
		self.hp = 100 + (self.level * 10)

	def getPlayer(self):
		return self.player
