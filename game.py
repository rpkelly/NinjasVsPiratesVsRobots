from livewires import games, color
from Ninja import Ninja
from Pirate import Pirate
from Robot import Robot
from Board import Board
import pygame
import os

board = Board()
board.loadBack('level1.map')
board.setBoard('level1.units')
images = []
units = []
act = 0
inactive = 1

screen_w = pygame.display.Info().current_w
screen_h = pygame.display.Info().current_h
CONST_TILE_SIZE = 60
CONST_SIDE_PANELS = 150
games.init(screen_width = (board.getWidth() * CONST_TILE_SIZE + CONST_SIDE_PANELS * 2),
							screen_height = (board.getHeight() * CONST_TILE_SIZE),
							fps = 50)
print(os.getcwd())
explosion = games.load_sound('sounds/Flashbang-Kibblesbob-899170896.wav')
#games.init(screen_width = (board.getLength() * 60), screen_height = (1500), fps = 50)
mouse = games.Mouse()

class HighlightBox(games.Sprite):
	def __init__(self, x, y):
		"""
		Draw a rounded rect onto a surface
		and use that surface as the image for a sprite.
		The surface is 80% transparent, so it seems like the
		unit is highlighted.
		RoundedRect equations from 
		http://pygame.org/project-AAfilledRoundedRect-2349-.html
		"""
		radius = 0.4
		surf = pygame.Surface((CONST_TILE_SIZE,CONST_TILE_SIZE), pygame.SRCALPHA, 32)
		rect = pygame.Rect(0,0,CONST_TILE_SIZE,CONST_TILE_SIZE)
		color = pygame.Color(0,0,100,80)
		alpha = color.a
		color.a = 0
		pos = rect.topleft
		rect.topleft=0,0
		rectangle = pygame.Surface(rect.size, pygame.SRCALPHA, 32)

		circle = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA,32)
		pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
		circle = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

		radius = rectangle.blit(circle,(0,0))
		radius.bottomright = rect.bottomright
		rectangle.blit(circle, radius)
		radius.topright = rect.topright
		rectangle.blit(circle, radius)
		radius.bottomleft = rect.bottomleft
		rectangle.blit(circle,radius)

		rectangle.fill((0,0,0), rect.inflate(-radius.w,0))
		rectangle.fill((0,0,0), rect.inflate(0,-radius.h))

		rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
		rectangle.fill((255,255,255,alpha), special_flags=pygame.BLEND_RGBA_MIN)

		surf.blit(rectangle,pos)
	
		super(HighlightBox, self).__init__(image=surf, x = x, y = y)
	def moveComplete(self):
		self.destroy();

class Unit(games.Sprite):
	selected = False
	def __init__(self, unit):
		if(unit.getPlayer() == 0):
			super(Unit, self).__init__(image=games.load_image("img/f"+unit.getImage()),
										x = unit.getX() * CONST_TILE_SIZE + CONST_TILE_SIZE/2 + CONST_SIDE_PANELS,
										y = unit.getY() * CONST_TILE_SIZE + CONST_TILE_SIZE/2)
		else:
			super(Unit, self).__init__(image=games.load_image("img/"+unit.getImage()),
										x = unit.getX() * CONST_TILE_SIZE + CONST_TILE_SIZE/2 + CONST_SIDE_PANELS,
										y = unit.getY() * CONST_TILE_SIZE + CONST_TILE_SIZE/2)
		self.unit = unit
		self.enemy = None
		self.dest_x = None
		self.dest_y = None

	def update(self):
		global act
		global inactive

		if(self.enemy is not None):
			if(self.x == self.enemy.x - CONST_TILE_SIZE/2 or self.x == self.enemy.x + CONST_TILE_SIZE/2):
				self.dx = -self.dx
			if(self.y == self.enemy.y - CONST_TILE_SIZE/2 or self.y == self.enemy.y + CONST_TILE_SIZE/2):
				self.dy = -self.dy
			if(self.y == self.enemy.y + CONST_TILE_SIZE or self.y == self.enemy.y - CONST_TILE_SIZE):
				self.dy = 0
			if(self.x == self.enemy.x + CONST_TILE_SIZE or self.x == self.enemy.x - CONST_TILE_SIZE):
				self.dx = 0
			if(self.dx == self.dy):
				self.enemy = None
				if(self.unit.getPlayer() == act):
					temp = act
					act = inactive
					inactive = temp

		if(self.dest_x is not None and self.enemy is None):
			if(self.dx == 0 and self.dy == 0):
				x = self.dest_x - self.x
				y = self.dest_y - self.y
				if(x > 0):
					x = 2
				elif(x < 0):
					x = -2
				if(y > 0):
					y = 2
				elif(y < 0):
					y = -2
				self.dx = x
				self.dy = y
			if(self.x == self.dest_x and self.y == self.dest_y):
				self.dx = 0
				self.dy = 0
				self.dest_x = None
				self.dest_y = None
				if(self.unit.getPlayer() == act):
					temp = act
					act = inactive
					inactive = temp

		highlight = HighlightBox(x = self.x, y = self.y)
		if(mouse.x <(self.x + CONST_TILE_SIZE/2) and (mouse.x > self.x-CONST_TILE_SIZE/2) and mouse.y < self.y+CONST_TILE_SIZE/2 and mouse.y > self.y-CONST_TILE_SIZE/2 and mouse.is_pressed(0) and act == self.unit.getPlayer() and self.selected != True):
			for unit in units:
				if(unit.isSelected()):
					unit.notSelected()
			self.selected = True
			games.screen.add(highlight)

		if(self.selected == True):
			if(games.keyboard.is_pressed(games.K_w) or games.keyboard.is_pressed(games.K_UP)):
				if(self.y > CONST_TILE_SIZE/2):
					condition = self.checkSpot(self.x, self.y - CONST_TILE_SIZE)
					if(condition != 1):
						self.notSelected()
						self.y = self.y - CONST_TILE_SIZE
						if(condition == 0):
							self.dest_x = self.x
							self.dest_y = self.y
							self.y += CONST_TILE_SIZE
						if(condition == 2):
							for enemy in self.overlapping_sprites:
								self.y += CONST_TILE_SIZE
								self.enemy = enemy
								if(self.y > enemy.y and self.dy == 0):
									self.dy = -2
								self.battle(enemy)

			if(games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_LEFT)):
				if(self.x > CONST_TILE_SIZE/2 + CONST_SIDE_PANELS):
					condition = self.checkSpot(self.x - CONST_TILE_SIZE, self.y)
					if(condition != 1):
						self.notSelected()
						self.x = self.x - CONST_TILE_SIZE
						if(condition == 0):
							self.dest_x = self.x
							self.dest_y = self.y
							self.x += CONST_TILE_SIZE
						if(condition == 2):
							for enemy in self.overlapping_sprites:
								self.x += CONST_TILE_SIZE
								self.enemy = enemy
								if(self.x > enemy.x and self.dx == 0):
									self.dx = -2
								self.battle(enemy)
				
			if(games.keyboard.is_pressed(games.K_s) or games.keyboard.is_pressed(games.K_DOWN)):
				if(self.y < board.getHeight() * CONST_TILE_SIZE - CONST_TILE_SIZE/2):
					condition = self.checkSpot(self.x, self.y + 60)
					if(condition != 1):
						self.notSelected()
						self.y += CONST_TILE_SIZE
						if(condition == 0):
							self.dest_x = self.x
							self.dest_y = self.y
							self.y -= CONST_TILE_SIZE
						if(condition == 2):
							for enemy in self.overlapping_sprites:
								self.y -= CONST_TILE_SIZE
								self.enemy = enemy
								if(self.y < enemy.y and self.dy == 0):
									self.dy = 2
								self.battle(enemy)

			if(games.keyboard.is_pressed(games.K_d) or games.keyboard.is_pressed(games.K_RIGHT)):
				if(self.x < board.getWidth() * CONST_TILE_SIZE - CONST_TILE_SIZE/2 + CONST_SIDE_PANELS):
					condition = self.checkSpot(self.x + CONST_TILE_SIZE, self.y)
					if(condition != 1):
						self.notSelected()
						self.x += CONST_TILE_SIZE
						if(condition == 0):
							self.dest_x = self.x
							self.dest_y = self.y
							self.x -= CONST_TILE_SIZE
						if(condition == 2):
							for enemy in self.overlapping_sprites:
								self.x -= CONST_TILE_SIZE
								self.enemy = enemy
								if(self.x < enemy.x and self.dx == 0):
									self.dx = 2
								self.battle(enemy)

	def killed(self):
		units.remove(self)
		explosion.play()
		self.destroy()

	def isSelected(self):
		return self.selected

	def notSelected(self):
		for hl in list(set(self.overlapping_sprites).difference(set(units))):
			hl.moveComplete()
		self.selected = False
	
	def checkSpot(self, x, y):
		for piece in units:
			if(piece.get_x() == x and piece.get_y() == y):
				if(piece.unit.getPlayer() == self.unit.getPlayer()):
					return 1
				else:
					return 2
		return 0

	def battle(self, enemy):
		global act
		global inactive
		lvl = self.unit.getLevel()
		e_lvl = enemy.unit.getLevel()
		dmg_done = self.unit.attack(enemy.unit)
		if(dmg_done > 0): #Sweet Victory!
			games.screen.add(games.Message(value = -dmg_done,
											size = 20,
											color = color.dark_red,
											x = enemy.get_x(),
											y = enemy.get_y() - CONST_TILE_SIZE/2 + 10,
											lifetime = 30))
			if(lvl < self.unit.getLevel()):
				games.screen.add(games.Message(value = "Level Up!",
												size = 25,
												color = color.yellow,
												x = self.get_x(),
												y = self.get_y(),
												lifetime = 50))											
			if(enemy.unit.getHp() <= 0):
				self.dest_x = enemy.get_x()
				self.dest_y = enemy.get_y()
				enemy.killed()
				
		else: #Crushing Defeat!
			games.screen.add(games.Message(value = dmg_done,
											size = 20,
											color = color.dark_red,
											x = self.get_x(),
											y = self.get_y() - CONST_TILE_SIZE/2 + 10,
											lifetime = 30))
			if(e_lvl < enemy.unit.getLevel()):
				games.screen.add(games.Message(value = "Level Up!",
												size = 25,
												color = color.yellow,
												x = enemy.get_x(),
												y = enemy.get_y(),
												lifetime = 50))
			if(self.unit.getHp() <= 0):
				temp = act
				act = inactive
				inactive = temp
				self.killed()

class UnitInfo(games.Text):
	def __init__(self, unit, x, y):
		super(UnitInfo, self).__init__(value = unit.unit.getType(),
										size = 20,
										color = color.red,
										x = x,
										y = y)
		if(unit.unit.getPlayer() == 1):
			self.set_color(color.blue)
		self.unit = unit;

	def update(self):
		if(self.unit.isSelected()):
			self.set_color(color.purple)
		else:
			if(self.unit.unit.getPlayer() == 0):
				self.set_color(color.red)
			else:
				self.set_color(color.blue)
		self.set_value(self.unit.unit.getType() + " HP: " + str(self.unit.unit.getHp()) + " Lvl: "+str(self.unit.unit.getLevel()))
		if(self.unit.unit.getHp() <= 0):
			self.destroy()

class PlayerText(games.Text):
	def __init__(self, player):
		if(player == 0):
			super(PlayerText, self).__init__(value= "Player 1",
											size = 25,
											color = color.red,
											x = CONST_SIDE_PANELS/2,
											y = CONST_TILE_SIZE/2)
			self.main_color = color.red
		else:
			super(PlayerText, self).__init__(value= "Player 2",
											size = 25,
											color = color.blue,
											x = pygame.display.Info().current_w - CONST_SIDE_PANELS/2,
											y = CONST_TILE_SIZE/2)
			self.main_color = color.blue
		self.player = player

	def update(self):
		global act
		global inactive
		if(self.player == act):
			self.set_color(color.purple)
		else:
			self.set_color(self.main_color)

class TheWatcher(games.Sprite):
	def __init__(self):
		super(TheWatcher, self).__init__(image = games.load_image("img/pixel.png"), x = -50, y = -50)

	def update(self):
		player_1_units = 0
		player_2_units = 0
		for unit in units:
			if(unit.unit.getPlayer() == 0):
				player_1_units += 1
			else:
				player_2_units += 1
		if(player_1_units == 0):
			games.screen.add(games.Message(value = "Player 2 Wins!",
										size = 90,
										color = color.black,
										x = pygame.display.Info().current_w / 2,
										y = pygame.display.Info().current_h / 2,
										lifetime = 100,
										after_death = games.screen.quit))
		if(player_2_units == 0):
			games.screen.add(games.Message(value = "Player 1 Wins!",
										size = 90,
										color = color.black,
										x = pygame.display.Info().current_w / 2,
										y = pygame.display.Info().current_h / 2,
										lifetime = 100,
										after_death = games.screen.quit))


for image in board.getMap():
	images.append(games.load_image('img/' + image.strip(), transparent = False))


for unit in board.getPieces():
	units.append(Unit(unit))
	games.screen.add(units[len(units) - 1])
x_off = CONST_SIDE_PANELS
y_off = 0
background = pygame.display.get_surface()
for i in range(board.getHeight() * board.getWidth()):
	background.blit(images[i], (x_off, y_off))
	x_off += CONST_TILE_SIZE
	if((i+1) % board.getWidth() == 0 and i > 0):
		y_off += CONST_TILE_SIZE
		x_off = CONST_SIDE_PANELS

games.screen.background=background
games.screen.add(PlayerText(0))
games.screen.add(PlayerText(1))

player_1 = 0
player_2 = 0
for unit in units:
	if(unit.unit.getPlayer() == 0):
		games.screen.add(UnitInfo(unit = unit, x = CONST_SIDE_PANELS/2, y = CONST_TILE_SIZE + player_1 * 20))
		player_1 += 1
	else:
		games.screen.add(UnitInfo(unit = unit, x = pygame.display.Info().current_w - CONST_SIDE_PANELS/2, y = CONST_TILE_SIZE + player_2 * 20))
		player_2 += 1
games.screen.add(TheWatcher())
games.screen.mainloop()	
