CIMG_DEPS=-lm -lpthread -lX11

all: unravel_convol.o convol.o dual_convol.o naive_convol.o
	g++ -o run -g convol.o unravel_convol.o dual_convol.o naive_convol.o $(CIMG_DEPS)

%.o : %.cpp
	g++ -c -o $@ $<

clean:
	rm *.o
