#!/usr/bin/python

import copy
import pygame
from pygame.locals import *

# Population function lookup table
LUT = { 0: 0, 1: 1, 2: 1, 3: 2, 4: 1, 5: 2, 6: 2, 7: 3, 8: 1, 9: 2, 10: 2, 11: 3, 12: 2, 13: 3, 14: 3, 15: 4, 16: 1, 17: 2, 18: 2, 19: 3, 20: 2, 21: 3, 22: 3, 23: 4, 24: 2, 25: 3, 26: 3, 27: 4, 28: 3, 29: 4, 30: 4, 31: 5, 32: 1, 33: 2, 34: 2, 35: 3, 36: 2, 37: 3, 38: 3, 39: 4, 40: 2, 41: 3, 42: 3, 43: 4, 44: 3, 45: 4, 46: 4, 47: 5, 48: 2, 49: 3, 50: 3, 51: 4, 52: 3, 53: 4, 54: 4, 55: 5, 56: 3, 57: 4, 58: 4, 59: 5, 60: 4, 61: 5, 62: 5, 63: 6, 64: 1, 65: 2, 66: 2, 67: 3, 68: 2, 69: 3, 70: 3, 71: 4, 72: 2, 73: 3, 74: 3, 75: 4, 76: 3, 77: 4, 78: 4, 79: 5, 80: 2, 81: 3, 82: 3, 83: 4, 84: 3, 85: 4, 86: 4, 87: 5, 88: 3, 89: 4, 90: 4, 91: 5, 92: 4, 93: 5, 94: 5, 95: 6, 96: 2, 97: 3, 98: 3, 99: 4, 100: 3, 101: 4, 102: 4, 103: 5, 104: 3, 105: 4, 106: 4, 107: 5, 108: 4, 109: 5, 110: 5, 111: 6, 112: 3, 113: 4, 114: 4, 115: 5, 116: 4, 117: 5, 118: 5, 119: 6, 120: 4, 121: 5, 122: 5, 123: 6, 124: 5, 125: 6, 126: 6, 127: 7, 128: 1, 129: 2, 130: 2, 131: 3, 132: 2, 133: 3, 134: 3, 135: 4, 136: 2, 137: 3, 138: 3, 139: 4, 140: 3, 141: 4, 142: 4, 143: 5, 144: 2, 145: 3, 146: 3, 147: 4, 148: 3, 149: 4, 150: 4, 151: 5, 152: 3, 153: 4, 154: 4, 155: 5, 156: 4, 157: 5, 158: 5, 159: 6, 160: 2, 161: 3, 162: 3, 163: 4, 164: 3, 165: 4, 166: 4, 167: 5, 168: 3, 169: 4, 170: 4, 171: 5, 172: 4, 173: 5, 174: 5, 175: 6, 176: 3, 177: 4, 178: 4, 179: 5, 180: 4, 181: 5, 182: 5, 183: 6, 184: 4, 185: 5, 186: 5, 187: 6, 188: 5, 189: 6, 190: 6, 191: 7, 192: 2, 193: 3, 194: 3, 195: 4, 196: 3, 197: 4, 198: 4, 199: 5, 200: 3, 201: 4, 202: 4, 203: 5, 204: 4, 205: 5, 206: 5, 207: 6, 208: 3, 209: 4, 210: 4, 211: 5, 212: 4, 213: 5, 214: 5, 215: 6, 216: 4, 217: 5, 218: 5, 219: 6, 220: 5, 221: 6, 222: 6, 223: 7, 224: 3, 225: 4, 226: 4, 227: 5, 228: 4, 229: 5, 230: 5, 231: 6, 232: 4, 233: 5, 234: 5, 235: 6, 236: 5, 237: 6, 238: 6, 239: 7, 240: 4, 241: 5, 242: 5, 243: 6, 244: 5, 245: 6, 246: 6, 247: 7, 248: 5, 249: 6, 250: 6, 251: 7, 252: 6, 253: 7, 254: 7, 255: 8 }

def newCountLiveNeighbours(neighbours):
	return LUT[int(neighbours)]

# Colors
GRAY	= (127, 127, 127)
MAGENTA	= (255, 0, 255)
WHITE	= (255, 255, 255)
YELLOW	= (255, 255, 0)

# Constants
WORLD_SIZE = 100
CELL_SIZE = 5
VIEW_GRID = 0
WRAP_EDGES = True

# Spaceships
GLIDER = [
	[0, 1, 0],
	[0, 0, 1],
	[1, 1, 1],
]

# Oscillators
BLINKER = [
	[1, 1, 1],
]

# Methuselahs
R_PENTOMINO = [
	[0, 1, 1],
	[1, 1, 0],
	[0, 1, 0]
]

class Cell(object):
	alive = False

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return "(%d, %d)" % (self.x, self.y)

	def draw(self, screen):
		rect = [self.x * CELL_SIZE + 1, self.y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1]
		pygame.draw.rect(screen, YELLOW, rect)

	def isAlive(self):
		return self.alive

	def isDead(self):
		return not self.alive

def buildGrid(screen):
	# Fill grid background
	grid = pygame.Surface(screen.get_size())
	grid = grid.convert()
	grid.fill(GRAY)

	# Draw grid lines
	if VIEW_GRID:
		for i in range(0, WORLD_SIZE * CELL_SIZE + 1, CELL_SIZE):
			pygame.draw.line(grid, WHITE, (i, 0), (i, WORLD_SIZE * CELL_SIZE))
			pygame.draw.line(grid, WHITE, (0, i), (WORLD_SIZE * CELL_SIZE, i))

	return grid

def layCells():
	cells = []
	for i in range(WORLD_SIZE):
		row = []
		for j in range(WORLD_SIZE):
			row.append(Cell(j, i))
		cells.append(row)

	#for cell in GLIDER:
	#	cells[cell[0]][cell[1]].alive = True

	pattern = R_PENTOMINO
	pos = (WORLD_SIZE / 2 - 1, WORLD_SIZE / 2 - 1)

	for row in range(len(pattern)):
		for col in range(len(pattern[row])):
			if pattern[row][col]:
				cells[pos[1] + row][pos[0] + col].alive = True

	return cells

def countLiveNeighbours(cell, cells):
	total = 0
	for i in range(cell.y - 1, cell.y + 2):
		for j in range(cell.x - 1, cell.x + 2):
			if not (i == cell.y and j == cell.x):
				if WRAP_EDGES:
					if cells[i % WORLD_SIZE][j % WORLD_SIZE].isAlive():
						total += 1
				else:
					if 0 <= i and i < WORLD_SIZE and \
					   0 <= j and j < WORLD_SIZE:
						if cells[i][j].isAlive():
							total += 1
	return total

def main():
	# Initialise screen
	pygame.init()
	pygame.display.set_caption('Game of Life')
	screen = pygame.display.set_mode((WORLD_SIZE * CELL_SIZE + 1, WORLD_SIZE * CELL_SIZE + 1))
	clock = pygame.time.Clock()

	grid = buildGrid(screen)
	cells = layCells()

	# Event loop
	while 1:
		# -- Update --

		#clock.tick(10)

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
			elif event.type == QUIT:
				return

		# Updating cells
		newCells = copy.deepcopy(cells)

		for i, row in enumerate(cells):
			for j, cell in enumerate(row):
				liveNeighbours = countLiveNeighbours(cell, cells)
				if cell.isAlive():
					if liveNeighbours < 2 or \
					   liveNeighbours > 3:
						newCells[i][j].alive = False
				elif cell.isDead():
					if liveNeighbours == 3:
						newCells[i][j].alive = True

		cells = newCells

		# -- Render --

		# Draw grid
		screen.blit(grid, (0, 0))

		# Draw cells
		for row in cells:
			for cell in row:
				if cell.isAlive():
					cell.draw(screen)

		screen.blit(screen, (0, 0))
		pygame.display.flip()


if __name__ == '__main__': main()
