#ifndef __TANKPLAYED_H
#define __TANKPLAYED_H

#include <iostream>
#include <string>
#include "Tank.h"
#include "Datas.h"

class TankPlayed : public Tank
{
	public:
		TankPlayed(Tank *t);
		void validate();
		void addData(unsigned char data);
		std::string toString();

		Datas m_datas;
};

#endif
