#ifndef __SMART_H
#define __SMART_H

#include <string>
#include <cstdio>
#include <iostream>
#include "Tank.h"

class SmartIterator
{
	public:
		SmartIterator(char* name);
		~SmartIterator();
		Tank* get(int idtank);
	private:
		FILE* fd;
		int index;
};

#endif
