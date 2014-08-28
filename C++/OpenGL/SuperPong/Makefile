CC=g++
CFLAGS=-c -Wall
LDFLAGS=
LIBFLAGS=-lsfml-graphics -lsfml-window -lsfml-system -lGLU -lGL
#-lsfml-audio
SOURCES=$(wildcard *.cpp)
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=main

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@ $(LIBFLAGS)

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@ 
clean:
	rm *.o main
