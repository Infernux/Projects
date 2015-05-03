CC = g++ -std=c++11 -g
CFLAGS = -Wall -g
IFLAGS = -Iheaders
OPATH = obj/

vpath %.h headers
vpath %.cpp src
vpath %.o obj

main : main.o chromosome.o gene.o picker.o constants.h
	$(CC) $(CFLAGS) -o main $(OPATH)main.o $(OPATH)chromosome.o $(OPATH)gene.o $(OPATH)picker.o

gene.o : gene.h gene.cpp constants.h
chromosome.o : chromosome.h chromosome.cpp gene.o constants.h
picker.o : picker.cpp picker.h constants.h

%.o : %.cpp constants.h
	$(CC) -c $< $(IFLAGS)
	mv $@ $(OPATH)

clean :
	rm $(OPATH)*.o
