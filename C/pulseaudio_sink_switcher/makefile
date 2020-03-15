BIN=pss

CC=gcc
LD_FLAGS=-lpulse
BINARIES=main.o pa_helpers.o

$(BIN): $(BINARIES)
	$(CC) -o $(BIN) $(BINARIES) $(LD_FLAGS)

main.o: main.c
	$(CC) -c main.c

pa_helpers.o: pa_helpers.c pa_helpers.h
	$(CC) -c pa_helpers.c
