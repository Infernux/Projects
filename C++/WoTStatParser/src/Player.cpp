#include "Player.h"

using namespace std;

Player::Player(char* fichier){
	total=0;
	stats.wins=0;
	stats.losses=0;
	stats.survivedBattles=0;
	//python(fichier);
	parse();
}

Player::~Player(){
	for(int i=0; i<tanks.size(); ++i){
		delete tanks[i];
	}
}

void Player::python(char* fichier){
	char* fd[1] = {fichier};
	FILE* fp = fopen("unPickle", "r");
	Py_Initialize();
	PySys_SetArgv(1, fd);
	PyRun_SimpleFile(fp, "unPickle");
	Py_Finalize();
	fclose(fp);	
}

int Player::hexToInt(char c){
	int res;
	switch(c){
		case 'a':
			res=10;
			break;
		case 'b':
			res=11;
			break;
		case 'c':
			res=12;
			break;
		case 'd':
			res=13;
			break;
		case 'e':
			res=14;
			break;
		case 'f':
			res=15;
			break;	
		default:
			res=c-'0';
			break;
	}
	return res;	
}

void Player::parse(){
	string s;
	FILE* cache = fopen("datas/cache.dat", "rb");
	TankHelper helper;

	unsigned char c;
	fseek(cache, sizeof(char)*10, SEEK_CUR);

	do{
		//id du char
		fread(&c, sizeof(char), 1, cache);
		while(c!=')'){
			s+=c;
			fread(&c, sizeof(char), 1, cache);
		}

		int id = atoi(s.c_str());
		int idtank = id/256;
		int idnation = ((id-idtank*256)-1)/16;
		s.erase();

		//dernière bataille
		fseek(cache, sizeof(char)*3, SEEK_CUR);

		fread(&c, sizeof(char), 1, cache);
		while(c!=','){
			s+=c;
			fread(&c, sizeof(char), 1, cache);
		}

		long last = atol(s.c_str());
		s.erase();
		
		TankPlayed* tank = new TankPlayed(helper.get(idnation, idtank));
		tank->setLast(last);
		tanks.push_back(tank);
		//cout << tank->toString() << endl;

		//datas
		unsigned char startchar;
		fseek(cache, sizeof(char), SEEK_CUR);
		fread(&startchar, sizeof(char), 1, cache);
		unsigned char c2;
		fread(&c, sizeof(char), 1, cache);
		while(c!=startchar){
			unsigned char val=-1;
			if(c=='\\'){//cas hexa
				fread(&c2, sizeof(char), 1, cache);
				if(c2=='x'){
					fread(&c, sizeof(char), 1, cache);
					val=hexToInt(c)*16;
					//printf("%c", c);
					fread(&c, sizeof(char), 1, cache);
					val+=hexToInt(c);
					//printf("%c|", c);
					tank->addData(val);
				}else if(c2=='\''){
					val=(int)'\'';
					//printf("%x|", val);
					tank->addData(val);
				}else if(c2=='n'){
					//10
					val=(int)'\n';
					//printf("%x|", val);
					tank->addData(val);
				}else if(c2=='r'){
					//13
					val=(int)'\r';
					//printf("%x|", val);
					tank->addData(val);
				}else if(c2=='t'){
					//9
					val=(int)'\t';
					//printf("%x|", val);
					tank->addData(val);
				}else if(c2=='\\'){
					val=(int)'\\';
					//printf("%x|", val);
					tank->addData(val);
				}else{
					val=(int)c;
					c=c2;
					//printf("%x|", val);
					tank->addData(val);
				}
			}else{
				val=(int)c;
				//printf("%x|", val);
				tank->addData(val);
			}
			fread(&c, sizeof(char), 1, cache);
		}
		tank->validate();

		gatherDatas(tank);

		fseek(cache, sizeof(char), SEEK_CUR);
		fread(&c, sizeof(char), 1, cache);
		fseek(cache, sizeof(char)*5, SEEK_CUR);
	}while(c!='}');

	fclose(cache);

	/*for(unsigned int i=0; i<tanks.size(); ++i){
		TankPlayed* t = tanks[i];

	}*/
}

void Player::gatherDatas(TankPlayed *tank){
	total+=tank->m_datas.randomData.battleCount;
	stats.wins+=tank->m_datas.randomData.wins;
	stats.losses+=tank->m_datas.randomData.losses;
	stats.survivedBattles+=tank->m_datas.randomData.survivedBattles;
}
