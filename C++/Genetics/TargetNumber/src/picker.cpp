#include "picker.h"

Picker::Picker()
{
    sum=0;
    currentlyFilled=0;
}

void Picker::addContender(int id, int fitting)
{
    values[currentlyFilled].id=id;
    sum+=fitting;
    values[currentlyFilled].val=sum;
    currentlyFilled++;
}

void Picker::reset()
{
    prevSum=sum;
    sum=0;
    currentlyFilled=0;
}

Chromosome* Picker::pick(Chromosome **generation){
    std::mt19937 eng((std::random_device())());
    std::uniform_int_distribution<> picking(0,sum);

    int rdmValue = picking(eng);
    return findChrom(generation,rdmValue);
}

bool Picker::isConsanguin(){
    return sum==prevSum;
}

//~~~~~~~~~~~~~~~~~~~~ Private ~~~~~~~~~~~~~~~~~~~~~~~~~

Chromosome* Picker::findChrom(Chromosome *generation[], int value, int pivot, int lastInc){
    if(lastInc==0 || lastInc==1)
        lastInc=2;

    if(value>values[pivot].val){
        return findChrom(generation,value,pivot+lastInc/2,lastInc/2);
    }else if(pivot==0 || value>values[pivot-1].val){
        return generation[pivot];
    }else{
        return findChrom(generation,value,pivot-lastInc/2,lastInc/2);
    }
}
