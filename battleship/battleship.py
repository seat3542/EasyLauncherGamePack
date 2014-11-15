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

class Battleship():
	
	def __init__(self):
		self.root = Tk()
		self.root.title("Battleship")
		self.message = StringVar()
		self.images = {}
		self.setupVariables()
		self.loadImages()
		self.buildGUI()
		self.setBoundaries()
		self.newGame()
		
	def setupVariables (self):
		self.hiddenShips = [0, 1, 2, 3, 4]
		self.shipsPlaced = 0
		self.phase = "setup"
		self.ghostShipType = "longship"
		self.message.set(" ")
	
	def newGame (self):
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
	
	def createMapGhosts (self):
		self.ghostShip = self.ocean.create_image(3, 3,
								image=self.images[self.ghostShipType],
								state=HIDDEN, anchor=NW,)
		self.ghostX = self.parchment.create_image(3, 3,
								image=self.images["whiteX"],
								state=HIDDEN, anchor=NW,)
	
	def buildGUI(self):
		self.contentFrame = Frame(self.root)
		self.contentFrame.grid(row=0, column=0)
		self.topBar = Frame(self.contentFrame, border=2, relief=RAISED,
							pady=3)
		self.topBar.grid(row=0, column=0, columnspan=23, sticky=E+W)
		self.newGameButton = Button(self.topBar, text="New Game",
									command=self.newGame)
		self.newGameButton.grid(row=0, column=0)
		self.messageBox = Label(self.topBar, textvariable=self.message,
								height=2)
		self.messageBox.grid(row=1, column=0, sticky=W+E)
		# Assigning weights
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_rowconfigure(0, weight=1)
		self.contentFrame.grid_columnconfigure(0, weight=1)
		self.contentFrame.grid_rowconfigure(0, weight=1)
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
		self.topLeftBar.grid (column=1, row=1, columnspan=10, sticky=W+E, pady=(5,0))
		for column in range (0, 9):
			self.topLeftBar.grid_columnconfigure(column, weight=1)
		self.topRightBar = Frame(self.contentFrame, padx=4)
		self.topRightBar.grid (column=12, row=1, columnspan=10, sticky=W+E, pady=(5,0))
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
		# Ship quickview displays
		self.shipsLabel = Label(self.contentFrame, text="Your\nShips")
		self.shipsLabel.grid(row=12, column=11)
		self.longshipBox = Canvas(self.contentFrame, height=25, 
								  width=121, relief=SUNKEN, border=2,
								  bg="#4C8ED4")
		self.longshipBox.grid(column=1, row=13, columnspan=5)
		self.frigateBox = Canvas(self.contentFrame, height=25, width=97,
								 relief=SUNKEN, border=2, bg="#4C8ED4")
		self.frigateBox.grid(row=13, column=7, columnspan=4)
		self.brigBox = Canvas(self.contentFrame, height=25, width=73,
							  relief=SUNKEN, border=2, bg="#4C8ED4")
		self.brigBox.grid(row=13, column=12, columnspan=3)
		self.schoonerBox = Canvas(self.contentFrame, height=25, width=73,
							  relief=SUNKEN, border=2, bg="#4C8ED4")
		self.schoonerBox.grid(row=13, column=16, columnspan=3)
		self.sloopBox = Canvas(self.contentFrame, height=25, width=49,
							   relief=SUNKEN, border=2, bg="#4C8ED4")
		self.sloopBox.grid(row=13, column=20, columnspan=2)
		# Ship quickview labels
		self.longshipLabel = Label(self.contentFrame, text="Longship")
		self.longshipLabel.grid(column=1, row=14, columnspan=5)
		self.frigateLabel = Label(self.contentFrame, text="Frigate")
		self.frigateLabel.grid(row=14, column=7, columnspan=4)
		self.brigLabel = Label(self.contentFrame, text="Brig")
		self.brigLabel.grid(row=14, column=12, columnspan=3)
		self.schoonerLabel = Label(self.contentFrame, text="Schooner")
		self.schoonerLabel.grid(row=14, column=16, columnspan=3)
		self.sloopLabel = Label(self.contentFrame, text="Sloop")
		self.sloopLabel.grid(row=14, column=20, columnspan=2)
		
	def setupCanvases (self):
		self.ocean.create_image(3, 3, image=self.images["ocean"],
								anchor=NW)
		self.parchment.create_image(3, 3, anchor=NW,
									image=self.images["parchment"])
		self.placeOnCanvas (self.longshipBox, "longship", (1, 'A'))
		self.placeOnCanvas (self.frigateBox, "frigate", (1, 'A'))
		self.placeOnCanvas (self.brigBox, "brig", (1, 'A'))
		self.placeOnCanvas (self.schoonerBox, "schooner", (1, 'A'))
		self.placeOnCanvas (self.sloopBox, "sloop", (1, 'A'))
		
	def loadImages (self):
		self.images["ocean"] = PhotoImage(
				file="battleshipOceanRetro.png")
		self.images["parchment"] = PhotoImage(
				file="battleshipParchmentRetro.png")
		self.images["longship"] = PhotoImage(
				file="battleshipLongship.png")
		self.images["longshipV"] = PhotoImage(
				file="battleshipLongshipV.png")
		self.images["frigate"] = PhotoImage(
				file="battleshipFrigate.png")
		self.images["frigateV"] = PhotoImage(
				file="battleshipFrigateV.png")
		self.images["brig"] = PhotoImage(file="battleshipBrig.png")
		self.images["brigV"] = PhotoImage(file="battleshipBrigV.png")
		self.images["schooner"] = PhotoImage(
				file="battleshipSchooner.png")
		self.images["schoonerV"] = PhotoImage(
				file="battleshipSchoonerV.png")
		self.images["sloop"] = PhotoImage(file="battleshipSloop.png")
		self.images["sloopV"] = PhotoImage(file="battleshipSloopV.png")
		self.images["fire"] = PhotoImage(
				file="battleshipFireTransparent.png")
		self.images["splash"] = PhotoImage(
				file="battleshipSplashTransparent.png")
		self.images["redX"] = PhotoImage(
				file="battleshipRedXTransparent.png")
		self.images["whiteX"] = PhotoImage(
				file="battleshipWhiteXTransparent.png")
		
	def setBoundaries (self):
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
	
	def setupShipHealth (self):
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
	
	def placeOnCanvas (self, whichCanvas, item, location):
		return whichCanvas.create_image(self.convertToCoord (location),
								 anchor=NW, image=self.images[item])
		
	def hideGhostShip (self, mouseleave):
		self.ocean.itemconfig(self.ghostShip, state=HIDDEN)
	
	def hideGhostX (self, mouseleave):
		self.parchment.itemconfig(self.ghostX, state=HIDDEN)
	
	def rotateGhostShip (self, mouseclick):
		if self.ghostShipType == "longship":
			self.ghostShipType = "longshipV"
		elif self.ghostShipType == "frigate":
			self.ghostShipType = "frigateV"
		elif self.ghostShipType == "brig":
			self.ghostShipType = "brigV"
		elif self.ghostShipType == "schooner":
			self.ghostShipType = "schoonerV"
		elif self.ghostShipType == "sloop":
			self.ghostShipType = "sloopV"
		elif self.ghostShipType == "longshipV":
			self.ghostShipType = "longship"
		elif self.ghostShipType == "frigateV":
			self.ghostShipType = "frigate"
		elif self.ghostShipType == "brigV":
			self.ghostShipType = "brig"
		elif self.ghostShipType == "schoonerV":
			self.ghostShipType = "schooner"
		elif self.ghostShipType == "sloopV":
			self.ghostShipType = "sloop"
		self.ocean.itemconfig(self.ghostShip, 
							  image=self.images[self.ghostShipType])
	
	def mouseOverOcean (self, mouse):
		if self.ghostShipType != "none":
			locationNumLet = self.convertMouseToNumLet(mouse)
			locationCoord = self.convertToCoord(locationNumLet)
			if (locationNumLet[0] <= 
							self.boundaries[self.ghostShipType][0] and
							locationNumLet[1] <= 
							self.boundaries[self.ghostShipType][1]):
				self.ocean.coords(self.ghostShip, locationCoord)
				self.ocean.itemconfig(self.ghostShip, state=NORMAL)
			elif (locationNumLet[0] <= 
					self.boundaries[self.ghostShipType][0]):
				self.ocean.coords(
						self.ghostShip, (locationCoord[0], 3 + 24 *
						(ord(self.boundaries[self.ghostShipType][1])-65)))
				self.ocean.itemconfig(self.ghostShip, state=NORMAL)
			elif (locationNumLet[1] <= 
					self.boundaries[self.ghostShipType][1]):
				self.ocean.coords(self.ghostShip, (3 + 24*
								 (self.boundaries[self.ghostShipType][0]-1),
								  locationCoord[1]))
				self.ocean.itemconfig(self.ghostShip, state=NORMAL)
	
	def mouseOverParchment (self, mouse):
		if self.phase == "attack":
			locationNumLet = self.convertMouseToNumLet(mouse)
			locationCoord = self.convertToCoord(locationNumLet)
			self.parchment.coords(self.ghostX, locationCoord)
			self.parchment.itemconfig(self.ghostX, state=NORMAL)
	
	def parchmentLClick (self, mouseclick):
		if self.phase == "attack":
			if self.parchmentGrid[self.convertMouseToNumLet(mouseclick)]["IsHit"] is False:
				yourMove = self.processAttack(self.convertMouseToNumLet(mouseclick), self.parchment)
				CPUnumLet = (randint(1, 10), chr(65 + randint(0, 9)))
				while self.oceanGrid[CPUnumLet]["IsHit"] is True:
					CPUnumLet = (randint(1, 10), chr(65 + randint(0, 9)))
				CPUMove = self.processAttack(CPUnumLet, self.ocean)
				message = "You attacked " + str(yourMove[0]) + yourMove[1] + "\nYour opponent attacked " + str(CPUMove[0]) + CPUMove[1]
				self.message.set(message)
				self.checkVictory()
				
	def convertMouseToNumLet (self, mouse):
		number = int((mouse.x - 4) / 24) + 1
		letter = chr(65+int((mouse.y - 4) / 24))
		return (number, letter)
	
	def convertCoordToNumLet (self, coordinates):
		number = int((coordinates[0] - 4) / 24) + 1
		letter = chr(65+int((coordinates[1] - 4) / 24))
		return (number, letter)
	
	def convertToCoord (self, NumLet):
		return (3 + (NumLet[0]-1)*24, 3 + (ord(NumLet[1])-65)*24)
		
	def buildGrids (self):
		self.oceanGrid = {}
		self.parchmentGrid = {}
		for num in range(1, 11):
			for let in range (0, 10):
				self.oceanGrid[(num, chr(65+let))]={"WhatShip":"none", "IsHit":False}
				self.parchmentGrid[(num, chr(65+let))]={"WhatShip":"none", "IsHit":False}
		
	def run(self):
		""" Run Battleship"""
		self.root.mainloop()
	
	# GAMEPLAY
	# Setup phase
	def oceanLClick (self, leftclick):
		locationNumLet = self.convertMouseToNumLet(leftclick)
		if self.ghostShipType != "none":
			if (locationNumLet[0] <= 
							self.boundaries[self.ghostShipType][0] and
							locationNumLet[1] <= 
							self.boundaries[self.ghostShipType][1]):
				self.placeAShipOcean (locationNumLet)
			elif (locationNumLet[0] <= 
					self.boundaries[self.ghostShipType][0]):
				self.placeAShipOcean ((locationNumLet[0], self.boundaries[self.ghostShipType][1]))
			elif (locationNumLet[1] <= 
					self.boundaries[self.ghostShipType][1]):
				self.placeAShipOcean ((self.boundaries[self.ghostShipType][0], locationNumLet[1]))
	
	def placeShipsUpdate (self):
		if self.shipsPlaced == 0:
			self.message.set(
					"LEFT CLICK on the ocean to place your LONGSHIP.\n RIGHT CLICK to rotate it before placing it.")
			self.ghostShipType = "longship"
		if self.shipsPlaced == 1:
			self.message.set(
					"LEFT CLICK on the ocean to place your FRIGATE.\n RIGHT CLICK to rotate it before placing it.")
			self.ghostShipType = "frigate"
		if self.shipsPlaced == 2:
			self.message.set(
					"LEFT CLICK on the ocean to place your SCHOONER.\n RIGHT CLICK to rotate it before placing it.")
			self.ghostShipType = "schooner"
		if self.shipsPlaced == 3:
			self.message.set(
					"LEFT CLICK on the ocean to place your BRIG.\n RIGHT CLICK to rotate it before placing it.")
			self.ghostShipType = "brig"
		if self.shipsPlaced == 4:
			self.message.set(
					"LEFT CLICK on the ocean to place your SLOOP.\n RIGHT CLICK to rotate it before placing it.")
			self.ghostShipType = "sloop"
		if self.shipsPlaced == 5:
			self.message.set("Good. You placed all your ships.")
			self.ghostShipType = "none"
			self.phase = "attack"
			self.ocean.itemconfig(self.ghostShip, state=HIDDEN)
		else:
			self.ocean.itemconfig(self.ghostShip, 
								  image=self.images[self.ghostShipType])
	
	def placeAShipOcean (self, numLet):
		if (all(self.oceanGrid[space]["WhatShip"] == "none" 
				for space in self.spacesOccupiedBy(self.ghostShipType, 
				numLet))):
			self.placeOnCanvas(self.ocean, self.ghostShipType, numLet)
			for space in self.spacesOccupiedBy(self.ghostShipType, 
											   numLet):
				self.oceanGrid[space]["WhatShip"] = self.ghostShipType
			self.shipsPlaced += 1
			self.placeShipsUpdate()
	
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
		self.hiddenShips[slot] = self.placeOnCanvas(self.parchment, shipType, numLet)
		self.parchment.itemconfig(self.hiddenShips[slot], state=HIDDEN)
		for space in self.spacesOccupiedBy(shipType, numLet):
			self.parchmentGrid[space]["WhatShip"] = shipType
	
	def spacesOccupiedBy (self, whatship, bowLocation):
		occupied = []
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
		if (whatship == "longshipV" or whatship == "frigateV" or 
				whatship == "schoonerV" or whatship == "brigV" or
				whatship == "sloopV"):
			occupied.append(bowLocation)
			occupied.append((bowLocation[0], chr(ord(bowLocation[1])+1)))
		if (whatship == "longshipV" or whatship == "frigateV" or 
				whatship == "schoonerV" or whatship == "brigV"):	
			occupied.append((bowLocation[0], chr(ord(bowLocation[1])+2)))
		if whatship == "longshipV" or whatship == "frigateV":	
			occupied.append((bowLocation[0], chr(ord(bowLocation[1])+3)))
		if whatship == "longshipV":
			occupied.append((bowLocation[0], chr(ord(bowLocation[1])+4)))
		return occupied
		
	def generateParchmentGrid (self):
		activeShip = "longship"
		# Generate Longship
		if randint(0, 1) == 1:
			activeShip = "longshipV"
		numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		self.placeAShipParchment(numlet, activeShip)
		# generate frigate
		if randint(0, 1) == 1:
			activeShip = "frigateV"
		else:
			activeShip = "frigate"
		numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		while not (all(self.parchmentGrid[space]["WhatShip"] == "none" 
				for space in self.spacesOccupiedBy(activeShip, numlet))):
			numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		self.placeAShipParchment(numlet, activeShip)
		# generate Schooner
		if randint(0, 1) == 1:
			activeShip = "schoonerV"
		else:
			activeShip = "schooner"
		numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		while not (all(self.parchmentGrid[space]["WhatShip"] == "none" 
				for space in self.spacesOccupiedBy(activeShip, numlet))):
			numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		self.placeAShipParchment(numlet, activeShip)
		# generate brig
		if randint(0, 1) == 1:
			activeShip = "brigV"
		else:
			activeShip = "brig"
		numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		while not (all(self.parchmentGrid[space]["WhatShip"] == "none" 
				for space in self.spacesOccupiedBy(activeShip, numlet))):
			numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		self.placeAShipParchment(numlet, activeShip)
		# generate sloop
		if randint(0, 1) == 1:
			activeShip = "sloopV"
		else:
			activeShip = "sloop"
		numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		while not (all(self.parchmentGrid[space]["WhatShip"] == "none" 
				for space in self.spacesOccupiedBy(activeShip, numlet))):
			numlet = self.convertCoordToNumLet((randint(4, self.convertToCoord(self.boundaries[activeShip])[0]), randint(4, self.convertToCoord(self.boundaries[activeShip])[1])))
		self.placeAShipParchment(numlet, activeShip)
	
	# Attack phase
	
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
					self.placeOnCanvas(box, image, (self.playerShips[shipHit], 'A'))
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
			self.phase = "over"
			self.message.set("You've sunken the enemy fleet!\nVictory is yours!")
		if (self.playerShips["longship"] == 0 and 
				self.playerShips["frigate"] == 0 and 
				self.playerShips["schooner"] == 0 and
				self.playerShips["brig"] == 0 and 
				self.playerShips["sloop"] == 0):
			self.phase = "over"
			self.message.set("Your entire fleet rests in Davy Jones' locker!\nThe enemy has won!")
		if self.phase == "over":
			self.parchment.bind("<Button-1>", 0)
			self.parchment.bind("<Motion>", 0)
			self.parchment.bind("<Leave>", 0)
			self.ocean.bind("<Button-1>", 0)
			self.ocean.bind("<Motion>", 0)
			self.ocean.bind("<Leave>", 0)
			self.ocean.bind("<Button-3>", 0)
			for i in range (0, 5):
				self.parchment.itemconfig(self.hiddenShips[i], 
										  state=NORMAL)
		

if __name__ == '__main__':
	app = Battleship()
	app.run()
