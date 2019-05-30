.PHONY: clean

OBJECTS=ppm_reader.o utils.o drawing_cairo.o file_readers.o
CFLAGS=-O2
LIBS=-lcairo -lX11
EXEC=ppm_reader

ppm_reader: $(OBJECTS)
	$(CC) -o $(EXEC) $? $(LIBS)

ppm_reader.o: ppm_reader.c
	$(CC) -c $< $(CFLAGS)

utils.o: utils.c utils.h
	$(CC) -c $< $(CFLAGS)

drawing_cairo.o: drawing_cairo.c drawing_cairo.h
	$(CC) -c $< $(CFLAGS)

file_readers.o: file_readers.c file_readers.h
	$(CC) -c $< $(CFLAGS)

clean:
	rm -rf *.o
