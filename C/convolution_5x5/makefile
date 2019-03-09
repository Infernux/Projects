main: main.o utils.o
	gcc -o main main.o utils.o

main.o: main.c
	gcc -c main.c -O0 -g

utils.o: utils.c
	gcc -c utils.c -O0 -g

clean:
	rm *.o
