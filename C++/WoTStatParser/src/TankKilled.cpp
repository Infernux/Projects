#include "TankKilled.h"

using namespace std;

TankKilled::TankKilled(Tank* t, int killed){
	m_idnation=t->m_idnation;
	m_idtank=t->m_idtank;
	m_type=t->m_type;
	m_last=t->m_last;
	m_tier=t->m_tier;
	m_name=new string(*t->m_name);
	timeKilled=killed;
}

string TankKilled::toString(){
	char s[10]="";
	string res = string(*m_name);
	sprintf(s, "%d", timeKilled);
	res+=" : ";
	res+=s;
	return res;
}
