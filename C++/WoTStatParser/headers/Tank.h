#ifndef __TANK_H
#define __TANK_H

#include <string>
#include <cstdio>
#include <cstdlib>
#include <vector>

#include <iostream>

class Tank
{
	public:
		Tank(std::string *nom, int idtank, int type, int tier, int idnation=-1, long last=-1);
		Tank();
		~Tank();
		std::string toString();
		void setLast(long last);
		void setNation(int nation);

	//protected:
		//attributs
		std::string *m_name;

		int m_idnation;
		int m_idtank;
		int m_type;
		long m_last;
		int m_tier;

	private:
		std::string toTime(long l);
		std::string showNation(int idnation);
		std::string showType(int type);
		std::string getTier(int tier);

};

#endif
