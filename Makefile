ifeq ($(OS),Windows_NT)
	RM = del /Q
else
	RM = rm -f
endif

# -lpthread
CC = g++
CFLAGS = -g -std=c++11 -Wall
FILES = num_game.cpp num_game.h

numgame: $(FILES)
	$(CC) $(CFLAGS) $(FILES) -o numgame

default:
	numgame

clean:
	$(RM) numgame numgame.exe