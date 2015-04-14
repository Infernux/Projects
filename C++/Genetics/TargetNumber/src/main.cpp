#include <unistd.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define geneSize 10
#define nbChrom 5

using namespace std;

class Gene
{
    public:
        Gene(){values=new bool[geneSize];}
        ~Gene(){delete[] values;}
        //int geneSize = 5;
        bool *values;
        void random(){
            for(int i=0; i<geneSize; ++i)
                values[i]=rand()%2;
        }
        friend ostream& operator<<(ostream &s, Gene &g){
            for(int i=0; i<geneSize; i++){
                s<<g.values[i]?"1":"0";
            }
            return s;
        }
};

class Chromosome
{
    public:
        Chromosome(){
            genes=new Gene*[nbChrom];
            //*genes = (Gene*)malloc(sizeof(int)*nbChrom);
            for(int i=0; i<nbChrom; ++i){genes[i]=new Gene(); genes[i]->random();}
        }
        ~Chromosome(){for(int i=0; i<nbChrom; ++i){delete genes[i];} delete[] genes;}
        Gene **genes;
        friend ostream& operator<<(ostream &s,Chromosome &c){
            for(int i=0; i<nbChrom; ++i){
                s<<*c.genes[i]<<" ";
            }
            return s;
        }
};

int main(){
    srand (time(NULL));

    Chromosome *c = new Chromosome();
    cout << *c << endl;
    delete c;
}
