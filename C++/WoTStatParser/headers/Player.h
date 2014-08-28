#ifndef __PLAYER_H
#define __PLAYER_H

#include <vector>
#include <python2.7/Python.h>
#include <string>
#include <iostream>
#include "TankPlayed.h"
#include "TankHelper.h"
#include "TankPlayed.h"

class Player
{
	public:
		Player(char* fichier);
		~Player();

		std::vector<TankPlayed*> tanks;
		Stats stats;
		unsigned int total;
	private:
		int hexToInt(char c);
		void python(char* fichier);
		void parse();
		void gatherDatas(TankPlayed *tank);
};

#endif
