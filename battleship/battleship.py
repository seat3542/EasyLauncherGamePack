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
		self.leftLabels = []
		self.rightLabels = []
		self.loadImages()
		self.message = StringVar()
		self.message.set("This is much harder than it should be.")
		self.buildGUI()
		
	
	def buildGUI(self):
		self.contentFrame = Frame(self.root)
		self.contentFrame.grid(row=0, column=0)
		self.topBar = Frame(self.contentFrame, border=2, relief=RAISED, 
							bg="red")
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
			self.leftLabels.append(Label(self.contentFrame, text=i+1))
			self.rightLabels.append(Label(self.contentFrame, text=i+1))
			self.leftLabels[i].grid(row=(i-8), column=0)
			self.rightLabels[i].grid(row=(i-8), column=22)
		#Maps
		self.ocean = Canvas(self.contentFrame, height=241, width=241,
							relief=SUNKEN, border=2)
		self.ocean.grid (row=2, column=1, rowspan=10, columnspan=10)
		self.parchment = Canvas(self.contentFrame, height=241, 
								width=241, relief=SUNKEN, border=2)
		self.parchment.grid(row=2, column=12, rowspan=10, columnspan=10)
		# Ship quickview displays
		self.shipsLabel = Label(self.contentFrame, text="Your\nShips")
		self.shipsLabel.grid(row=12, column=11)
		self.longshipBox = Canvas(self.contentFrame, height=25, 
								  width=121, relief=SUNKEN, border=2)
		self.longshipBox.grid(column=1, row=13, columnspan=5)
		self.frigateBox = Canvas(self.contentFrame, height=25, width=97,
								 relief=SUNKEN, border=2)
		self.frigateBox.grid(row=13, column=7, columnspan=4)
		self.brigBox = Canvas(self.contentFrame, height=25, width=73,
							  relief=SUNKEN, border=2)
		self.brigBox.grid(row=13, column=12, columnspan=3)
		self.schoonerBox = Canvas(self.contentFrame, height=25, width=73,
							  relief=SUNKEN, border=2)
		self.schoonerBox.grid(row=13, column=16, columnspan=3)
		self.sloopBox = Canvas(self.contentFrame, height=25, width=49,
							   relief=SUNKEN, border=2)
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
				
	
	def placeOnCanvas (self, whichCanvas, item, x, y):
		whichCanvas.create_image(3 + (x-1)*24, 3 + (y-1)*24, 
								 image=self.images[item], anchor=NW)
		
	def run(self):
		""" Run Battleship"""
		self.root.mainloop()

if __name__ == '__main__':
	app = Battleship()
	app.run()
