CFLAGS=-Wall -Werror -g -O0

main: main.o utils.o
	gcc -o main main.o utils.o

main.o: main.c
	gcc -c main.c $(CFLAGS)

utils.o: utils.c
	gcc -c utils.c $(CFLAGS)

clean:
	rm *.o
