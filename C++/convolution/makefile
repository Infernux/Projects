#CC=g++
#OPTIONS=-mavx
#CC=aarch64-linux-gnu-g++

CIMG_DEPS=-lm -lstdc++
CIMG_DEPS_X86=-lm -lpthread -lX11
#OBJ = main.o unravel_convol.o convol.o dual_convol.o naive_convol.o triple_convol.o filters.o linear_convol.o
OBJ = main.o convol.o dual_convol.o filters.o 
OBJ_X86 = main.o unravel_convol.o convol.o dual_convol.o naive_convol.o triple_convol.o filters.o linear_convol.o avx_convol.o

all: $(OBJ)
	$(CC) -o run -g $(OBJ) $(CIMG_DEPS)

%.o : %.cpp
	$(CC) -g -c -o $@ $< $(OPTIONS)

clean:
	rm *.o
