#!/usr/bin/python3
#############################################################
# File Name:   Minesweeper.py
# Author:	   A.S. ("LittleFireDragon")
# Date:		   11/11/14
# Purpose:	   The classic game, Minesweeper, made in python.
#############################################################
from tkinter import *
from random import randint

class Minesweeper():
	""" Game of logically deducing locations of and flagging bombs. """
	
	def __init__(self):
		""" Initialize the entire game."""
		self.root = Tk()
		self.root.title("Minesweeper")
		# Variables
		self.board = []
		self.gameOver = False
		self.images = {}
		self.__size = IntVar()
		self.__score = IntVar()
		self.__numMines = IntVar()
		self.__numFlags = IntVar()
		self.__spacesUnrevealed = 0
		self.__endMessage = StringVar()
		# Setup
		self.resetVariables()
		self.loadImages()
		self.constructUI()
		self.createBoard()
		self.generateMines()
		self.setBordered()
	
	def createBoard (self):
		""" Generate boardentries to populate the game board."""
		for i in range(0,self.__size.get()):
			self.board.append([])
			self.board[i] = [boardentry(i, j, self) 
							for j in range(0,self.__size.get())]

	def generateMines (self):
		""" Generate mines and place them randomly on the board.
		
		Generate the game's specified number of mines by generating row
		and column coordinates randomly. Check the previously created 
		mines to ensure no duplicate mines are created (and therefore, 
		that there are exactly the specified number of mines on the 
		board). Once a valid set of coordinates is created, set the
		boardentry in that location to have a mine in it.
		"""
		mineCoord = []
		for x in range(0, self.__numMines.get()):
			mineCoord.append((randint(0, self.__size.get() - 1), 
							  randint(0, self.__size.get() - 1)))
			for y in range(0, x):
				while mineCoord[x] == mineCoord[y]:	# Prevent duplicates
					mineCoord[x] = ((randint(0, self.__size.get() - 1), 
									randint(0, self.__size.get() - 1)))
			self.board[mineCoord[x][0]][mineCoord[x][1]].setMine(True)
	
	def loadImages (self):
		""" Load png files from the minesweeper directory.
		
		Load pngs from the minesweeper directory into PhotoImages. Then
		fill out the images dictionary with these PhotoImages. Number
		tiles are keyed with their actual corresponding number, and
		image tiles are keyed with descriptive strings.
		"""
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

	def constructUI (self):
		""" Construct the UI using tkinter frames, etc.
		
		Construct a tkinter grid system with three main sections: the
		header on top, the game window in the middle, and the game
		message on the bottom. The header contains 3 pairs of a label on
		top and a display on the bottom, from left to right: score,
		number of flags, and number of mines. It also contains the new
		game button spanning both rows on the far right. The game 
		message contains only a label that displays a message when the
		game ends. The game window contains the board.
		"""
		self.contentFrame = Frame(self.root)
		self.contentFrame.grid(column=0, row=0)
		self.header = Frame(self.contentFrame)
		self.header.grid(column=0, row=0, sticky=W+E)
		self.scoreLabel = Label(self.header, text="Score:")
		self.scoreLabel.grid(column=0, row=0)
		self.scoreDisplay = Label(self.header, relief=SUNKEN, 
								  width=5, textvariable=self.__score)
		self.scoreDisplay.grid(column=0, row=1, padx=10)
		self.flagsLabel = Label(self.header, image=self.images["flag"])
		self.flagsLabel.grid(column=1, row=0)
		self.flagsDisplay = Label(self.header, relief=SUNKEN, width=5,
								  textvariable=self.__numFlags)
		self.flagsDisplay.grid(column=1, row=1, padx=10)
		self.minesLabel = Label(self.header, image=self.images["mine"])
		self.minesLabel.grid(column=2, row=0)
		self.minesDisplay = Label(self.header, relief=SUNKEN, width=5,
								  textvariable=self.__numMines)
		self.minesDisplay.grid(column=2, row=1, padx=10)
		self.newGameButton = Button(self.header, text="New Game", 
									command=self.newGame)
		self.newGameButton.grid(column=3, row=0, rowspan=2, 
								sticky=N+S+E+W, padx=10)			
		self.gamewindow = Frame(self.contentFrame, border=1, 
								relief=SUNKEN)
		self.gamewindow.grid(column=0, row=1, pady=2)
		self.gameMessage = Label(self.contentFrame, 
								 textvariable=self.__endMessage)
		self.gameMessage.grid (column=0, row=2, columnspan=4)

	def setBordered (self):
		""" Tell each boardentry how many mines border it.
		
		The first layer of ifs is to detect when a boardentry has no
		adjacent entries in a given direction (e.g. if it's on row 0 it
		has nothing above it), to prevent the next layer of ifs from
		stepping over the boundaries of the board.
		The second layer of ifs checks whether the immediately adjacent
		entry in that direction has a mine in it, and if so, adds 1 to
		the border counter. The sum of all 8 of these (or fewer, if some
		directions don't get past the first layer of ifs) is set as that
		entry's value for how many mines border it.
		"""
		for row in range(0, self.__size.get()):
			for column in range(0, self.__size.get()):
				bordered = 0
				# Top left
				if row > 0 and column > 0:
					if self.board[row-1][column-1].getMine():
						bordered += 1
				# Left
				if column > 0:
					if self.board[row][column-1].getMine():
						bordered += 1
				# Bottom left
				if column > 0 and row < self.__size.get() - 1:
					if self.board[row+1][column-1].getMine():
						bordered += 1
				# Top
				if row > 0:
					if self.board[row-1][column].getMine():
						bordered += 1
				# Bottom
				if row < self.__size.get() - 1:
					if self.board[row+1][column].getMine():
						bordered += 1
				# Top right
				if row > 0 and column < self.__size.get() - 1:
					if self.board[row-1][column+1].getMine():
						bordered += 1
				# Top
				if column < self.__size.get() - 1:
					if self.board[row][column+1].getMine():
						bordered += 1
				# Bottom right
				if (row < self.__size.get() - 1 and 
						column < self.__size.get() -1 ):
					if self.board[row+1][column+1].getMine():
						bordered += 1
				self.board[row][column].setBordered (bordered)
	
	def revealAdjacentBlanks (self, row, column):
		""" Recursively reveal all reachable empty boxes and a border.
		
		Reveal the given entry. Then recursively spread in all eight
		directions, revealing all connected blank (bordered by 0 mines) 
		entries, as well as revealing one additional layer (which 
		consists of numbered entries).
		"""
		self.board[row][column].revealEntry('<Button-1>')
		self.board[row][column].sink('<ButtonRelease-1>')
		# Top left
		if row > 0 and column > 0:
			if (self.board[row-1][column-1].getBordered() == 0 and
					self.board[row-1][column-1].getRevealed() is False):
				self.revealAdjacentBlanks(row-1, column-1)
			elif self.board[row-1][column-1].getRevealed() is False:
				self.board[row-1][column-1].revealEntry('<Button-1>')
				self.board[row-1][column-1].sink('<ButtonRelease-1>')
		# Left
		if column > 0:
			if (self.board[row][column-1].getBordered() == 0 and
					self.board[row][column-1].getRevealed() is False):
				self.revealAdjacentBlanks(row, column-1)
			elif self.board[row][column-1].getRevealed() is False:
				self.board[row][column-1].revealEntry('<Button-1>')
				self.board[row][column-1].sink('<ButtonRelease-1>')
		# Bottom left
		if column > 0 and row < self.__size.get() - 1:
			if (self.board[row+1][column-1].getBordered() == 0 and
					self.board[row+1][column-1].getRevealed() is False):
				self.revealAdjacentBlanks(row+1, column-1)
			elif self.board[row+1][column-1].getRevealed() is False:
				self.board[row+1][column-1].revealEntry('<Button-1>')
				self.board[row+1][column-1].sink('<ButtonRelease-1>')
		# Top
		if row > 0:
			if (self.board[row-1][column].getBordered() == 0 and
					self.board[row-1][column].getRevealed() is False):
				self.revealAdjacentBlanks(row-1, column)
			elif self.board[row-1][column].getRevealed() is False:
				self.board[row-1][column].revealEntry('<Button-1>')
				self.board[row-1][column].sink('<ButtonRelease-1>')
		# Bottom
		if row < self.__size.get() - 1:
			if (self.board[row+1][column].getBordered() == 0 and
					self.board[row+1][column].getRevealed() is False):
				self.revealAdjacentBlanks(row+1, column)
			elif self.board[row+1][column].getRevealed() is False:
				self.board[row+1][column].revealEntry('<Button-1>')
				self.board[row+1][column].sink('<ButtonRelease-1>')
		# Top right
		if row > 0 and column < self.__size.get() - 1:
			if (self.board[row-1][column+1].getBordered() == 0 and
					self.board[row-1][column+1].getRevealed() is False):
				self.revealAdjacentBlanks(row-1, column+1)
			elif self.board[row-1][column+1].getRevealed() is False:
				self.board[row-1][column+1].revealEntry('<Button-1>')
				self.board[row-1][column+1].sink('<ButtonRelease-1>')
		# Right
		if column < self.__size.get() - 1:
			if (self.board[row][column+1].getBordered() == 0 and
					self.board[row][column+1].getRevealed() is False):
				self.revealAdjacentBlanks(row, column+1)
			elif self.board[row][column+1].getRevealed() is False:
				self.board[row][column+1].revealEntry('<Button-1>')
				self.board[row][column+1].sink('<ButtonRelease-1>')
		# Bottom right
		if (row < self.__size.get() - 1 and 
				column < self.__size.get() - 1):
			if (self.board[row+1][column+1].getBordered() == 0 and
					self.board[row+1][column+1].getRevealed() is False):
				self.revealAdjacentBlanks(row+1, column+1)
			elif self.board[row+1][column+1].getRevealed() is False:
				self.board[row+1][column+1].revealEntry('<Button-1>')
				self.board[row+1][column+1].sink('<ButtonRelease-1>')
	
	def revealAll (self):
		""" End game. Reveal (without sinking) all hidden entries."""
		self.gameOver = True	# Prevent from messing with score
		for x in range(0, self.__size.get()):
			for y in range(0, self.__size.get()):
				self.board[x][y].revealEntry('<Button-1>')
	
	def increaseScore (self):
		""" Increment the score by one."""
		self.__score.set(self.__score.get() + 1)
	
	def decrementUnrevealed (self):
		""" Decrease the number of unrevealed spaces by one."""
		self.__spacesUnrevealed += -1
		
	def getUnrevealed (self):
		""" Get the number of unrevealed spaces."""
		return self.__spacesUnrevealed
	
	def decrementFlags (self):
		""" Decrease the counter for flags in play by one."""
		self.__numFlags.set(self.__numFlags.get() - 1)
	
	def incrementFlags (self):
		""" Increase the counter for flags in play by one."""
		self.__numFlags.set(self.__numFlags.get() + 1)
		
	def getMines (self):
		""" Get the number of mines on the board"""
		return self.__numMines.get()
	
	def win (self):
		""" Set the game message to a victory message."""
		self.__endMessage.set("Congratulations! You win!")
		
	def lose (self):
		""" Set the game message to a loss message."""
		self.__endMessage.set("Oops! Better luck next time!")
		
	def newGame (self):
		""" Reset all aspects of the game."""
		self.resetVariables()
		self.resetBoard()
		self.generateMines()
		self.setBordered()
	
	def resetVariables (self):
		""" Reset game variables."""
		self.gameOver = False
		self.__size.set(16)
		self.__score.set(0)
		self.__numMines.set(25)
		self.__numFlags.set(0)
		self.__spacesUnrevealed = self.__size.get() * self.__size.get()
		self.__endMessage.set(" ")
	
	def resetBoard (self):
		""" Reset every entry in the game board."""
		for i in range(0,self.__size.get()):
			for j in range(0,self.__size.get()):
				self.board[i][j].reset()

	def run(self):
		""" Run Minesweeper"""
		self.root.mainloop()


class boardentry():
	""" A square on the board, including its UI button.
	
	The game's board is essentially a 2D list consisting of these. Each
	one has some attributes and an associated button on the UI.
	"""
	
	def __init__(self, row, column, parent):
		""" Initialize a cell upon creation."""
		self.__parent = parent
		self.__col = column
		self.__row = row
		self.__mine = False
		self.__flag = False
		self.__revealed = False
		self.__bordered = 0
		self.UIbutton = Button(parent.gamewindow,
							   image=parent.images["blank"],
							   activeforeground="light grey", 
							   activebackground="light grey")
		self.UIbutton.grid(column=column, row=row)
		self.UIbutton.bind('<Button-1>', self.checkEntry)
		self.UIbutton.bind('<ButtonRelease-1>', self.sink)
		self.UIbutton.bind('<Button-3>', self.flagEntry)
	
	def reset (self):
		""" Resets the cell's attributes and button to default."""
		self.__mine = False
		self.__flag = False
		self.__bordered = 0
		self.__revealed = False
		self.UIbutton.config(image=self.__parent.images["blank"],
							 relief=RAISED)
		self.UIbutton.bind('<Button-1>', self.checkEntry)
		
	def flagEntry (self, buttonpush):
		""" Toggle whether the unrevealed cell has a flag on it."""
		if self.__revealed is False:
			if self.__flag is False:
				self.__flag = True
				self.UIbutton.config(image=self.__parent.images["flag"])
				self.__parent.incrementFlags()
			else:
				self.__flag = False
				self.UIbutton.config(
									image=self.__parent.images["blank"])
				self.__parent.decrementFlags()
	
	def checkEntry (self,buttonpush):
		""" Check the contents of a cell and run appropriate function.
		
		Check what's in a cell when it's clicked. If the cell has a
		mine, the game is over. Otherwise, if the cell has no mines
		around it, flood out and reveal all such connected cells. 
		Otherwise, just reveal that cell.
		"""
		if self.__mine:
			self.__parent.lose()
			self.__parent.revealAll()
		elif self.__bordered == 0:	# Clear vast swaths of 0s.
			self.__parent.revealAdjacentBlanks(self.__row, self.__col)
		else:
			self.revealEntry(buttonpush)
	
	def revealEntry (self, buttonpush):
		""" Reveal a cell's contents and change appropriate counters.
		
		Reveal a cell's contents. Decrease number of unrevealed cells,
		and if appropriate, increase the score. If the cell was flagged,
		and clicking it does not cause a game over, remove the flag,
		so the counter won't be wrong. Set the button's image.
		"""
		if self.__revealed is False:
			# Handle the counters
			self.__parent.decrementUnrevealed()
			self.__revealed = True
			if self.__mine is False and self.__parent.gameOver is False:
				self.__parent.increaseScore()
				if self.__flag:
					self.__flag = False
					self.__parent.decrementFlags()
			# Change the image
			if self.__mine and self.__flag:
				self.UIbutton.config(
								image=self.__parent.images["flagmine"])
			elif self.__mine:
				self.UIbutton.config(image=self.__parent.images["mine"])
			elif self.__bordered == 0:
				self.UIbutton.config(
									image=self.__parent.images["blank"])
			else:
				self.UIbutton.config(
							image=self.__parent.images[self.__bordered])
			
	def sink (self, buttonrelease):
		""" During a game, 'disable' a button and make it flat.
		
		Only while the game is running (so revealing remaining icons
		after a game ends keeps them visually distinct), set a button
		to be flat and do nothing when clicked (not setting it to
		DISABLED because that would grey out the images). Also, because
		this is the last thing called in the process of clicking a cell,
		check for victory here - if the number of unrevealed cells is
		equal to the number of mines, the player has won.
		"""
		if self.__parent.gameOver is False:
			self.UIbutton.config(command=0, relief=FLAT)
			# Victory check
			if (self.__parent.getUnrevealed() == 
					self.__parent.getMines()):
				self.__parent.win()
				self.__parent.revealAll()
	
	def setMine (self, mine):
		""" Set whether this cell contains a mine."""
		self.__mine = mine
	
	def getMine (self):
		""" Get whether this cell contains a mine."""
		return self.__mine
	
	def setBordered (self, bordered):
		""" Set how many mines border this cell."""
		self.__bordered = bordered
	
	def getBordered (self):
		""" Get how many mines border this cell."""
		return self.__bordered
	
	def getRevealed (self):
		""" Get whether this cell is revealed or not."""
		return self.__revealed


if __name__ == '__main__':
	app = Minesweeper()
	app.run()
