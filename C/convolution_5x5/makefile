#DEBUG=-DRANDOM_VALS
#DEBUG+=-DPRINT_DIFF
CFLAGS=-Wall -Werror -Wno-unused-command-line-argument -g -O2

main: main.o utils.o neon_impl.o
	$(CC) -o main main.o utils.o neon_impl.o

main.o: main.c
	$(CC) -c main.c $(CFLAGS) $(COMPILER_SPECIFIC)

utils.o: utils.c
	$(CC) -c utils.c $(CFLAGS) $(COMPILER_SPECIFIC) $(DEBUG)

neon_impl.o: neon_impl.c neon_impl.h
	$(CC) -c neon_impl.c $(CFLAGS) $(COMPILER_SPECIFIC)

clean:
	rm *.o
