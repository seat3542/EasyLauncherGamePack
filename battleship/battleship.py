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
		self.images = {}
		self.boundaries = {}
		self.leftLabels = []
		self.rightLabels = []
		self.loadImages()
		self.message = StringVar()
		self.message.set("Yarrr, matey. This game be unfinished!")
		self.buildGUI()
		self.setBoundaries()
		self.hoverIconType = "longship"
		self.hoverIcon = self.ocean.create_image(3, 3,
								image=self.images[self.hoverIconType],
								state=HIDDEN, anchor=NW,)
		
		#NOTE TO SELF: grid will be a dictionary. Keys will be NumLets.
		#            Contents will be dictionary: [Whatship] and [IsHit]
	
	def buildGUI(self):
		self.contentFrame = Frame(self.root)
		self.contentFrame.grid(row=0, column=0)
		self.topBar = Frame(self.contentFrame, border=2, relief=RAISED)
		self.topBar.grid(row=0, column=0, columnspan=23, sticky=E+W)
		self.newGameButton = Button(self.topBar, text="New Game")
		self.newGameButton.grid(row=0, column=0)
		self.messageBox = Label(self.topBar, textvariable=self.message,
								height=2)
		self.messageBox.grid(row=1, column=0, sticky=W+E)
		# Map grid labels
		for i in range(0, 10):
			self.leftLabels.append(Label(self.contentFrame, text=i+1))
			self.rightLabels.append(Label(self.contentFrame, text=i+1))
			self.leftLabels[i].grid(row=1, column=(i+1))
			self.rightLabels[i].grid(row=1, column=(i+12))
		for i in range(10, 20):
			self.leftLabels.append(Label(self.contentFrame, 
										 text=chr(55+i)))
			self.rightLabels.append(Label(self.contentFrame, 
										  text=chr(55+i)))
			self.leftLabels[i].grid(row=(i-8), column=0)
			self.rightLabels[i].grid(row=(i-8), column=22)
		#Maps
		self.ocean = Canvas(self.contentFrame, height=241, width=241,
							relief=SUNKEN, border=2)
		self.ocean.grid (row=2, column=1, rowspan=10, columnspan=10)
		self.parchment = Canvas(self.contentFrame, height=241, 
								width=241, relief=SUNKEN, border=2)
		self.parchment.grid(row=2, column=12, rowspan=10, columnspan=10)
		self.ocean.bind("<Button-1>", self.canvasLClick)
		self.parchment.bind("<Button-1>", self.canvasLClick)
		self.ocean.bind("<Motion>", self.mouseOverOcean)
		self.ocean.bind("<Leave>", self.hideGhostShip)
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
		# Draw on canvas
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
	
	def placeOnCanvas (self, whichCanvas, item, location):
		return whichCanvas.create_image(self.convertToCoord (location),
								 anchor=NW, image=self.images[item])
		
	def canvasLClick (self, leftclick):
		print(self.convertToNumLet(leftclick))
		
	def hideGhostShip (self, mouseleave):
		self.ocean.itemconfig(self.hoverIcon, state=HIDDEN)
	
	def mouseOverOcean (self, mouse):
		locationNumLet = self.convertToNumLet(mouse)
		locationCoord = self.convertToCoord(locationNumLet)
		if (locationNumLet[0] <= 
						self.boundaries[self.hoverIconType][0] and
						locationNumLet[1] <= 
						self.boundaries[self.hoverIconType][1]):
			self.ocean.coords(self.hoverIcon, locationCoord)
			self.ocean.itemconfig(self.hoverIcon, state=NORMAL)
		elif (locationNumLet[0] <= 
				self.boundaries[self.hoverIconType][0]):
			self.ocean.coords(
					self.hoverIcon, (locationCoord[0], 3 + 24 *
					(ord(self.boundaries[self.hoverIconType][1])-65)))
			self.ocean.itemconfig(self.hoverIcon, state=NORMAL)
		elif (locationNumLet[1] <= 
				self.boundaries[self.hoverIconType][1]):
			self.ocean.coords(self.hoverIcon, (3 + 24*
							 (self.boundaries[self.hoverIconType][0]-1),
							  locationCoord[1]))
			self.ocean.itemconfig(self.hoverIcon, state=NORMAL)
		
	def convertToNumLet (self, mouse):
		number = int((mouse.x - 4) / 24) + 1
		letter = chr(65+int((mouse.y - 4) / 24))
		return (number, letter)
	
	def convertToCoord (self, NumLet):
		return (3 + (NumLet[0]-1)*24, 3 + (ord(NumLet[1])-65)*24)
		
	def run(self):
		""" Run Battleship"""
		self.root.mainloop()




if __name__ == '__main__':
	app = Battleship()
	app.run()
