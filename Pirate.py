import Piece
import random

class Pirate(Piece.Piece):
	def __init__(self, x, y, p):
		super(Pirate, self)
		self.image = 'pirate.png'
		#The percent chance you'll hit a unit at equal health
		self.pirate_attack = 50
		self.ninja_attack = 33
		self.robot_attack = 67
		self.unit_type = "pirate"
		self.movement = 2
		self.x = x
		self.y = y
		self.exp = 0
		self.level = 1
		self.hp = 100
		self.player = p
	
	def attack(self, enemy):
		ratio = self.getHp() /enemy.getHp()
		rand = random.randrange(100)
		if(enemy.getType() == "pirate"):
			attack = self.pirate_attack
		elif(enemy.getType() == "robot"):
			attack = self.robot_attack
		elif(enemy.getType() == "ninja"):
			attack = self.ninja_attack
		else:
			attack = 10
		if(rand < (ratio * attack)):
			n_hp = enemy.getHp()
			damage_dealt = self.getLevel() * random.randrange(10,20)
			enemy.setHp(n_hp - damage_dealt)
			self.setExp(self.getExp() + 20)
			if(self.getExp() % 100 == 0):
				self.levelUp()
			return damage_dealt
		else:
			n_lvl = enemy.getLevel()
			damage_recieved = n_lvl * random.randrange(5,10)
			self.setHp(self.getHp() - damage_recieved)
			enemy.setExp(enemy.getExp() + 10)
			if(enemy.getExp() % 100 == 0):
				enemy.levelUp()
			return -damage_recieved
	
