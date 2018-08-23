CIMG_DEPS=-lm -lpthread -lX11

all: unravel_convol.o convol.o dual_convol.o
	g++ -o run -g convol.o unravel_convol.o dual_convol.o $(CIMG_DEPS)

convol.o: convol.cpp
	g++ -c convol.cpp

unravel_convol.o : unravel_convol.cpp
	g++ -c unravel_convol.cpp

dual_convol.o : dual_convol.cpp
	g++ -c dual_convol.cpp

clean:
	rm *.o
