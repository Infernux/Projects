#CFLAGS=-g

main: main.o interpolate.o image_processing.o
	gcc -o main main.o interpolate.o image_processing.o

main.o: main.c
	gcc -c main.c $(CFLAGS)

interpolate.o: interpolate.c interpolate.h
	gcc -c interpolate.c $(CFLAGS)

image_processing.o: image_processing.c image_processing.c
	gcc -c image_processing.c $(CFLAGS)

test: test.o interpolate.o image_processing.o
	g++ -o test test.o interpolate.o image_processing.o -lgtest

test.o: test.c
	g++ -c test.c

clean:
	rm *.o
