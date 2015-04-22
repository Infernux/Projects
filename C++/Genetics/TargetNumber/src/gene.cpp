#include "gene.h"

Gene::Gene()
{
    values=new bool[geneSize];
}

Gene::Gene(bool v)
{
    values=new bool[geneSize];
    for(int i=0;i<geneSize;++i)
        values[i]=v;
}

Gene::~Gene()
{
    delete[] values;
}

void Gene::random(){
    std::mt19937 eng((std::random_device())());
    std::uniform_int_distribution<> boolPicker(0,1);
    do{
        for(int i=0; i<geneSize; ++i)
            values[i]=boolPicker(eng);
    }while(!isValid());
}

int Gene::getValue(){
    int value = 0;
    for(int i=0; i<geneSize; i++){
        value=value<<1;
        value|=values[i]?1:0;
    }
    return value; 
}

bool Gene::isOperator(){
    if(getValue()>9)
        return true;
    else
        return false;
}

bool Gene::isValid(){
    if(getValue()>13)
        return false;
    return true;
}

//-------------------------- OPERATOR -----------------------

ostream& operator<<(ostream &s, Gene &g){
    for(int i=0; i<geneSize; i++){
        s<<g.values[i]?"1":"0";
    }
    return s;
}
