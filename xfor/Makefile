main : main.c
	gcc-4.7 -g -Wall -o main main.c xfor.h -std=c99 -fextended-identifiers -Wno-trigraphs -DSKIP_UNIVERSAL_UTF8 -DSKIP_EVALUATED_COMMA_ASSIGN

macro : main.c
	gcc-4.7 -E -Wall -o main main.c -std=c99 -fextended-identifiers -Wno-trigraphs -DSKIP_UNIVERSAL_UTF8 -DSKIP_EVALUATED_COMMA_ASSIGN

launch : main
	./main
