#include "SmartIterator.h"

using namespace std;

SmartIterator::SmartIterator(char* name)
{
	index=0;
	fd = fopen(name, "rb");
}

SmartIterator::~SmartIterator(){
	if(fd!=NULL)
		fclose(fd);
}

Tank* SmartIterator::get(int idtank){
	if(idtank>index){
		index = idtank+1;
	}else{
		fseek(fd, 0, SEEK_SET);
		index = idtank+1;
	}

	unsigned char c;
	fread(&c, sizeof(char), 1, fd);
	while(idtank!=c && !feof(fd)){
		do{ //on rejoint la prochaine ligne
			fread(&c, sizeof(char), 1, fd);
		}while(c!='\n');
		fread(&c, sizeof(char), 1, fd);
	}

	if(feof(fd)){
		cout << idtank << endl;
		string* s = new string("zeufeuk !");
		Tank* tank = new Tank(s, idtank, 0, 0);
		return tank;
	}

	fseek(fd, sizeof(char), SEEK_CUR);

	string* s=new string();
	fread(&c, sizeof(char), 1, fd);
	do{
		*s+=c;
		fread(&c, sizeof(char), 1, fd);
	}while(c!='|' && !feof(fd));

	char type;
	
	fread(&type, sizeof(char), 1, fd);

	fseek(fd, sizeof(char), SEEK_CUR);

	string s2;
	fread(&c, sizeof(char), 1, fd);
	do{
		s2+=c;
		fread(&c, sizeof(char), 1, fd);
	}while(c!='\n' && !feof(fd));

	Tank* tank = new Tank(s, idtank, type-'0', atoi(s2.c_str()));

	return tank;
}
