CIMG_DEPS=-lm -lpthread -lX11
OBJ = main.o unravel_convol.o convol.o dual_convol.o naive_convol.o triple_convol.o filters.o linear_convol.o

all: $(OBJ)
	g++ -o run -g $(OBJ) $(CIMG_DEPS)

%.o : %.cpp
	g++ -c -o $@ $<

clean:
	rm *.o
