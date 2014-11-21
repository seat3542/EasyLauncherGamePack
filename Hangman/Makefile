CC=gcc
CFLAGS=-Wall -g

.PHONY: all 

all: bin/hangman

bin/hangman: bin/hangman.o
	${CC} ${CFLAGS} bin/hangman.o -o bin/hangman

bin/hangman.o: src/hangman.c include/hangman.h
	${CC} ${CFLAGS} -c src/hangman.c -o bin/hangman.o
	
clean:
	rm bin/*.o bin/hangman