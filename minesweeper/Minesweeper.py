#!/usr/bin/python3
#############################################################
# File Name:   Minesweeper.py
# Author:	   A.S. ("LittleFireDragon")
# Date:		   11/9/14
# Purpose:	   The classic game, Minesweeper, made in python.
#############################################################
from tkinter import *
from random import randint

class Minesweeper ():
	def __init__(self):
		self.root = Tk()
		self.root.title("Minesweeper")
		self.gameOver = False
		self.__size = IntVar ()
		self.__size.set (16)
		self.__score = IntVar ()
		self.__score.set (0)
		self.__numMines = IntVar ()
		self.__numMines.set (25)
		self.__numFlags = IntVar ()
		self.__numFlags.set (0)
		self.__spacesUnrevealed = self.__size.get() * self.__size.get()
		# Set up images
		self.images = {}
		self.images[1] = PhotoImage(file="1.png")
		self.images[2] = PhotoImage(file="2.png")
		self.images[3] = PhotoImage(file="3.png")
		self.images[4] = PhotoImage(file="4.png")
		self.images[5] = PhotoImage(file="5.png")
		self.images[6] = PhotoImage(file="6.png")
		self.images[7] = PhotoImage(file="7.png")
		self.images[8] = PhotoImage(file="8.png")
		self.images["mine"] = PhotoImage(file="mine.png")
		self.images["flagmine"] = PhotoImage(file="flagmine.png")
		self.images["flag"] = PhotoImage(file="flag.png")
		self.images["blank"] = PhotoImage(file="blank.png")
		#End image setup
		self.mainframe = Frame(self.root)
		self.mainframe.grid (column=0, row=0)
		self.header = Frame(self.mainframe)
		self.header.grid (column=0, row=0, sticky=W+E)
		self.scoreLabel = Label(self.header, text="Score:")
		self.scoreLabel.grid (column=0, row=0)
		self.scoreDisplay = Label(self.header, relief=SUNKEN, width=5,
									textvariable=self.__score)
		self.scoreDisplay.grid (column=0, row=1, padx=10)
		self.flagsLabel = Label(self.header, image=self.images["flag"])
		self.flagsLabel.grid (column=1, row=0)
		self.flagsDisplay = Label(self.header, relief=SUNKEN, width=5,
									textvariable=self.__numFlags)
		self.flagsDisplay.grid (column=1, row=1, padx=10)
		self.minesLabel = Label(self.header, image=self.images["mine"])
		self.minesLabel.grid (column=2, row=0)
		self.minesDisplay = Label(self.header, relief=SUNKEN, width=5,
									textvariable=self.__numMines)
		self.minesDisplay.grid (column=2, row=1, padx=10)
		self.newGame = Button(self.header, text="New Game", 
							command=self.newGame)
		self.newGame.grid (column=3, row=0, rowspan=2, sticky=N+S+E+W,
							padx=10)
		self.gamewindow = Frame(self.mainframe, border=1, relief=SUNKEN)
		self.gamewindow.grid (column=0, row=1, pady=2)
		#initialize board
		self.board = []
		for i in range(0,self.__size.get()):
			self.board.append ([])
			self.board[i] = [boardentry(i, j, self) 
							for j in range(0,self.__size.get())]
		#Generate mines
		self.generateMines()
		#Find bordered mines for all entries.
		self.setBordered()

	def generateMines (self):
		mineLocation = []
		for x in range(0, self.__numMines.get()):
			mineLocation.append((randint(0, self.__size.get() - 1), 
								randint(0, self.__size.get() - 1)))
			#if x > 0:
			for y in range(0, x):
				while mineLocation[x] == mineLocation[y]:
					mineLocation[x] = ((randint(0, self.__size.get() - 1), 
										randint(0, self.__size.get() - 1)))
			self.board[mineLocation[x][0]][mineLocation[x][1]].setMine (True)

	def setBordered (self):
		for x in range(0, self.__size.get()):
			for y in range(0, self.__size.get()):
				bordered = 0
				if x > 0 and y > 0:
					if self.board[x-1][y-1].getMine() == True:
						bordered += 1
				if y > 0:
					if self.board[x][y-1].getMine() == True:
						bordered += 1
				if y > 0 and x < self.__size.get() - 1:
					if self.board[x+1][y-1].getMine() == True:
						bordered += 1
				if x > 0:
					if self.board[x-1][y].getMine() == True:
						bordered += 1
				if x < self.__size.get() - 1:
					if self.board[x+1][y].getMine() == True:
						bordered += 1
				if x > 0 and y < self.__size.get() - 1:
					if self.board[x-1][y+1].getMine() == True:
						bordered += 1
				if y < self.__size.get() - 1:
					if self.board[x][y+1].getMine() == True:
						bordered += 1
				if x < self.__size.get() - 1 and y < self.__size.get() - 1:
					if self.board[x+1][y+1].getMine() == True:
						bordered += 1
				self.board[x][y].setBordered (bordered)
	
	def revealAdjacentBlanks (self, row, column):
		self.board[row][column].revealEntry('<Button-1>')
		self.board[row][column].sink ('<ButtonRelease-1>')

		if row > 0 and column > 0:
			if self.board[row-1][column-1].getBordered() == 0 \
					and self.board[row-1][column-1].getRevealed() == False:
				self.revealAdjacentBlanks (row-1, column-1)
			elif self.board[row-1][column-1].getRevealed() == False:
				self.board[row-1][column-1].revealEntry ('<Button-1>')
				self.board[row-1][column-1].sink ('<ButtonRelease-1>')
		if column > 0:
			if self.board[row][column-1].getBordered() == 0 \
					and self.board[row][column-1].getRevealed() == False:
				self.revealAdjacentBlanks (row, column-1)
			elif self.board[row][column-1].getRevealed() == False:
				self.board[row][column-1].revealEntry ('<Button-1>')
				self.board[row][column-1].sink ('<ButtonRelease-1>')
		if column > 0 and row < self.__size.get() - 1:
			if self.board[row+1][column-1].getBordered() == 0 \
					and self.board[row+1][column-1].getRevealed() == False:
				self.revealAdjacentBlanks (row+1, column-1)
			elif self.board[row+1][column-1].getRevealed() == False:
				self.board[row+1][column-1].revealEntry ('<Button-1>')
				self.board[row+1][column-1].sink ('<ButtonRelease-1>')
		if row > 0:
			if self.board[row-1][column].getBordered() == 0 \
					and self.board[row-1][column].getRevealed() == False:
				self.revealAdjacentBlanks (row-1, column)
			elif self.board[row-1][column].getRevealed() == False:
				self.board[row-1][column].revealEntry ('<Button-1>')
				self.board[row-1][column].sink ('<ButtonRelease-1>')
		if row < self.__size.get() - 1:
			if self.board[row+1][column].getBordered() == 0 \
					and self.board[row+1][column].getRevealed() == False:
				self.revealAdjacentBlanks (row+1, column)
			elif self.board[row+1][column].getRevealed() == False:
				self.board[row+1][column].revealEntry ('<Button-1>')
				self.board[row+1][column].sink ('<ButtonRelease-1>')
		if row > 0 and column < self.__size.get() - 1:
			if self.board[row-1][column+1].getBordered() == 0 \
					and self.board[row-1][column+1].getRevealed() == False:
				self.revealAdjacentBlanks (row-1, column+1)
			elif self.board[row-1][column+1].getRevealed() == False:
				self.board[row-1][column+1].revealEntry ('<Button-1>')
				self.board[row-1][column+1].sink ('<ButtonRelease-1>')
		if column < self.__size.get() - 1:
			if self.board[row][column+1].getBordered() == 0 \
					and self.board[row][column+1].getRevealed() == False:
				self.revealAdjacentBlanks (row, column+1)
			elif self.board[row][column+1].getRevealed() == False:
				self.board[row][column+1].revealEntry ('<Button-1>')
				self.board[row][column+1].sink ('<ButtonRelease-1>')
		if row < self.__size.get() - 1 and column < self.__size.get() - 1:
			if self.board[row+1][column+1].getBordered() == 0 \
					and self.board[row+1][column+1].getRevealed() == False:
				self.revealAdjacentBlanks (row+1, column+1)
			elif self.board[row+1][column+1].getRevealed() == False:
				self.board[row+1][column+1].revealEntry ('<Button-1>')
				self.board[row+1][column+1].sink ('<ButtonRelease-1>')
	
	def revealAll (self):
		self.gameOver = True
		for x in range(0, self.__size.get()):
			for y in range(0, self.__size.get()):
				self.board[x][y].revealEntry('<Button-1>')
				self.board[x][y].sink('<ButtonRelease-1>')
	
	def increaseScore (self):
		self.__score.set (self.__score.get() + 1)
	
	def decrementUnrevealed (self):
		self.__spacesUnrevealed += -1
	
	def decrementFlags (self):
		self.__numFlags.set (self.__numFlags.get() - 1)
	
	def incrementFlags (self):
		self.__numFlags.set (self.__numFlags.get() + 1)
		
	def getUnrevealed (self):
		return self.__spacesUnrevealed
	
	def getMines (self):
		return self.__numMines.get()
		
	def newGame (self):
		self.gameOver = False
		self.__size.set (16)
		self.__score.set (0)
		self.__numMines.set (25)
		self.__numFlags.set (0)
		self.resetBoard ()
		self.generateMines()
		self.setBordered()
	
	def resetBoard (self):
		for i in range(0,self.__size.get()):
			for j in range(0,self.__size.get()):
				self.board[i][j].reset()

	def run(self):
		self.root.mainloop()

class boardentry ():
	def __init__ (self, row, column, parent):
		self.__parent = parent
		self.__mine = False
		self.__flag = False
		self.__bordered = 0
		self.__revealed = False
		self.__col = column
		self.__row = row
		self.UIbutton = Button(parent.gamewindow,
								image=parent.images["blank"],
								activeforeground="light grey", 
								activebackground="light grey")
		self.UIbutton.grid(column=column, row=row)
		self.UIbutton.bind('<Button-1>', self.checkEntry)
		self.UIbutton.bind('<ButtonRelease-1>', self.sink)
		self.UIbutton.bind('<Button-3>', self.flagEntry)
	
	def reset (self):
		self.__mine = False
		self.__flag = False
		self.__bordered = 0
		self.__revealed = False
		self.UIbutton.config (image=self.__parent.images["blank"],
								relief=RAISED)
		self.UIbutton.bind('<Button-1>', self.checkEntry)
	
	def checkEntry (self,buttonpush):
		if self.__mine == True:
			self.__parent.revealAll()
		elif self.__bordered == 0:
			self.__parent.revealAdjacentBlanks (self.__row, self.__col)
		else:
			self.revealEntry(buttonpush)
		if self.__parent.getUnrevealed () == self.__parent.getMines ():
			self.__parent.gameOver = True
	
	def revealEntry (self, buttonpush):
		if self.__revealed == False:
			self.__parent.decrementUnrevealed()
			self.__revealed = True
			if self.__mine == False and self.__parent.gameOver == False:
				self.__parent.increaseScore()
				if self.__flag == True:
					self.__flag = False
					self.__parent.decrementFlags()
			if self.__mine == True and self.__flag == True:
				self.UIbutton.config(image=self.__parent.images["flagmine"])
			elif self.__mine == True:
				self.UIbutton.config(image=self.__parent.images["mine"])
			elif self.__bordered == 0:
				self.UIbutton.config(image=self.__parent.images["blank"])
			else:
				self.UIbutton.config(
							image=self.__parent.images[self.__bordered])
			
	def sink (self, buttonrelease):
		self.UIbutton.config(command=0, relief=FLAT)
	
	def flagEntry (self, buttonpush):
		if self.__revealed == False:
			if self.__flag == False:
				self.__flag = True
				self.UIbutton.config(image=self.__parent.images["flag"])
				self.__parent.incrementFlags()
			else:
				self.__flag = False
				self.UIbutton.config(image=self.__parent.images["blank"])
				self.__parent.decrementFlags()
	
	def setMine (self, mine):
		self.__mine = mine
	
	def getMine (self):
		return self.__mine
	
	def setBordered (self, bordered):
		self.__bordered = bordered
	
	def getBordered (self):
		return self.__bordered
	
	def getRevealed (self):
		return self.__revealed

if __name__ == '__main__':
	app = Minesweeper()
	app.run()
