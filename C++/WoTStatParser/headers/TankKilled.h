#ifndef __TANKKILLED_H
#define __TANKKILLED_H

#include <iostream>
#include <string>
#include "Tank.h"

class TankKilled : public Tank
{
	public:
		TankKilled(Tank* t, int killed);
		std::string toString();

		unsigned int timeKilled;
};

#endif
