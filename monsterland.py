# -*- coding: utf-8 -*-
from random import randint

world = []
adventurer = {"x": 0, "y": 0, "hp": 10.0, "gold": 0}

def generateWorld(sizeX, sizeY):
	global world
	for y in range(0, sizeY):
		row = []
		for x in range(0, sizeX):
			#generate perimeter
			if x == 0 or y == 0 or x == (sizeX-1) or y == (sizeY-1):
				cell = 200
			else:
				cell = getRandomCell()
			row.append(cell)
		world.append(row)

def spawnAdventurer():
	adventurer["x"] = 1
	adventurer["y"] = 1

def getRandomCell():
	return randint(110, 200)
	
def updateAdventurer(dir):
	global adventurer
	dir = dir.lower()
	
	newx = adventurer["x"]
	newy = adventurer["y"]
	
	if dir == "n":
		newy -= 1
	elif dir == "s":
		newy += 1
	elif dir == "e":
		newx += 1
	elif dir == "w":
		newx -= 1
		
	if onMove(newx, newy):
		adventurer["x"] = newx
		adventurer["y"] = newy
	
	return adventurer["hp"] > 0
		 
def onMove(x, y):
	cell = getCell(x, y)
	
	if isRock(cell):
		adventurer["hp"] -= 0.5
		return False
	elif isWater(cell):
		adventurer["hp"] -= 0.1
	elif isSwamp(cell):
		adventurer["hp"] -= 0.5
	elif isGold(cell):
		adventurer["gold"] += 1
		setCell(x, y, getRandomCell())
	elif isSource(cell):
		adventurer["hp"] += 1
		setCell(x, y, getCell(x, y) -1)
	
	if isGround(cell):
		adventurer["hp"] -= 0.01
	
	return True

def getCell(x, y):
	return world[y][x]

def setCell(x, y, cell):
	world[y][x] = cell
	
def isRock(cell):
	return cell in range(182, 200 +1)
	
def isWater(cell):
	return cell in range(179, 181 +1)
	
def isGold(cell):
	return cell == 130

def isSwamp(cell):
	return cell in range(171, 178 +1)
	
def isSource(cell):
	return cell in range(112, 113 +1)
	
def isGround(cell):
	result = not isRock(cell)
	result &= not isWater(cell)
	result &= not isSwamp(cell)
	result &= not isSource(cell)
	return result
	
def drawWorld(showHidden):
	global world
	print "[hp: ", adventurer["hp"], "][gold: ", adventurer["gold"], "]"
	for y, row in enumerate(world):
		mapRow = ""
		for x, cell in enumerate(row):
			if adventurer["x"] == x and adventurer["y"] == y:
				mapRow += "@"
			elif isRock(cell):
				mapRow += "#"
			elif isWater(cell):
				mapRow += "~"
			elif isSwamp(cell):
				mapRow += "\""
			elif isSource(cell):
				mapRow += "&"
			# gold, show only if user can see hidden objects
			elif isGold(cell) and showHidden:
				mapRow += "G"
			# unknown, AKA ground
			else:
				mapRow += " "
		print mapRow
	
if __name__ == "__main__":
	generateWorld(40, 10)
	spawnAdventurer()

	userInput = ""
	print "Adventure begins!\nWrite a letter 'nswe' for move in that direction or 'exit' to leave game."
	print "Collect [G]old.\n Use [&] Sources to increase your HP.\nAvoid:\n[#] Rocks\n[~] Water\n[\"] Swamp"
	while True:	
		drawWorld(True)
		userInput = raw_input().lower()
		isAlive = updateAdventurer(userInput)
		if userInput == "exit" or not isAlive:
			break
	print "See ya!"



