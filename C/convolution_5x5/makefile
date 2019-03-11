CFLAGS=-Wall -Werror -g -O0 -Wno-unused-command-line-argument

main: main.o utils.o neon_impl.o
	$(CC) -o main main.o utils.o neon_impl.o

main.o: main.c
	$(CC) -c main.c $(CFLAGS) $(COMPILER_SPECIFIC)

utils.o: utils.c
	$(CC) -c utils.c $(CFLAGS) $(COMPILER_SPECIFIC)

neon_impl.o: neon_impl.c neon_impl.h
	$(CC) -c neon_impl.c $(CFLAGS) $(COMPILER_SPECIFIC)

clean:
	rm *.o
