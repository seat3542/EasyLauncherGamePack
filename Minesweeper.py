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
		self.__size = IntVar ()
		self.__size.set (16)
		self.__score = IntVar ()
		self.__score.set (0)
		self.__numMines = 25
		self.mainframe = Frame(self.root)
		self.mainframe.grid (column=0, row=0)
		self.header = Frame(self.mainframe)
		self.header.grid (column=0, row=0)
		self.label = Label(self.header, textvariable=self.__score)
		self.label.grid (column=0, row=0)
		self.DEBUG = Button(self.header, text="DEBUG", command=self.revealAll)
		self.DEBUG.grid (column=1, row=0)
		self.gamewindow = Frame(self.mainframe)
		self.gamewindow.grid (column=0, row=1)
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
		for x in range(0, self.__numMines):
			mineLocation.append((randint(0, self.__size.get() - 1), 
								randint(0, self.__size.get() - 1)))
			if x > 0:
				for y in range(0, x-1):
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
	
	def revealAll (self):
		for x in range(0, self.__size.get()):
			for y in range(0, self.__size.get()):
				self.board[x][y].revealEntry('<Button-1>')

	def run(self):
		self.root.mainloop()

class boardentry ():
	def __init__ (self, row, column, parent):
		self.__parent = parent
		self.__mine = False
		self.__flag = False
		self.__bordered = 0
		self.UIbutton = Button(parent.gamewindow, text=" ")
		self.UIbutton.grid(column=column, row=row)
		self.UIbutton.bind('<Button-1>', self.checkEntry)
		self.UIbutton.bind('<Button-3>', self.flagEntry)
	
	def checkEntry (self,buttonpush):
		if self.__mine == True:
			self.__parent.revealAll()
		else:
			self.revealEntry(buttonpush)
	
	def revealEntry (self, buttonpush):
		if self.__mine == True:
			self.UIbutton.config(bg="black", state=DISABLED, relief=SUNKEN)
		else:
			self.UIbutton.config(bg="grey", state=DISABLED, relief=SUNKEN)
			#Ugly debugging code!
			if self.__bordered == 1:
				self.UIbutton.config(text="1", bg="green")
			if self.__bordered == 2:
				self.UIbutton.config(text="2", bg="teal")
			if self.__bordered == 3:
				self.UIbutton.config(text="3", bg="blue")
			if self.__bordered == 4:
				self.UIbutton.config(text="4", bg="purple")
			if self.__bordered == 5:
				self.UIbutton.config(text="5", bg="dark red")
			if self.__bordered == 6:
				self.UIbutton.config(text="6", bg="red")
			if self.__bordered == 7:
				self.UIbutton.config(text="7", bg="orange")
			if self.__bordered == 8:
				self.UIbutton.config(text="8", bg="yellow")
			
	
	def flagEntry (self, buttonpush):
		if self.__flag == False:
			self.__flag = True
			self.UIbutton.config(bg="red", activebackground="red")
		else:
			self.__flag = False
			self.UIbutton.config(bg="light grey")
	
	def setMine (self, mine):
		self.__mine = mine
	
	def getMine (self):
		return self.__mine
	
	def setBordered (self, bordered):
		self.__bordered = bordered

if __name__ == '__main__':
	app = Minesweeper()
	app.run()
