/****************************************************************************
 * File: 				hangman.h
 * Author:			littlefiredragon @ github
 * Description: A text-based hangman game made for the Easy Launcher
 * 							Game Pack.
 ***************************************************************************/
#ifndef HANGMAN_H
#define HANGMAN_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

typedef struct Alphabet
{
	char letter;
	bool bGuessed;
	bool bInWord;
} Alphabet;

typedef struct Hangman
{
	char pictures[8][37];
	Alphabet sAlphabet[26];
	char *word;
	int wordLength;
	int hangingMan;
} Hangman;

void initializeAlphabet (Alphabet sAlphabet[], char *word, int wordlength);
void setupPictures (Hangman *psGame);
void chooseWord (char **word, int *wordLength);
void initializeGame (Hangman *psGame);
void printGame (Hangman *psGame);
void takeTurn (Hangman *psGame);
bool gameIsOver (Hangman *psGame);
bool gameIsWon (Hangman *psGame);

#endif /* HANGMAN_H */
