#include "chromosome.h"

Chromosome::Chromosome(){
    genes=new Gene*[nbGene];
    for(int i=0; i<nbGene; ++i){genes[i]=new Gene();}
}

Chromosome::Chromosome(bool b){
    genes=new Gene*[nbGene];
    //*genes = (Gene*)malloc(sizeof(int)*nbGene);
    for(int i=0; i<nbGene; ++i){genes[i]=new Gene(b);}
}
Chromosome::~Chromosome(){for(int i=0; i<nbGene; ++i){delete genes[i];} delete[] genes;}

void Chromosome::randomize(){
    for(int i=0; i<nbGene; ++i){genes[i]->random();}
}

//distance
void Chromosome::fitting(){
//unsigned int Chromosome::fitting(){
    fittingValue=abs(number - getValue());
}

int Chromosome::getValue(){
    bool expecting=true; //true:number,false:operator
    int lastOperator=-1; //0:+, 1:-, 2:*, 3:/
    int res=0;

    for(int i=0; i<nbGene; ++i){
        Gene *g = genes[i];
        int val=g->getValue();
        if(g->isOperator() && expecting==false){
            switch(val){
                case 10:
                    lastOperator=0;
                    break;
                case 11:
                    lastOperator=1;
                    break;
                case 12:
                    lastOperator=2;
                    break;
                case 13:
                    lastOperator=3;
                    break;
            }
            expecting=!expecting;
        }else if(!g->isOperator() && expecting==true){
            switch(lastOperator){
                case 0:
                    res+=val;
                    break;
                case 1:
                    res-=val;
                    break;
                case 2:
                    res*=val;
                    break;
                case 3:
                    if(val != 0)
                        return -1;
                    break;
                case -1:
                    res=val;
                    break;
            }
            expecting=!expecting;
            lastOperator=-1;
        }
    }
    return res;
}

void Chromosome::crossingover(Chromosome *c2){
    // create source of randomness, and initialize it with non-deterministic seed
    std::mt19937 eng((std::random_device())());

    // a distribution that takes randomness and produces values in specified range
    std::uniform_int_distribution<> dist(0,geneSize*nbGene-1);

    int pivot = dist(eng);

    bool swp;
    for(int i=pivot; i<geneSize*nbGene; ++i){
        int gene = i/geneSize;
        int spot = i%geneSize;
        swp=c2->genes[gene]->values[spot];
        c2->genes[gene]->values[spot]=genes[gene]->values[spot];
        genes[gene]->values[spot]=swp;
    }
}

int Chromosome::getFittingValue(){
    return fittingValue;
}

ostream& operator<<(ostream &s,Chromosome &c){
    for(int i=0; i<nbGene; ++i){
        s<<*c.genes[i]<<" ";
    }
    s<<endl<<c.getValue();
    return s;
}
