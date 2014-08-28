#include "TankHelper.h"

using namespace std;

TankHelper::TankHelper() : germany("datas/germany.dat"), urss("datas/urss.dat"), usa("datas/usa.dat"), france("datas/france.dat"), gb("datas/gb.dat"), china("datas/china.dat")
{
}

TankHelper::~TankHelper(){
}

Tank* TankHelper::get(int nation, int idtank){
	Tank* tank;
	switch(nation){
		case 0:
			//urss
			tank = urss.get(idtank);
			break;
		case 1:
			//germany
			tank = germany.get(idtank);
			break;
		case 2:
			//usa
			tank = usa.get(idtank);
			break;
		case 3:
			//china
			tank = china.get(idtank);
			break;
		case 4:
			//france
			tank = france.get(idtank);
			break;
		case 5:
			//anglais
			tank = gb.get(idtank);
			break;
	}
	tank->setNation(nation);
	return tank;
}
