#include "TankPlayed.h"

using namespace std;

TankPlayed::TankPlayed(Tank* t){
	m_idnation=t->m_idnation;
	m_idtank=t->m_idtank;
	m_type=t->m_type;
	m_last=t->m_last;
	m_tier=t->m_tier;
	m_name=new string(*t->m_name);
	delete t;
}

string TankPlayed::toString(){
	string s = Tank::toString();
	s+=" ";
	s+=m_datas.toString();
	return s;
}

void TankPlayed::validate(){
	m_datas.parse();
}

void TankPlayed::addData(unsigned char data){
	m_datas.addData(data);
}
