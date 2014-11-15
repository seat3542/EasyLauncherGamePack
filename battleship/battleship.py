#!/usr/bin/python3
#############################################################
# File Name:   battleship.py
# Author:	   A.S. ("LittleFireDragon")
# Date:		   11/12/14
# Purpose:	   The classic game Battleship, set not in WWII
#			   but in the age of wooden ships, in python.
#############################################################
from tkinter import *
from random import randint
from random import choice

class Battleship():
	""" Single player battleship against the computer. """
	
	# INITIAL GAME CONSTRUCTION
	def __init__(self):
		""" Set up everything for the first time. """
		self.root = Tk()
		self.root.title("Battleship")
		self.__message = StringVar()
		self.__images = {}
		self.setupVariables()
		self.loadImages()
		self.buildGUI()
		self.setBoundaries()
		self.newGame()
		
	def buildGUI(self):
		""" Create the tkinter UI. Initially bind map functions. """
		# Build basic tkinter layout
		self.contentFrame = Frame(self.root)
		self.contentFrame.grid(row=0, column=0)
		self.topBar = Frame(self.contentFrame, border=2, relief=RAISED,
							pady=3)
		self.topBar.grid(row=0, column=0, columnspan=23, sticky=E+W)
		self.newGameButton = Button(self.topBar, text="New Game",
									command=self.newGame)
		self.newGameButton.grid(row=0, column=0)
		self.messageBox = Label(self.topBar, height=2,
								textvariable=self.__message)
		self.messageBox.grid(row=1, column=0, sticky=W+E)
		# weights for spacing
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_rowconfigure(0, weight=1)
		self.contentFrame.grid_columnconfigure(0, weight=1)
		self.contentFrame.grid_rowconfigure(0, weight=1)
		self.contentFrame.grid_rowconfigure(13, pad=3)
		self.topBar.grid_columnconfigure(0, weight=1)
		self.topBar.grid_rowconfigure(0, weight=1)
		# Map grid labels
		self.leftLabels = []
		self.rightLabels = []
		self.leftBar = Frame(self.contentFrame, pady=4)
		self.leftBar.grid (column=0, row=2, rowspan=10, sticky=N+S)
		for row in range (0, 10):
			self.leftBar.grid_rowconfigure(row, weight=1)
		self.rightBar = Frame(self.contentFrame, pady=4)
		self.rightBar.grid (column=22, row=2, rowspan=10, sticky=N+S)
		for row in range (0, 10):
			self.rightBar.grid_rowconfigure(row, weight=1)
		self.topLeftBar = Frame(self.contentFrame, padx=4)
		self.topLeftBar.grid (column=1, row=1, columnspan=10, 
							  sticky=W+E, pady=(5,0))
		for column in range (0, 9):
			self.topLeftBar.grid_columnconfigure(column, weight=1)
		self.topRightBar = Frame(self.contentFrame, padx=4)
		self.topRightBar.grid (column=12, row=1, columnspan=10, 
							   sticky=W+E, pady=(5,0))
		for column in range (0, 9):
			self.topRightBar.grid_columnconfigure(column, weight=1)
		for i in range(0, 10):
			self.leftLabels.append(Label(self.topLeftBar, text=i+1))
			self.rightLabels.append(Label(self.topRightBar, text=i+1))
			self.leftLabels[i].grid(row=0, column=(i))
			self.rightLabels[i].grid(row=0, column=(i))
		for i in range(10, 20):
			self.leftLabels.append(Label(self.leftBar, 
										 text=chr(55+i)))
			self.rightLabels.append(Label(self.rightBar, 
										  text=chr(55+i)))
			self.leftLabels[i].grid(row=(i-10), column=0)
			self.rightLabels[i].grid(row=(i-10), column=0)
		# Maps
		self.ocean = Canvas(self.contentFrame, height=241, width=241,
							relief=SUNKEN, border=2)
		self.ocean.grid (row=2, column=1, rowspan=10, columnspan=10)
		self.parchment = Canvas(self.contentFrame, height=241, 
								width=241, relief=SUNKEN, border=2)
		self.parchment.grid(row=2, column=12, rowspan=10, columnspan=10)
		# Map Bindings
		self.parchment.bind("<Button-1>", self.parchmentLClick)
		self.parchment.bind("<Motion>", self.mouseOverParchment)
		self.parchment.bind("<Leave>", self.hideGhostX)
		self.ocean.bind("<Button-1>", self.oceanLClick)
		self.ocean.bind("<Motion>", self.mouseOverOcean)
		self.ocean.bind("<Leave>", self.hideGhostShip)
		self.ocean.bind("<Button-3>", self.rotateGhostShip)
		# Ship quickview area
		self.shipsLabel = Label(self.contentFrame, text="Your\nShips")
		self.shipsLabel.grid(row=12, column=11)
		self.shipDisplayBar = Frame(self.contentFrame, pady=2)
		self.shipDisplayBar.grid (column=1, columnspan=21,
								  row=13, sticky=E+W)
		self.shipDisplayBar.grid_columnconfigure(0, weight=1)
		self.shipDisplayBar.grid_columnconfigure(1, weight=1)
		self.shipDisplayBar.grid_columnconfigure(2, weight=1)
		self.shipDisplayBar.grid_columnconfigure(3, weight=1)
		self.shipDisplayBar.grid_columnconfigure(4, weight=1)
		# Ship quickview canvases
		self.longshipBox = Canvas(self.shipDisplayBar, height=25, 
								  width=121, relief=SUNKEN, border=2,
								  bg="#4C8ED4")
		self.longshipBox.grid(row=0, column=0)
		self.frigateBox = Canvas(self.shipDisplayBar, height=25, 
								 width=97, relief=SUNKEN, border=2, 
								 bg="#4C8ED4")
		self.frigateBox.grid(row=0, column=1)
		self.brigBox = Canvas(self.shipDisplayBar, height=25, width=73,
							  relief=SUNKEN, border=2, bg="#4C8ED4")
		self.brigBox.grid(row=0, column=2)
		self.schoonerBox = Canvas(self.shipDisplayBar, height=25, 
								  width=73, relief=SUNKEN, border=2, 
								  bg="#4C8ED4")
		self.schoonerBox.grid(row=0, column=3)
		self.sloopBox = Canvas(self.shipDisplayBar, height=25, width=49,
							   relief=SUNKEN, border=2, bg="#4C8ED4")
		self.sloopBox.grid(row=0, column=4)
		# Ship quickview labels
		self.longshipLabel = Label(self.shipDisplayBar, text="Longship")
		self.longshipLabel.grid(row=1, column=0)
		self.frigateLabel = Label(self.shipDisplayBar, text="Frigate")
		self.frigateLabel.grid(row=1, column=1)
		self.brigLabel = Label(self.shipDisplayBar, text="Brig")
		self.brigLabel.grid(row=1, column=2)
		self.schoonerLabel = Label(self.shipDisplayBar, text="Schooner")
		self.schoonerLabel.grid(row=1, column=3)
		self.sloopLabel = Label(self.shipDisplayBar, text="Sloop")
		self.sloopLabel.grid(row=1, column=4)

	def loadImages (self):
		""" Load pngs and create image dictionary. """
		self.__images["ocean"] = PhotoImage(
				file="battleshipOceanRetro.png")
		self.__images["parchment"] = PhotoImage(
				file="battleshipParchmentRetro.png")
		self.__images["longship"] = PhotoImage(
				file="battleshipLongship.png")
		self.__images["longshipV"] = PhotoImage(
				file="battleshipLongshipV.png")
		self.__images["frigate"] = PhotoImage(
				file="battleshipFrigate.png")
		self.__images["frigateV"] = PhotoImage(
				file="battleshipFrigateV.png")
		self.__images["brig"] = PhotoImage(file="battleshipBrig.png")
		self.__images["brigV"] = PhotoImage(file="battleshipBrigV.png")
		self.__images["schooner"] = PhotoImage(
				file="battleshipSchooner.png")
		self.__images["schoonerV"] = PhotoImage(
				file="battleshipSchoonerV.png")
		self.__images["sloop"] = PhotoImage(file="battleshipSloop.png")
		self.__images["sloopV"] = PhotoImage(
				file="battleshipSloopV.png")
		self.__images["fire"] = PhotoImage(
				file="battleshipFireTransparent.png")
		self.__images["splash"] = PhotoImage(
				file="battleshipSplashTransparent.png")
		self.__images["redX"] = PhotoImage(
				file="battleshipRedXTransparent.png")
		self.__images["whiteX"] = PhotoImage(
				file="battleshipWhiteXTransparent.png")
				
	def setBoundaries (self):
		""" Create dictionary for keeping ships completely on the board.
		
		Create a dictionary where the key is a ship type and orientation
		and the contents are a NumLet for the farthest downward and
		rightward a ship's bow (where its coordinates are recorded from)
		can go without the rest of it going off the game map.
		"""
		self.boundaries = {}
		self.boundaries["longshipV"] = (10, 'F')
		self.boundaries["longship"] = (6, 'J')
		self.boundaries["frigateV"] = (10, 'G')
		self.boundaries["frigate"] = (7, 'J')
		self.boundaries["brigV"] = (10, 'H')
		self.boundaries["brig"] = (8, 'J')
		self.boundaries["schoonerV"] = (10, 'H')
		self.boundaries["schooner"] = (8, 'J')
		self.boundaries["sloopV"] = (10, 'I')
		self.boundaries["sloop"] = (9, 'J')	
		
	# GAME CONSTRUCTION/RESETTING
	def setupVariables (self):
		""" Set up variables that are reset before every game. """
		self.__hiddenShips = [0, 1, 2, 3, 4]
		self.__shipsPlaced = 0
		self.__phase = "setup"
		self.__ghostShipType = "longship"
		self.__message.set(" ")

	def createMapGhosts (self):
		""" Create the icons that follow the mouse over maps. """
		self.__ghostShip = self.ocean.create_image(
			3, 3, image=self.__images[self.__ghostShipType], anchor=NW,
			state=HIDDEN)
		self.__ghostX = self.parchment.create_image(
			3, 3, image=self.__images["whiteX"], state=HIDDEN, 
			anchor=NW)

	def setupShipHealth (self):
		""" Set/reset all player & CPU ship healths to full health. """
		self.playerShips = {}
		self.CPUShips = {}
		self.playerShips["longship"] = 5
		self.playerShips["frigate"] = 4
		self.playerShips["schooner"] = 3
		self.playerShips["brig"] = 3
		self.playerShips["sloop"] = 2
		self.CPUShips["longship"] = 5
		self.CPUShips["frigate"] = 4
		self.CPUShips["schooner"] = 3
		self.CPUShips["brig"] = 3
		self.CPUShips["sloop"] = 2
	
	def newGame (self):
		""" Reset everything (displays and variables) for a new game."""
		self.ocean.delete("all")
		self.parchment.delete("all")
		self.longshipBox.delete("all")
		self.frigateBox.delete("all")
		self.schoonerBox.delete("all")
		self.brigBox.delete("all")
		self.sloopBox.delete("all")
		self.setupCanvases()
		self.setupVariables()
		self.createMapGhosts()
		self.buildGrids()
		self.setupShipHealth()
		self.placeShipsUpdate()
		self.generateParchmentGrid()
		
	# MAP CREATION	
	def buildGrids (self):
		self.oceanGrid = {}
		self.parchmentGrid = {}
		for num in range(1, 11):
			for let in range (0, 10):
				self.oceanGrid[(num, chr(65+let))]= \
					{"WhatShip":"none", "IsHit":False}
				self.parchmentGrid[(num, chr(65+let))]= \
					{"WhatShip":"none", "IsHit":False}
		
	def setupCanvases (self):
		self.ocean.create_image(3, 3, image=self.__images["ocean"],
								anchor=NW)
		self.parchment.create_image(3, 3, anchor=NW,
									image=self.__images["parchment"])
		self.placeOnCanvas (self.longshipBox, "longship", (1, 'A'))
		self.placeOnCanvas (self.frigateBox, "frigate", (1, 'A'))
		self.placeOnCanvas (self.brigBox, "brig", (1, 'A'))
		self.placeOnCanvas (self.schoonerBox, "schooner", (1, 'A'))
		self.placeOnCanvas (self.sloopBox, "sloop", (1, 'A'))
	
	def generateParchmentGrid (self):
		self.generateParchmentShip(choice(["longship", "longshipV"]))
		self.generateParchmentShip(choice(["frigate", "frigateV"]))
		self.generateParchmentShip(choice(["schooner", "schoonerV"]))
		self.generateParchmentShip(choice(["brig", "brigV"]))
		self.generateParchmentShip(choice(["sloop", "sloopV"]))
	
	def generateParchmentShip (self, activeShip):
		numlet = self.convertCoordToNumLet((randint(4, 
			self.convertNumLetToCoord(self.boundaries[activeShip])[0]), 
			randint(4, self.convertNumLetToCoord(
			self.boundaries[activeShip])[1])))
		while not (all(self.parchmentGrid[space]["WhatShip"] == "none" 
				for space in self.spacesOccupiedBy(activeShip, 
												   numlet))):
			numlet = self.convertCoordToNumLet((randint(4, 
				self.convertNumLetToCoord(
				self.boundaries[activeShip])[0]), 
				randint(4, self.convertNumLetToCoord(
				self.boundaries[activeShip])[1])))
		self.placeAShipParchment(numlet, activeShip)

	def placeAShipParchment (self, numLet, shipType):
		if shipType == "longshipV" or shipType == "longship":
			slot = 0
		elif shipType == "frigateV" or shipType == "frigate":
			slot = 1
		elif shipType == "schoonerV" or shipType == "schooner":
			slot = 2
		elif shipType == "brigV" or shipType == "brig":
			slot = 3
		else:
			slot = 4
		self.__hiddenShips[slot] = self.placeOnCanvas(self.parchment, 
													  shipType, numLet)
		self.parchment.itemconfig(self.__hiddenShips[slot], 
								  state=HIDDEN)
		for space in self.spacesOccupiedBy(shipType, numLet):
			self.parchmentGrid[space]["WhatShip"] = shipType
			
	# MAP FUNCTIONALITY		
	def placeOnCanvas (self, whichCanvas, item, location):
		return whichCanvas.create_image(self.convertNumLetToCoord (
										location), 
										image=self.__images[item],
										anchor=NW)
		
	def hideGhostShip (self, mouseleave):
		self.ocean.itemconfig(self.__ghostShip, state=HIDDEN)
	
	def hideGhostX (self, mouseleave):
		self.parchment.itemconfig(self.__ghostX, state=HIDDEN)
	
	def mouseOverOcean (self, mouse):
		if self.__ghostShipType != "none":
			locationNumLet = self.convertMouseToNumLet(mouse)
			locationCoord = self.convertNumLetToCoord(locationNumLet)
			if (locationNumLet[0] <= 
					self.boundaries[self.__ghostShipType][0] and
					locationNumLet[1] <= 
					self.boundaries[self.__ghostShipType][1]):
				self.ocean.coords(self.__ghostShip, locationCoord)
				self.ocean.itemconfig(self.__ghostShip, state=NORMAL)
			elif (locationNumLet[0] <= 
					self.boundaries[self.__ghostShipType][0]):
				self.ocean.coords(
					self.__ghostShip, (locationCoord[0], 3 + 24 *
					(ord(self.boundaries[self.__ghostShipType][1])-65)))
				self.ocean.itemconfig(self.__ghostShip, state=NORMAL)
			elif (locationNumLet[1] <= 
					self.boundaries[self.__ghostShipType][1]):
				self.ocean.coords(
					self.__ghostShip, (3 + 24 *
					(self.boundaries[self.__ghostShipType][0] - 1),
					locationCoord[1]))
				self.ocean.itemconfig(self.__ghostShip, state=NORMAL)
	
	def mouseOverParchment (self, mouse):
		if self.__phase == "attack":
			locationNumLet = self.convertMouseToNumLet(mouse)
			locationCoord = self.convertNumLetToCoord(locationNumLet)
			self.parchment.coords(self.__ghostX, locationCoord)
			self.parchment.itemconfig(self.__ghostX, state=NORMAL)
	
	def placeShipsUpdate (self):
		if self.__shipsPlaced == 0:
			self.__message.set(
					"LEFT CLICK on the ocean to place your LONGSHIP.\n" 
					"RIGHT CLICK to rotate it before placing it.")
			self.__ghostShipType = "longship"
		if self.__shipsPlaced == 1:
			self.__message.set(
					"LEFT CLICK on the ocean to place your FRIGATE.\n" 
					"RIGHT CLICK to rotate it before placing it.")
			self.__ghostShipType = "frigate"
		if self.__shipsPlaced == 2:
			self.__message.set(
					"LEFT CLICK on the ocean to place your SCHOONER.\n"
					"RIGHT CLICK to rotate it before placing it.")
			self.__ghostShipType = "schooner"
		if self.__shipsPlaced == 3:
			self.__message.set(
					"LEFT CLICK on the ocean to place your BRIG.\n" 
					"RIGHT CLICK to rotate it before placing it.")
			self.__ghostShipType = "brig"
		if self.__shipsPlaced == 4:
			self.__message.set(
					"LEFT CLICK on the ocean to place your SLOOP.\n "
					"RIGHT CLICK to rotate it before placing it.")
			self.__ghostShipType = "sloop"
		if self.__shipsPlaced == 5:
			self.__message.set("Now left click the parchment map to "
							   "attack the enemy.")
			self.__ghostShipType = "none"
			self.__phase = "attack"
			self.ocean.itemconfig(self.__ghostShip, state=HIDDEN)
		else:
			self.ocean.itemconfig(
				self.__ghostShip, 
				image=self.__images[self.__ghostShipType])
	
	# MAP INTERACTION
	def rotateGhostShip (self, mouseclick):
		if self.__ghostShipType == "longship":
			self.__ghostShipType = "longshipV"
		elif self.__ghostShipType == "frigate":
			self.__ghostShipType = "frigateV"
		elif self.__ghostShipType == "brig":
			self.__ghostShipType = "brigV"
		elif self.__ghostShipType == "schooner":
			self.__ghostShipType = "schoonerV"
		elif self.__ghostShipType == "sloop":
			self.__ghostShipType = "sloopV"
		elif self.__ghostShipType == "longshipV":
			self.__ghostShipType = "longship"
		elif self.__ghostShipType == "frigateV":
			self.__ghostShipType = "frigate"
		elif self.__ghostShipType == "brigV":
			self.__ghostShipType = "brig"
		elif self.__ghostShipType == "schoonerV":
			self.__ghostShipType = "schooner"
		elif self.__ghostShipType == "sloopV":
			self.__ghostShipType = "sloop"
		self.ocean.itemconfig(self.__ghostShip, 
							  image=self.__images[self.__ghostShipType])
							  
	def oceanLClick (self, leftclick):
		locationNumLet = self.convertMouseToNumLet(leftclick)
		if self.__ghostShipType != "none":
			if (locationNumLet[0] <= 
							self.boundaries[self.__ghostShipType][0] and
							locationNumLet[1] <= 
							self.boundaries[self.__ghostShipType][1]):
				self.placeAShipOcean (locationNumLet)
			elif (locationNumLet[0] <= 
					self.boundaries[self.__ghostShipType][0]):
				self.placeAShipOcean (
					(locationNumLet[0], 
					self.boundaries[self.__ghostShipType][1]))
			elif (locationNumLet[1] <= 
					self.boundaries[self.__ghostShipType][1]):
				self.placeAShipOcean (
					(self.boundaries[self.__ghostShipType][0], 
					locationNumLet[1]))
	
	def parchmentLClick (self, mouseclick):
		if self.__phase == "attack":
			if self.parchmentGrid[self.convertMouseToNumLet(
					mouseclick)]["IsHit"] is False:
				yourMove = self.processAttack(
					self.convertMouseToNumLet(mouseclick), 
					self.parchment)
				CPUnumLet = (randint(1, 10), chr(65 + randint(0, 9)))
				while self.oceanGrid[CPUnumLet]["IsHit"]:
					CPUnumLet = (randint(1, 10), chr(65 + 
						randint(0, 9)))
				CPUMove = self.processAttack(CPUnumLet, self.ocean)
				message = ("You attacked " + str(yourMove[0]) + 
					yourMove[1] + "\nYour opponent attacked " + 
					str(CPUMove[0]) + CPUMove[1])
				self.__message.set(message)
				self.checkVictory()
	
	def placeAShipOcean (self, numLet):
		if (all(self.oceanGrid[space]["WhatShip"] == "none" 
				for space in self.spacesOccupiedBy(self.__ghostShipType, 
												   numLet))):
			self.placeOnCanvas(self.ocean, self.__ghostShipType, numLet)
			for space in self.spacesOccupiedBy(self.__ghostShipType, 
											   numLet):
				self.oceanGrid[space]["WhatShip"] = self.__ghostShipType
			self.__shipsPlaced += 1
			self.placeShipsUpdate()
				
	# GENERAL FUNCTIONALITY			
	def convertMouseToNumLet (self, mouse):
		number = int((mouse.x - 4) / 24) + 1
		letter = chr(65+int((mouse.y - 4) / 24))
		# If something out of bounds is produced, bring it back in.
		if number > 10:
			number = 10
		if letter == 'K':
			letter = 'J'
		return (number, letter)
	
	def convertCoordToNumLet (self, coordinates):
		number = int((coordinates[0] - 4) / 24) + 1
		letter = chr(65+int((coordinates[1] - 4) / 24))
		# If something out of bounds is produced, bring it back in.
		if number > 10:
			number = 10
		if letter == 'K':
			letter = 'J'
		return (number, letter)
	
	def convertNumLetToCoord (self, NumLet):
		return (3 + (NumLet[0]-1)*24, 3 + (ord(NumLet[1])-65)*24)
	
	def spacesOccupiedBy (self, whatship, bowLocation):
		occupied = []
		# Horizontal ships
		if (whatship == "longship" or whatship == "frigate" or 
				whatship == "schooner" or whatship == "brig" or
				whatship == "sloop"):
			occupied.append(bowLocation)
			occupied.append((bowLocation[0]+1, bowLocation[1]))
		if (whatship == "longship" or whatship == "frigate" or 
				whatship == "schooner" or whatship == "brig"):	
			occupied.append((bowLocation[0]+2, bowLocation[1]))
		if whatship == "longship" or whatship == "frigate":	
			occupied.append((bowLocation[0]+3, bowLocation[1]))
		if whatship == "longship":
			occupied.append((bowLocation[0]+4, bowLocation[1]))
		# Vertical ships
		if (whatship == "longshipV" or whatship == "frigateV" or 
				whatship == "schoonerV" or whatship == "brigV" or
				whatship == "sloopV"):
			occupied.append(bowLocation)
			occupied.append((bowLocation[0], 
							 chr(ord(bowLocation[1])+1)))
		if (whatship == "longshipV" or whatship == "frigateV" or 
				whatship == "schoonerV" or whatship == "brigV"):	
			occupied.append((bowLocation[0], 
							 chr(ord(bowLocation[1])+2)))
		if whatship == "longshipV" or whatship == "frigateV":	
			occupied.append((bowLocation[0], 
							 chr(ord(bowLocation[1])+3)))
		if whatship == "longshipV":
			occupied.append((bowLocation[0], 
							 chr(ord(bowLocation[1])+4)))
		return occupied
		
	def processAttack (self, numLet, whichMap):
		whichGrid = self.oceanGrid
		if self.parchment == whichMap:
			whichGrid = self.parchmentGrid
		if whichGrid[numLet]["IsHit"] == False:
			whichGrid[numLet]["IsHit"] = True
			if whichGrid[numLet]["WhatShip"] == "none":
				didHit = " but didn't hit anything."
				if whichMap == self.ocean:
					image = "splash"
				else:
					image = "whiteX"
			else:
				didHit = " and hit a ship!"
				shipHit = whichGrid[numLet]["WhatShip"]
				if shipHit == "longshipV" or shipHit == "longship":
					shipHit = "longship"
					box = self.longshipBox
				if shipHit == "frigateV" or shipHit == "frigate":
					shipHit = "frigate"
					box = self.frigateBox
				if shipHit == "schoonerV" or shipHit == "schooner":
					shipHit = "schooner"
					box = self.schoonerBox
				if shipHit == "brigV" or shipHit == "brig":
					shipHit = "brig"
					box = self.brigBox
				if shipHit == "sloopV" or shipHit == "sloop":
					shipHit = "sloop"
					box = self.sloopBox
				if whichMap == self.parchment:
					image = "redX"
					self.CPUShips[shipHit] += -1
					if self.CPUShips[shipHit] == 0:
						didHit = " and sunk a " + shipHit + "!"
				else:
					didHit = " and hit your " + shipHit + "!"
					image = "fire"
					self.placeOnCanvas(box, image, 
									   (self.playerShips[shipHit], 'A'))
					self.playerShips[shipHit] += -1
					if self.playerShips[shipHit] == 0:
						didHit = " and sunk your " + shipHit + "!"
			self.placeOnCanvas(whichMap, image, numLet)
		return (numLet, didHit)
		
	def checkVictory (self):
		if (self.CPUShips["longship"] == 0 and 
				self.CPUShips["frigate"] == 0 and 
				self.CPUShips["schooner"] == 0 and
				self.CPUShips["brig"] == 0 and 
				self.CPUShips["sloop"] == 0):
			self.__phase = "over"
			self.__message.set("You've sunken the enemy fleet!\n"
							   "Victory is yours!")
		if (self.playerShips["longship"] == 0 and 
				self.playerShips["frigate"] == 0 and 
				self.playerShips["schooner"] == 0 and
				self.playerShips["brig"] == 0 and 
				self.playerShips["sloop"] == 0):
			self.__phase = "over"
			self.__message.set("Your entire fleet rests in Davy Jones'"
							   "locker!\nThe enemy has won!")
		if self.__phase == "over":
			# Lock everything down.
			self.parchment.bind("<Button-1>", 0)
			self.parchment.bind("<Motion>", 0)
			self.parchment.bind("<Leave>", 0)
			self.ocean.bind("<Button-1>", 0)
			self.ocean.bind("<Motion>", 0)
			self.ocean.bind("<Leave>", 0)
			self.ocean.bind("<Button-3>", 0)
			for i in range (0, 5):
				# Reveal the enemy ships
				self.parchment.itemconfig(self.__hiddenShips[i], 
										  state=NORMAL)
		
	def run(self):
		""" Run Battleship"""
		self.root.mainloop()
	

if __name__ == '__main__':
	app = Battleship()
	app.run()
