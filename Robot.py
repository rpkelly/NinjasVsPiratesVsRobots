import Piece
import random

class Robot(Piece.Piece):
	def __init__(self, x, y, p):
		super(Robot, self)
		self.image = 'robot.png'
		#These represent the percent chance you will hit a type of unit
		#if you have equal health
		self.pirate_attack = 33
		self.ninja_attack = 67
		self.robot_attack = 50
		self.unit_type = "robot"
		self.movement = 1
		self.x = x
		self.y = y
		self.hp = 100
		self.exp = 0
		self.level = 1
		self.player = p
	
	def attack(self, enemy):
		ratio = self.getHp() / enemy.getHp()
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
