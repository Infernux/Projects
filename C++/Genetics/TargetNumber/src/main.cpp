#include <unistd.h>
#include <random>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "gene.h"
#include "chromosome.h"

using namespace std;

Chromosome* populateFirstGen(){
    Chromosome *generation = new Chromosome[generationSize];
    for(int i=0; i<generationSize; ++i){
        generation[i].randomize();
    }
    return generation;
}

Chromosome* findChrom(Chromosome generation[], int fitting[], int value, int pivot=generationSize/2, int lastInc=generationSize/2){
    if(lastInc==0 || lastInc==1)
        lastInc=2;

    if(value>fitting[pivot]){
        return findChrom(generation,fitting,value,pivot+lastInc/2,lastInc/2);
    }else if(pivot==0 || value>fitting[pivot-1]){
        return &generation[pivot];
    }else{
        return findChrom(generation,fitting,value,pivot-lastInc/2,lastInc/2);
    }
}

//trouver un autre moyen que la somme
Chromosome* selection(Chromosome* generation){
    Chromosome *newGeneration = (Chromosome*)malloc(sizeof(Chromosome)*generationSize);
    int fitting[generationSize];
    std::mt19937 eng((std::random_device())());
    std::uniform_int_distribution<> mutCrossProb(1,maxChance);

    int sum=0;
    //petit coup d'OMP
    for(int i=0; i<generationSize; ++i){
        generation[i].fitting();
        fitting[i]=generation[i].getFittingValue()+sum;
        cout << generation[i].getFittingValue() << ":";
        sum+=generation[i].getFittingValue();
    }
    cout << endl;

    cout << sum << endl;

    int alreadyPicked=0;
    std::uniform_int_distribution<> picker(0,sum);
    while(alreadyPicked<generationSize){
        int val1 = picker(eng);
        int val2 = picker(eng); //!= de pick1

        Chromosome *parent1 = findChrom(generation,fitting,val1);
        Chromosome *parent2 = findChrom(generation,fitting,val2);
        newGeneration[alreadyPicked]=parent1;
        alreadyPicked+=1;
        newGeneration[alreadyPicked]=parent2;
        alreadyPicked+=1;
        
    }

    delete[] generation;

    return newGeneration;
}

int main(){
    Chromosome* generation = populateFirstGen();
    generation = selection(generation);
    free(generation);
}
