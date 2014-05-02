import Robot
import Pirate
import Ninja
import csv
from pygame.locals import *

class Board(object):
	def __init__(self):	
		self.pieces = []
		self.background = []
		self.height = 0
		self.width = 0

	#adds a piece to the board
	def addPiece(self, piece):
		self.pieces.add(piece)

	#loads csv file that describes background
	def loadBack(self, csv_file):
		csvfile = open(csv_file, newline='')
		mapreader = csv.reader(csvfile)
		for row in mapreader:
			self.width = len(row)
			self.height += 1
			self.background.extend(row)
		

	#loads csv file that describes units, inits all units
	def setBoard(self, csv_file):
		csvfile = open(csv_file, newline='')
		piecereader = csv.reader(csvfile)
		r = 0
		c = 0
		for row in piecereader:
			for item in row:
				if(item == 'r0' or item == 'R0'):
					self.pieces.append(Robot.Robot(r, c, 0))
				elif(item == 'n0' or item == 'N0'):
					self.pieces.append(Ninja.Ninja(r, c, 0))
				elif(item == 'p0' or item == 'P0'):
					self.pieces.append(Pirate.Pirate(r, c, 0))
				elif(item == 'r1' or item == 'R1'):
					self.pieces.append(Robot.Robot(r, c, 1))
				elif(item == 'n1' or item == 'N1'):
					self.pieces.append(Ninja.Ninja(r, c, 1))
				elif(item == 'p1' or item == 'P1'):
					self.pieces.append(Pirate.Pirate(r, c, 1))
				r += 1
			c += 1
			r = 0

	def getPieces(self):
		return self.pieces

	def setPieces(self, pieces):
		self.pieces = pieces

	def getMap(self):
		return self.background

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width


