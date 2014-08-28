#include "Datas.h"

using namespace std;

Datas::Datas()
{	
	series=NULL;
	battle=NULL;
	epic=NULL;
	major=NULL;
	special=NULL;
	clan=NULL;
	company=NULL;

	m_datas=NULL;
}

Datas::~Datas()
{
	if(m_datas!=NULL){
		freeVector();
		delete m_datas;
	}
	if(series!=NULL)
		delete series;
	if(battle!=NULL)
		delete battle;
	if(epic!=NULL)
		delete epic;
	if(major!=NULL)
		delete major;
	if(special!=NULL)
		delete special;
	if(company!=NULL)
		delete company;
	if(clan!=NULL)
		delete clan;

	freeKills();
}

void Datas::initDatas(){
	randomData.maxKills=0;
	randomData.maxXP=0;
	randomData.totalXP=0;	
	randomData.battleCount=0;
	randomData.wins=0;
	randomData.losses=0;
	randomData.survivedBattles=0;
	randomData.winAndSurvived=0;
	randomData.frags=0, randomData.frags8p=0, randomData.fragsBeast=0;
	randomData.shots=0;
	randomData.hits=0;
	randomData.spotted=0;
	randomData.damageDealt=0;
	randomData.damageReceived=0;
	randomData.treeCut=0;
	randomData.capturePoints=0;
	randomData.decapPoints=0;
	
	if(series!=NULL){
		series->sniper=0;
		series->maxSniper=0;
		series->invincible=0;
		series->maxInvincible=0;
		series->dieHard=0;
		series->maxDieHard=0;
		series->killing=0;
		series->maxKilling=0;
		series->piercing=0;
		series->maxPiercing=0;
	}
	
	if(battle!=NULL){
		battle->battleHeroes=0;
		battle->fragsSinai=0;
		battle->warrior=0;
		battle->invader=0;
		battle->sniper=0;
		battle->defender=0;
		battle->steelWall=0;
		battle->supporter=0;
		battle->scout=0;
		battle->evileye=0;
	}

	if(major!=NULL){
		major->Kay=0;
		major->Carius=0;
		major->Knispel=0;
		major->Poppel=0;
		major->Abrams=0;
		major->LeClerc=0;
		major->Lavrinenko=0;
		major->Ekins=0;
	}

	if(epic!=NULL){
		epic->Wittman=0;
		epic->Orlik=0;
		epic->Oskin=0;
		epic->Halonen=0;
		epic->Burda=0;
		epic->Billotte=0;
		epic->Kolobanov=0;
		epic->Fadin=0;
		epic->RadleyWaters=0;
		epic->BrunoPietro=0;
		epic->Tarczay=0;
		epic->Pascucci=0;
		epic->Dumitru=0;
		epic->Lehvaslaiho=0;
		epic->Nikolas=0;
		epic->LaFayettePools=0;
		epic->BrotherInArms=0;
		epic->CrucialContribution=0;
		epic->DeLanglade=0;
		epic->TamadaYoshio=0;
		epic->bombardier=0;
		epic->huntsman=0;
		epic->alaric=0;
		epic->sturdy=0;
		epic->ironMan=0;
		epic->luckyDevil=0;
	}
}

void Datas::addData(unsigned char data)
{
	if(m_datas==NULL){
		m_datas=new vector<unsigned char>();
	}
	m_datas->push_back(data);
}

void Datas::parseRandom(){
	randomData.maxKills=get(10, 1);
	randomData.totalXP=get(11, 4);
	randomData.maxXP=get(15, 2);
	randomData.battleCount=get(17, 4);
	randomData.wins=get(21, 4);
	randomData.losses=get(25, 4);
	randomData.survivedBattles=get(29, 4);
	randomData.winAndSurvived=get(33, 4);
	randomData.frags=get(37, 4);
	randomData.frags8p=get(41, 4); //frags > tier VIII
	randomData.fragsBeast=get(45, 4);
	randomData.shots=get(49, 4);
	randomData.hits=get(53, 4);
	randomData.spotted=get(57, 4);
	randomData.damageDealt=get(61, 4);
	randomData.damageReceived=get(65, 4);
	randomData.treeCut=get(69, 2); //WTF
	randomData.capturePoints=get(71, 4);
	randomData.decapPoints=get(75, 4);	
}

void Datas::parseSeries(){
	series->sniper=get(79, 2);
	series->maxSniper=get(81, 2);
	series->invincible=get(83, 1);
	series->maxInvincible=get(84, 1);
	series->dieHard=get(85, 1);
	series->maxDieHard=get(86, 1);
	series->killing=get(87, 1);
	series->maxKilling=get(88, 1);
	series->piercing=get(89, 1);
	series->maxPiercing=get(90, 1);
}

void Datas::parseBattlePre20(){
	battle->battleHeroes=get(91, 2);
	battle->fragsSinai=get(93, 4);
	battle->warrior=get(97 ,2);
	battle->invader=get(99, 2);
	battle->sniper=get(101, 2);
	battle->defender=get(103, 2);
	battle->steelWall=get(105, 2);
	battle->supporter=get(107, 2);
}

void Datas::parseBattlePost20(){
	parseBattlePre20();
	battle->scout=get(109 ,2);
	battle->evileye=get(111, 2);
}

void Datas::parseMajorPre20(){
	major->Kay=get(109, 1);
	major->Carius=get(110, 1);
	major->Knispel=get(111, 1);
	major->Poppel=get(112, 1);
	major->Abrams=get(113, 1);
	major->LeClerc=get(114, 1);
	major->Lavrinenko=get(115, 1);
	major->Ekins=get(116, 1);
}

void Datas::parseMajorPost20(){
	major->Kay=get(113, 1);
	major->Carius=get(114, 1);
	major->Knispel=get(115, 1);
	major->Poppel=get(116, 1);
	major->Abrams=get(117, 1);
	major->LeClerc=get(118, 1);
	major->Lavrinenko=get(119, 1);
	major->Ekins=get(120, 1);
}

void Datas::parseEpic20(){
	epic->Boelter=get(117, 2); //boelter
	epic->Orlik=get(119, 2);
	epic->Oskin=get(121, 2);
	epic->Halonen=get(123, 2);
	epic->Burda=get(125, 2);
	epic->Billotte=get(127, 2);
	epic->Kolobanov=get(129, 2);
	epic->Fadin=get(131, 2);
	special->heroesOfRassenay=get(133, 2);
	epic->DeLaglanda=get(135, 2);
	epic->TamadaYoshio=get(137, 2);
	epic->Erohin=get(139, 2);
	epic->Horoshilov=get(141, 2);
	epic->Lister=get(143, 2);
}

void Datas::parseEpicPre24(){
	epic->Wittman=get(121, 2);
	epic->Orlik=get(123, 2);
	epic->Oskin=get(125, 2);
	epic->Halonen=get(127, 2);
	epic->Burda=get(129, 2);
	epic->Billotte=get(131, 2);
	epic->Kolobanov=get(133, 2);
	epic->Fadin=get(135, 2);
	epic->RadleyWaters=get(137, 2);
	epic->BrunoPietro=get(139, 2);
	epic->Tarczay=get(141, 2);
	epic->Pascucci=get(143, 2);
	epic->Dumitru=get(145, 2);
	epic->Lehvaslaiho=get(147, 2);
	epic->Nikolas=get(149, 2);
	epic->LaFayettePools=get(151, 2);
}

void Datas::parseEpic24(){
	parseEpicPre24();
	epic->BrotherInArms=get(278, 2);
	epic->CrucialContribution=get(280, 2);
}

void Datas::parseEpicPost24(){
	parseEpic24();
	epic->DeLanglade=get(282, 2);
	epic->TamadaYoshio=get(284, 2);
	epic->bombardier=get(286, 2);
	epic->huntsman=get(288, 2);
	epic->alaric=get(290, 2);
	epic->sturdy=get(292, 2);
	epic->ironMan=get(294, 2);
	epic->luckyDevil=get(296, 2);
}

void Datas::parseSpecialPre22(){
	special->beastHunter=get(145, 2);
	special->mouseBane=get(147, 2);
	special->tankExpertStrg=get(149, 1);
	special->titleSniper=get(150, 1);
	special->invincible=get(151, 1);
	special->dieHard=get(152, 1);
	special->raider=get(153, 2);
	special->handOfDeath=get(155, 1);
	special->armorPiercer=get(156, 1);
	special->kamikaze=get(157, 2);
	special->lumberjack=get(159, 1);
	special->markOfMastery=get(160, 1);
}

void Datas::parseSpecialPost22(){
	special->Sinai=get(153, 2);
	special->heroesOfRassenay=get(155, 2);
	special->beastHunter=get(157, 2);
	special->mouseBane=get(159, 2);
	special->tankExpertStrg=get(161, 2);
	special->titleSniper=get(163, 1);
	special->invincible=get(164, 1);
	special->dieHard=get(165, 1);
	special->raider=get(166, 2);
	special->handOfDeath=get(168, 1);
	special->armorPiercer=get(169, 1);
	special->kamikaze=get(170, 2);
	special->lumberjack=get(172, 1);
	special->markOfMastery=get(173, 1);
}

void Datas::parseCompany20(){
	company->totalXP=get(161, 4);
	company->battleCount=get(165, 4);
	company->wins=get(169, 4);
	company->losses=get(173, 4);
	company->survivedBattles=get(177, 4);
	company->frags=get(181, 4);
	company->shots=get(185, 4);
	company->hits=get(189, 4);
	company->spotted=get(193, 4);
	company->damageDealt=get(197, 4);
	company->damageReceived=get(201, 4);
	company->capturePoints=get(205, 4);
	company->decapPoints=get(209, 4);
}

void Datas::parseCompanyPost20(){
	company->totalXP=get(174, 4);
	company->battleCount=get(178, 4);
	company->wins=get(182, 4);
	company->losses=get(186, 4);
	company->survivedBattles=get(190, 4);
	company->frags=get(194, 4);
	company->shots=get(198, 4);
	company->hits=get(202, 4);
	company->spotted=get(206, 4);
	company->damageDealt=get(210, 4);
	company->damageReceived=get(214, 4);
	company->capturePoints=get(218, 4);
	company->decapPoints=get(222, 4);
}

void Datas::parseClan20(){
	clan->totalXP=get(213, 4);
	clan->battleCount=get(217, 4);
	clan->wins=get(221, 4);
	clan->losses=get(225, 4);
	clan->survivedBattles=get(229, 4);
	clan->frags=get(233, 4);
	clan->shots=get(237, 4);
	clan->hits=get(241, 4);
	clan->spotted=get(245, 4);
	clan->damageDealt=get(249, 4);
	clan->damageReceived=get(253, 4);
	clan->capturePoints=get(257, 4);
	clan->decapPoints=get(261, 4);
}

void Datas::parseClanPost20(){
	clan->totalXP=get(226, 4);
	clan->battleCount=get(230, 4);
	clan->wins=get(234, 4);
	clan->losses=get(238, 4);
	clan->survivedBattles=get(242, 4);
	clan->frags=get(246, 4);
	clan->shots=get(250, 4);
	clan->hits=get(254, 4);
	clan->spotted=get(258, 4);
	clan->damageDealt=get(262, 4);
	clan->damageReceived=get(266, 4);
	clan->capturePoints=get(270, 4);
	clan->decapPoints=get(274, 4);
}

void Datas::parseKills(unsigned int offset){
	TankHelper th;
	unsigned int nb = get(offset+2, 2);
	offset+=4;

	unsigned int startId=offset;
	unsigned int startNb=4*nb+offset;

	for(unsigned int i=0; i<nb; ++i){
		//6 octets d'information par char
		int id = get(startId, 2);
		startId+=4;
		int idtank = id/256;
		int idnation = ((id-idtank*256)-1)/16;

		unsigned int nbKills = get(startNb, 2);
		startNb+=2;

		Tank* t = th.get(idnation, idtank);
		TankKilled *k = new TankKilled(t, nbKills);
		kills.push_back(k);
		delete t;
	}
}

void Datas::showRest(unsigned int offset){
	printf("<");
	for(unsigned int i=offset; i<m_datas->size(); ++i){
		printf("%x|", get(i, 1));
	}
	printf(">");
}

void Datas::parse()
{
	if(m_datas==NULL){
		return;
	}

	m_version = get(0, 1);

	switch(m_version){
		case 26:
			epic=new Epic;
			major=new Major;
			battle=new Battle;
			series=new Series;
			special=new Special;
			company=new Company;
			clan=new Clan;
			initDatas();

			parseEpicPost24();
			parseMajorPost20();
			parseBattlePost20();
			parseSeries();
			parseSpecialPost22();
			parseCompanyPost20();
			parseClanPost20();
			parseKills(304);
			//showRest(304);
			break;

		case 24:
			epic=new Epic;
			major=new Major;
			battle=new Battle;
			series=new Series;
			special=new Special;
			company=new Company;
			clan=new Clan;
			initDatas();

			parseEpic24();
			parseMajorPost20();
			parseBattlePost20();
			parseSeries();
			parseSpecialPost22();
			parseCompanyPost20();
			parseClanPost20();
			parseKills(298);
			//showRest(298);
			break;
		
		case 22:
			major=new Major;
			battle=new Battle;
			series=new Series;
			special=new Special;
			company=new Company;
			clan=new Clan;
			initDatas();

			parseSeries();
			parseMajorPost20();
			parseBattlePost20();
			parseSpecialPost22();
			parseCompanyPost20();
			parseClanPost20();
			parseKills(278);
			//showRest(278);
			break;
		
		case 20:
			battle=new Battle;
			series=new Series;
			special=new Special;
			company=new Company;
			clan=new Clan;
			initDatas();

			parseSeries();
			parseBattlePre20();
			parseSpecialPre22();
			parseCompany20();
			parseClan20();
			parseKills(265);
			//showRest(265);
			break;

		case 18:
			parseKills(138);
			//showRest(138);
			break;
	}
	parseRandom();

	freeVector();
}

void Datas::freeVector(){
	m_datas->clear();
	delete m_datas;
	m_datas=NULL;
}

void Datas::freeKills(){
	for(int i=0; i<kills.size(); ++i){
		delete kills[i];
	}
}

string Datas::toString(){
	string res;
	char s[10]="";
	sprintf(s, "%d", randomData.maxKills);
	res="Max kills : ";
	res+=s;
	sprintf(s, "%d", randomData.totalXP);
	res+=" XP Total : ";
	res+=s;
	sprintf(s, "%d", randomData.maxXP);
	res+=" Max XP : ";
	res+=s;
	sprintf(s, "%d", randomData.battleCount);
	res+=" Battle Count : ";
	res+=s;
	sprintf(s, "%d", randomData.wins);
	res+=" Win Count : ";
	res+=s;
	sprintf(s, "%d", randomData.losses);
	res+=" Loose Count : ";
	res+=s;
	res+=" ";
	for(unsigned int j=0; j<kills.size(); ++j){
		res+=kills[j]->toString();
		res+="|";
	}
	return res;	
}

unsigned int Datas::get(int offset, int length){
	unsigned int res = 0;
	//if(m_datas!=NULL && offset<m_datas->size()){
	if(m_datas!=NULL){
		res=(*m_datas)[offset];
		for(int i=1; i<length; ++i){
			if((offset+i)<m_datas->size()){
				res+=(*m_datas)[offset+i]*(pow(256, i));
			}else{
				return 0;
			}
		}
	}
	return res;
}
