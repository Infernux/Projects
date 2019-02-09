main: main.o interpolate.o
	g++ -o main main.o interpolate.o -lgtest

main.o: main.c
	g++ -c main.c

interpolate.o: interpolate.c interpolate.h
	g++ -c interpolate.c

clean:
	rm *.o
