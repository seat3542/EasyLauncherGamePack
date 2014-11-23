#ifndef HANGMAN_H_
#define HANGMAN_H_

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct Alphabet
{
	char letter;
	bool bInWord;
	bool bGuessed;
} Alphabet;

typedef struct Hangman
{
	char *word;
	int wordLength;
	Alphabet sAlphabet[26];
	int hangingMan;
	char pictures[8][37];
} Hangman;

void initializeAlphabet (Alphabet sAlphabet[], char *word, int wordlength);
void setupPictures (Hangman *psGame);
void chooseWord (char **word, int *wordLength);
void initializeGame (Hangman *psGame);
void printGame (Hangman *psGame);
void takeTurn (Hangman *psGame);
bool gameIsOver (Hangman *psGame);
bool gameIsWon (Hangman *psGame);

#endif /* HANGMAN_H_ */
