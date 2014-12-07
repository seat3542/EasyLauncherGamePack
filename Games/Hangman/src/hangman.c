/****************************************************************************
 * File: 				hangman.c
 * Author:			littlefiredragon @ github
 * Description: A text-based hangman game made for the Easy Launcher
 * 							Game Pack.
 ***************************************************************************/

#include "../include/hangman.h"
#include <stdio.h>		/* For user input, screen output, file reading */
#include <stdlib.h>		/* For random number generator */
#include <stdbool.h>	/* For some "is" or "is not" shortcut functions */
#include <string.h>		/* For strcpy'ing ASCII art into an array */
#include <time.h>			/* For seeding random number generator */

#define FILENAME "../data/words.txt"
#define ALPHABET_SIZE 26
#define CHAR_CASE_OFFSET 32
#define MAX_MISTAKES 7

/****************************************************************************
 * Function:		initializeAlphabet
 * Description:	Initializes the alphabet array with capital letters, bGuessed
 * 							set to false, and determines whether each letter is in the
 * 							word and sets bInWord accordingly.
 * Parameters:	sAlphabet[]	-	Alphabet array
 * 							word				-	The chosen word to play the game with
 * 							wordlength	- How many characters are in that word
 * Returns:			None
 ***************************************************************************/
void initializeAlphabet (Alphabet sAlphabet[], char *word, int wordlength)
{
	int i = 0;
	int j = 0;
	for (i = 0; i < ALPHABET_SIZE; i++)
	{
		sAlphabet[i].letter = 'A' + i;
		sAlphabet[i].bGuessed = false;
		sAlphabet[i].bInWord = false;
		for (j = 0; j < wordlength; j++)
		{
			if (sAlphabet[i].letter == word[j])
			{
				sAlphabet[i].bInWord = true;
			} /* if alphabet letter is in the word */
		} /* for each letter in the word */
	} /* for each letter in the alphabet */
} /* end void initializeAlphabet */

/****************************************************************************
 * Function:		setupPictures
 * Description:	Places ASCII art consisting of 36 characters into their
 * 							slot of the pictures array. This art depicts the gallows
 * 							and the stick figure. The array index is the number of
 * 							incorrect guesses the player has made.
 * Parameters:	psGame	-	the hangman game.
 * Returns:			None
 ***************************************************************************/
void setupPictures (Hangman *psGame)
{
	strcpy(psGame->pictures[0], " +--+\n    |\n    |\n    |\n    |\n____|\n");
	strcpy(psGame->pictures[1], " +--+\n O  |\n    |\n    |\n    |\n____|\n");
	strcpy(psGame->pictures[2], " +--+\n O  |\n +  |\n    |\n    |\n____|\n");
	strcpy(psGame->pictures[3], " +--+\n O  |\n-+  |\n    |\n    |\n____|\n");
	strcpy(psGame->pictures[4], " +--+\n O  |\n-+- |\n    |\n    |\n____|\n");
	strcpy(psGame->pictures[5], " +--+\n O  |\n-+- |\n |  |\n    |\n____|\n");
	strcpy(psGame->pictures[6], " +--+\n O  |\n-+- |\n |  |\n/   |\n____|\n");
	strcpy(psGame->pictures[7], " +--+\n O  |\n-+- |\n |  |\n/ \\ |\n____|\n");
}

/****************************************************************************
 * Function:		chooseWord
 * Description:	Opens words.txt and reads the first line to determine how
 * 							many words it can choose from. Generates a random number
 * 							within this bound - if it generates 8, it will find the 8th
 * 							word in the document. Then reads and discards lines until
 * 							it reaches the line it's looking for. Reads a number and
 * 							places it in the word length pointed to, and allocates
 * 							enough space for a word of that size at the word pointer.
 * 							Reads the word and places it in the allocated space.
 * Parameters:	hWord				-	pointer to the char* that will become the word
 * 							pWordLength	-	pointer to the int that stores the word length
 * Returns:			None
 ***************************************************************************/
void chooseWord (char **hWord, int *pWordLength)
{
	FILE *pInputFile;
	int numWords;
	int chosen;
	int i = 0;

	pInputFile = fopen (FILENAME, "r");
	if (NULL == pInputFile)
	{
		printf ("ERROR: File not found!\n");
		exit (EXIT_FAILURE);
	} /* If no input file */
	fscanf (pInputFile, "%i\n", &numWords);
	chosen = 1 + (random () % numWords);
	for (i = 0; i < chosen; i++)
	{
		fscanf (pInputFile, "%i ", pWordLength);
		*hWord = (char *) malloc (sizeof(char) * *pWordLength);
		fscanf (pInputFile, "%s\n", *hWord);
		if (i != chosen - 1)
		{
			free ((void *) *hWord);
		} /* If we're not to chosen line yet */
	} /* for however long it takes to reach the chosen number */
	fclose (pInputFile);
} /* end void chooseWord */

/****************************************************************************
 * Function:		initializeGame
 * Description:	Sets up the entire game by setting all variables to default
 * 							and calling chooseWord, setupPictures, and initializeAlphabet
 * Parameters:	psGame	-	game to be initialized
 * Returns:			none
 ***************************************************************************/
void initializeGame (Hangman *psGame)
{
	psGame->word = NULL;
	psGame->wordLength = 0;
	psGame->hangingMan = 0;
	setupPictures (psGame);
	chooseWord (&(psGame->word), &(psGame->wordLength));
	initializeAlphabet (psGame->sAlphabet, psGame->word, psGame->wordLength);
} /* end void initializeGame */

/****************************************************************************
 * Function:		printGame
 * Description:	Prints the hangman gallows ASCII art, all the incorrectly
 * 							guessed characters, and the word being guessed at, with its
 * 							guessed letters displaying and its unguessed letters shown
 * 							as underscores.
 * Parameters:	psGame	-	game to print
 * Returns:			None
 ***************************************************************************/
void printGame (Hangman *psGame)
{
	int i = 0;

	printf ("%s\n", psGame->pictures[psGame->hangingMan]);
	for (i = 0; i < ALPHABET_SIZE; i++)
	{
		if (psGame->sAlphabet[i].bGuessed == true
				&& psGame->sAlphabet[i].bInWord == false)
		{
			printf ("%c ", psGame->sAlphabet[i].letter);
		} /* if letter i has been guessed and is not in the word */
	} /* for every letter in the alphabet */
	printf ("\n");
	for (i = 0; i < psGame->wordLength; i++)
	{
		if (psGame->sAlphabet[(psGame->word[i]) - 'A'].bGuessed == true)
		{
			printf ("%c", psGame->word[i]);
		} /* if this letter has been guessed */
		else
		{
			printf ("_");
		} /* if this letter has not been guessed */
	} /* for every letter in the word */
	printf ("\n");
} /* end void printGame */

/****************************************************************************
 * Function:		takeTurn
 * Description:	Prompts the player to enter a letter and continues to prompt
 * 							until valid input (characters between 'A' and 'Z' or 'a' and
 * 							'z', not yet guessed) is received.
 * Parameters:	psGame	-	game to use the data of
 * Returns:			None
 ***************************************************************************/
void takeTurn (Hangman *psGame)
{
	char letter = ' ';
	if (psGame->hangingMan < MAX_MISTAKES)
	{
		while ((letter < 'A' || letter > 'Z')
					|| psGame->sAlphabet[letter - 'A'].bGuessed == true)
		{
			printf ("Guess another letter: ");
			scanf (" %c", &letter);
			if (letter <= 'z' && letter >= 'a')
			{
				letter = letter - CHAR_CASE_OFFSET;
			} /* if letter is between 'a' and 'z', inclusive */
		} /* while letter is outside A-Z range or has already been guessed */
		if (psGame->sAlphabet[letter - 'A'].bInWord == false)
		{
			psGame->hangingMan++;
		} /* if letter is not in word */
		psGame->sAlphabet[letter - 'A'].bGuessed = true;
	} /* if hangingMan < max number of mistaken guesses allowed */
} /* end void takeTurn */

/****************************************************************************
 * Function:		gameIsOver
 * Description:	Determines whether the game is over.
 * Parameters:	psGame			-	game to determine status of
 * Returns:			bIsGameOver	-	whether the game is over
 ***************************************************************************/
bool gameIsOver (Hangman *psGame)
{
	bool bIsGameOver = false;
	if (MAX_MISTAKES == psGame->hangingMan || gameIsWon(psGame))
	{
		bIsGameOver = true;
	} /* if gameIsWon returns true or hangingMan = max mistakes allowed */
	return bIsGameOver;
} /* end bool gameIsOver */

/****************************************************************************
 * Function:		gameIsWon
 * Description:	Determines whether the game has been won (all characters in
 * 							the word have been guessed).
 * Parameters:	psGame			-	game to have status determined
 * Returns:			bIsGameWon	-	whether the user has won
 ***************************************************************************/
bool gameIsWon (Hangman *psGame)
{
	bool bIsGameWon = true;
	int i = 0;
	for (i = 0; i < psGame->wordLength; i++)
	{
		if (!(psGame->sAlphabet[psGame->word[i] - 65].bGuessed))
		{
			bIsGameWon = false;
		} /* if this letter in the word hasn't been guessed */
	} /* for each letter in the word */
	return bIsGameWon;
} /* end bool gameIsWon */

/****************************************************************************
 * Function:		main
 * Description:	Runs the game, hangman.
 * Parameters:	None
 * Returns:			0
 ***************************************************************************/
int main ()
{
	Hangman sGame;
	bool bEndProgram = false;
	char userChoice = ' ';

	srand(time(NULL));

	while (!bEndProgram)		// Loop allows user to play consecutive games
	{
		userChoice = ' ';			// Reset so prompt at the end works correctly.
		initializeGame (&sGame);

		while (!gameIsOver(&sGame))
		{
			printf ("\n======================\n");
			printGame (&sGame);
			takeTurn (&sGame);
		} /* while game isn't over */

		/* Once the game is over, print the final screen and ask if the user
		   wants to play again. */
		printf ("======================\n");
		printGame(&sGame);
		if (gameIsWon(&sGame))
		{
			printf ("Congratulations, you won! Good work!\n");
		} /* if game is won */
		else
		{
			printf ("Sorry, you lost! The word was %s.\n", sGame.word);
		} /* if game is not won */
		free ((void *) sGame.word);	// Free the allocated space used by the word

		// Prompt user for whether to play again
		while (userChoice != 'Y' && userChoice != 'y'
					&& userChoice != 'N' && userChoice != 'n')
		{
			printf ("Play again? (Y/N): ");
			scanf (" %c", &userChoice);
		} /* while user hasn't selected 'Y', 'y', 'N', or 'n' */
		if (userChoice == 'N' || userChoice == 'n')
		{
			bEndProgram = true;
		} /* if user selected 'N' or 'n' */
	} /* While program isn't ended */

	return 0;
} /* end main loop */
