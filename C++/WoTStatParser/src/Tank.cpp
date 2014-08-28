#include "Tank.h"

using namespace std;

Tank::Tank(){

}

Tank::Tank(string *nom, int idtank, int type, int tier, int idnation, long last){
	m_name=nom;
	m_type=type;
	m_tier=tier;
	m_last=last;
	m_idtank=idtank;
	m_idnation=idnation;
}

Tank::~Tank(){
	delete m_name;
}

string Tank::toString(){
	string s(*m_name);
	/*s+=" nation : "+showNation(m_idnation)+" type : "+showType(m_type);
	s+=" tier : "+getTier(m_tier);
	s+=" last : "+toTime(m_last);*/

	return s;
}

void Tank::setLast(long last){
	m_last=last;
}

void Tank::setNation(int nation){
	m_idnation=nation;
}

string Tank::toTime(long l){
	time_t time = l;
	return ctime(&time);
}

string Tank::getTier(int tier){
	string s;
	switch(tier){
		case 1:
			s="I";
			break;
		case 2:
			s="II";
			break;
		case 3:
			s="III";
			break;
		case 4:
			s="IV";
			break;
		case 5:
			s="V";
			break;
		case 6:
			s="VI";
			break;
		case 7:
			s="VII";
			break;
		case 8:
			s="VIII";
			break;
		case 9:
			s="IX";
			break;
		case 10:
			s="X";
			break;
	}
	return s;
}

string Tank::showNation(int idnation){
	string s;
	switch(idnation){
		case 0:
			s="URSS";
			break;

		case 1:
			s="Allemagne";
			break;

		case 2:
			s="USA";
			break;
	
		case 3:
			s="China";
			break;
	
		case 4:
			s="France";
			break;

		case 5:
			s="Anglais";
			break;
	}
	return s;
}

string Tank::showType(int type){
	string s;
	switch(type){
		case 0:
			s="Light Tank";
			break;

		case 1:
			s="Medium Tank";
			break;

		case 2:
			s="Heavy Tank";
			break;
		
		case 3:
			s="TD";
			break;

		case 4:
			s="SPG";
			break;
	}
	return s;
}
