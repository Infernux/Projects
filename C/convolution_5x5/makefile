CFLAGS=-Wall -Werror -g -O0 -Wno-unused-command-line-argument

main: main.o utils.o neon_impl.o
	$(CC) -o main main.o utils.o neon_impl.o

main.o: main.c
	$(CC) -c main.c $(CFLAGS)

utils.o: utils.c
	$(CC) -c utils.c $(CFLAGS)

neon_impl.o: neon_impl.c neon_impl.h
	$(CC) -c neon_impl.c $(CFLAGS)

clean:
	rm *.o
