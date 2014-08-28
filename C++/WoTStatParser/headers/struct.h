#ifndef __STRUCT_H
#define __STRUCT_H

typedef struct random{
	unsigned int maxKills;
	unsigned int maxXP;
	unsigned int totalXP;	
	unsigned int battleCount;
	unsigned int wins;
	unsigned int losses;
	unsigned int survivedBattles;
	unsigned int winAndSurvived;
	unsigned int frags;
	unsigned int frags8p;
	unsigned int fragsBeast;
	unsigned int shots;
	unsigned int hits;
	unsigned int spotted;
	unsigned int damageDealt;
	unsigned int damageReceived;
	unsigned int treeCut;
	unsigned int capturePoints;
	unsigned int decapPoints;
}RandomData, Stats;

typedef struct series{
	unsigned short sniper;
	unsigned short maxSniper;
	unsigned char invincible;
	unsigned char maxInvincible;
	unsigned char dieHard;
	unsigned char maxDieHard;
	unsigned char killing;
	unsigned char maxKilling;
	unsigned char piercing;
	unsigned char maxPiercing;
}Series;

typedef struct battle{
	unsigned short battleHeroes;
	unsigned int fragsSinai;
	unsigned short warrior;
	unsigned short invader;
	unsigned short sniper;
	unsigned short defender;
	unsigned short steelWall;
	unsigned short supporter;
	unsigned short scout;
	unsigned short evileye;
}Battle;

typedef struct major{
	unsigned char Kay;
	unsigned char Carius;
	unsigned char Knispel;
	unsigned char Poppel;
	unsigned char Abrams;
	unsigned char LeClerc;
	unsigned char Lavrinenko;
	unsigned char Ekins;
}Major;

typedef struct epic{
	union{
		unsigned short Wittman;
		unsigned short Boelter;
	};
	unsigned short Orlik;
	unsigned short Oskin;
	unsigned short Halonen;
	unsigned short Burda;
	unsigned short Billotte;
	unsigned short Kolobanov;
	unsigned short Fadin;
	unsigned short RadleyWaters;
	unsigned short DeLaglanda;
	union{
		unsigned short BrunoPietro;
		unsigned short Erohin;
	};
	union{
		unsigned short Tarczay;
		unsigned short Horoshilov;
	};
	union{
		unsigned short Pascucci;
		unsigned short Lister;
	};
	unsigned short Dumitru;
	unsigned short Lehvaslaiho;
	unsigned short Nikolas;
	unsigned short LaFayettePools;
	unsigned short BrotherInArms;
	unsigned short CrucialContribution;
	unsigned short DeLanglade;
	unsigned short TamadaYoshio;
	unsigned short bombardier;
	unsigned short huntsman;
	unsigned short alaric;
	unsigned short sturdy;
	unsigned short ironMan;
	unsigned short luckyDevil;
}Epic;

typedef struct special{
	unsigned short Sinai;
	unsigned short heroesOfRassenay;
	unsigned short beastHunter;
	unsigned short mouseBane;
	unsigned short tankExpertStrg;
	unsigned char titleSniper;
	unsigned char invincible;
	unsigned char dieHard;
	unsigned short raider;
	unsigned short handOfDeath;
	unsigned char armorPiercer;
	unsigned short kamikaze;
	unsigned char lumberjack;
	unsigned char markOfMastery;
}Special;

typedef struct company{
	unsigned int totalXP;	
	unsigned int battleCount;
	unsigned int wins;
	unsigned int losses;
	unsigned int survivedBattles;
	unsigned int frags;
	unsigned int shots;
	unsigned int hits;
	unsigned int spotted;
	unsigned int damageDealt;
	unsigned int damageReceived;
	unsigned int capturePoints;
	unsigned int decapPoints;
}Company;

typedef struct clan{
	unsigned int totalXP;	
	unsigned int battleCount;
	unsigned int wins;
	unsigned int losses;
	unsigned int survivedBattles;
	unsigned int frags;
	unsigned int shots;
	unsigned int hits;
	unsigned int spotted;
	unsigned int damageDealt;
	unsigned int damageReceived;
	unsigned int capturePoints;
	unsigned int decapPoints;
}Clan;

#endif
