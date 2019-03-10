CFLAGS=-Wall -Werror -g -O0 -Wno-unused-command-line-argument

main: main.o utils.o
	$(CC) -o main main.o utils.o

main.o: main.c
	$(CC) -c main.c $(CFLAGS)

utils.o: utils.c
	$(CC) -c utils.c $(CFLAGS)

clean:
	rm *.o
