CC = g++ -std=c++11 -g
CFLAGS = -Wall -g
IFLAGS = -Iheaders
OPATH = obj/

vpath %.h headers
vpath %.cpp src
vpath %.o obj

main : main.o chromosome.o gene.o
	$(CC) $(CFLAGS) -o main $(OPATH)main.o $(OPATH)chromosome.o $(OPATH)gene.o

gene.o : gene.h gene.cpp
chromosome.o : chromosome.h chromosome.cpp gene.o

%.o : %.cpp
	$(CC) -c $< $(IFLAGS)
	mv $@ $(OPATH)

clean :
	rm $(OPATH)*.o
