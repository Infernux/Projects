#include <unistd.h>
#include <random>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "gene.h"
#include "chromosome.h"
#include "picker.h"

using namespace std;

typedef struct strGenerations
{
    Chromosome *curGen[generationSize];
    Chromosome *newGen[generationSize];
}Generations;

void freeGeneration(Chromosome **g){
    for(int i=0; i<generationSize; ++i){
        delete g[i];
    }
    delete[] g;
}

Chromosome** populateFirstGen(){
    Chromosome **generation = new Chromosome*[generationSize];
    for(int i=0; i<generationSize; ++i){
        generation[i] = new Chromosome();
        generation[i]->randomize();
    }
    return generation;
}

//trouver un autre moyen que la somme
Chromosome** selection(Chromosome** generation, Picker *picker){
    if(generation==NULL)
        return NULL;

    picker->reset();
    //print G1 puis g2
    for(int i=0; i<generationSize; ++i){
        generation[i]->fitting();
        //cout << "(" << i << ":" << generation[i]->getFittingValue() << "):";
        int a = generation[i]->getFittingValue();
        a=(a==-1?0:a);
        picker->addContender(i,a);
        if(a==number){
            cout << endl << *generation[i] << "-> " << a << endl;
            freeGeneration(generation);

            return NULL;
        }
    }
    /*cout << endl << "Tab:";
    for(int i=0; i<generationSize; ++i){
        cout << fitting[i] << ",";
    }*/
    if(picker->isConsanguin()){
        cout << "Consanguins !" << endl;
        for(int i=1; i<generationSize-1; ++i){
            generation[0]->mutate();
            generation[i]->crossingover(generation[0]);
        }
        return generation;
    }else{
        cout << "sum:" << number*generationSize-picker->sum << endl;
    }

    Chromosome **newGeneration = new Chromosome*[generationSize];

    int alreadyPicked=0;

    std::mt19937 eng((std::random_device())());
    std::uniform_int_distribution<> mutCrossProb(1,maxChance);
    while(alreadyPicked<generationSize){
        Chromosome *parent1 = picker->pick(generation);
        Chromosome *parent2 = NULL;

        int tries=0;
        do{
            parent2 = picker->pick(generation);
            ++tries;
        }while(parent1==parent2 && tries<=100);

        int crossingOverPick = mutCrossProb(eng);
        int mutationPick1 = mutCrossProb(eng);
        int mutationPick2 = mutCrossProb(eng);

        //cout << "v1:" << val1 << ",v2:" << val2 << ",mut:" << crossingOverPick << endl;
        if(crossingOverPick<=crossingoverChance){
            parent1->crossingover(parent2);
        }

        if(mutationPick1 <= mutationChance)
            parent1->mutate();
        if(mutationPick2 <= mutationChance)
            parent2->mutate();

        newGeneration[alreadyPicked] = new Chromosome(parent1);
        alreadyPicked+=1;
        newGeneration[alreadyPicked] = new Chromosome(parent2);
        alreadyPicked+=1;
    }

    freeGeneration(generation);

    return newGeneration;
}

int main(){
    Picker *picker = new Picker();
    Chromosome** generation = populateFirstGen();
    for(int i=0; i<generations; ++i){
        //cout << "Generation : " << i << endl;
        generation = selection(generation,picker);
        if(generation==NULL)
            break;
    }
    if(generation!=NULL)
        freeGeneration(generation);

    delete picker;
}
