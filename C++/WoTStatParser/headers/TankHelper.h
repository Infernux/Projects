#ifndef __TANKHELPER_H
#define __TANKHELPER_H

#include <string>
#include "SmartIterator.h"
#include "Tank.h"

class TankHelper
{
	public:
		TankHelper();
		~TankHelper();
		Tank* get(int nation, int idtank);
	private:
		SmartIterator germany;
		SmartIterator urss;
		SmartIterator usa;
		SmartIterator france;
		SmartIterator gb;
		SmartIterator china;
};

#endif
