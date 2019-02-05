#CC=g++
#OPTIONS=-mavx

OBJ = main.o

all: $(OBJ)
	$(CXX) -o run -g $(OBJ) -fPIE -pie -lstdc++

%.o : %.cpp
	$(CXX) -g -c -o $@ $< $(OPTIONS)

clean:
	rm *.o

copy: run
	adb push run /data/local/tmp/

run: copy
	adb shell "chmod +x /data/local/tmp/run; LD_LIBRARY_PATH=/data/local/tmp/ /data/local/tmp/run"
