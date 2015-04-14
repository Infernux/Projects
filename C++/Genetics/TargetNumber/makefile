CC = g++
CFLAGS = -Wall
IFLAGS = -Iheaders
OPATH = obj/

vpath %.h headers
vpath %.cpp src
vpath %.o obj

main : main.o
	$(CC) -g -o main main.o

%.o : %.cpp
	$(CC) -c $<

clean :
	rm *.o
