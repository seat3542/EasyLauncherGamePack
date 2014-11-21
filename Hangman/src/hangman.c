#include "../include/hangman.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define filename "../data/words.txt"

void initializeAlphabet (Alphabet sAlphabet[], char *word, int wordlength)
{
	int i = 0;
	int j = 0;
	for (i = 0; i < 26; i++)
	{
		sAlphabet[i].letter = 65 + i;
		sAlphabet[i].bGuessed = false;
		sAlphabet[i].bInWord = false;
		for (j = 0; j < wordlength; j++)
		{
			if (sAlphabet[i].letter == word[j])
			{
				sAlphabet[i].bInWord = true;
			}
		}
	}
}

void setupPictures (Hangman *psGame)
{
	strcpy(psGame->pictures[0], "Placeholder 0\n");
	strcpy(psGame->pictures[1], "Placeholder 1\n");
	strcpy(psGame->pictures[2], "Placeholder 2\n");
	strcpy(psGame->pictures[3], "Placeholder 3\n");
	strcpy(psGame->pictures[4], "Placeholder 4\n");
	strcpy(psGame->pictures[5], "Placeholder 5\n");
	strcpy(psGame->pictures[6], "Placeholder 6\n");
	strcpy(psGame->pictures[7], "Placeholder 7\n");
}

/*void printPicture (char *pictures, int which)
{

}*/

void chooseWord (char **word, int *wordLength)
{
	FILE *pInputFile;
	int numWords;
	int chosen;
	int i = 0;

	pInputFile = fopen (filename, "r");
	if (NULL == pInputFile)
	{
		printf ("ERROR: File not found!\n");
		exit (EXIT_FAILURE);
	}
	fscanf (pInputFile, "%i\n", &numWords);
	chosen = 1 + (rand () % numWords);
	for (i = 0; i < chosen; i++)
	{
		fscanf (pInputFile, "%i ", wordLength);
		*word = (char *) malloc (sizeof(char) * *wordLength);
		fscanf (pInputFile, "%s\n", *word);
		if (i != chosen - 1)
		{
			free ((void *) *word);
		}
	}
	fclose (pInputFile);
}

void initializeGame (Hangman *psGame)
{
	psGame->word = NULL;
	psGame->wordLength = 0;
	psGame->hangingMan = 0;
	setupPictures (psGame);
	chooseWord (&(psGame->word), &(psGame->wordLength));
	initializeAlphabet (psGame->sAlphabet, psGame->word, psGame->wordLength);
}

void printGame (Hangman *psGame)
{
	int i = 0;

	printf ("%s\n", psGame->pictures[psGame->hangingMan]);
	for (i = 0; i < 26; i++)
	{
		if (psGame->sAlphabet[i].bGuessed == true
				&& psGame->sAlphabet[i].bInWord == false)
		{
			printf ("%c ", psGame->sAlphabet[i].letter);
		}
	}
	printf ("\n");
	for (i = 0; i < psGame->wordLength; i++)
	{
		if (psGame->sAlphabet[(psGame->word[i]) - 65].bGuessed == true)
		{
			printf ("%c", psGame->word[i]);
		}
		else
		{
			printf ("_");
		}
	}
	printf ("\n");
}

void takeTurn (Hangman *psGame)
{
	char letter = ' ';
	if (psGame->hangingMan < 7)
	{
		while ((letter < 'A' || letter > 'Z')
					&& psGame->sAlphabet[letter - 65].bGuessed == true)
		{
			printf ("Guess another letter: ");
			scanf ("%c", &letter);
			if (letter < 'z' && letter > 'a')
			{
				letter = letter - 32;
			}
		}
		psGame->sAlphabet[letter - 65].bGuessed = true;
		if (psGame->sAlphabet[letter - 65].bInWord == false)
		{
			psGame->hangingMan++;
		}
	}
}

int main ()
{
	Hangman sGame;

	initializeGame (&sGame);

	while (sGame.hangingMan < 7)
	{
		printf ("======================\n");
		printGame (&sGame);
		takeTurn (&sGame);
	}
	printf ("======================\n");
	printGame(&sGame);
	printf ("You've lost! The word was %s.\n", sGame.word);

	return 0;
}
