C_FLAGS:=-finstrument-functions -fPIC #-g

main: main.o libtest.so libdecorator.so
	gcc -o main main.o -rdynamic -L. -ltest -ldecorator

main.o: main.c
	gcc -c main.c ${C_FLAGS} -rdynamic

libtest.so: test.c
	gcc --shared -o libtest.so test.c ${C_FLAGS} -rdynamic

libdecorator.so: decorator.c
	gcc --shared -o libdecorator.so decorator.c

clean:
	rm *.o
	rm *.so
	rm main

run: main
	LD_LIBRARY_PATH=. ./main
