#ifndef __DATAS_H
#define __DATAS_H

#include <vector>
#include <cstring>
#include <string>
#include <cstdio>
#include <cmath>

#include "struct.h"
#include "TankKilled.h"
#include "TankHelper.h"

class Datas
{
	public:
		Datas();
		~Datas();
		void addData(unsigned char data);
		void parse();
		unsigned int get(int offset, int length=1);
		std::string toString();
		void showRest(unsigned int offset);

		RandomData randomData;
		Series *series;
		Battle *battle;
		Epic *epic;
		Major *major;
		Special *special;
		Company *company;
		Clan *clan;
		std::vector<TankKilled*> kills;

	private:
		void initDatas();
		void parseRandom();
		void parseSeries();
		void parseBattlePre20();
		void parseBattlePost20();
		void parseMajorPre20();
		void parseMajorPost20();
		void parseEpic20();
		void parseEpicPre24();
		void parseEpic24();
		void parseEpicPost24();
		void parseSpecialPre22();
		void parseSpecialPost22();
		void parseCompany20();
		void parseCompanyPost20();
		void parseClan20();
		void parseClanPost20();
		void parseKills(unsigned int offset);

		unsigned char m_version;
		std::vector<unsigned char> *m_datas;
		void freeVector();
		void freeKills();
};

#endif
