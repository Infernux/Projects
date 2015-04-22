#ifndef __CHROMOSOME_H__
#define __CHROMOSOME_H__

#include <unistd.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <random>

#include "gene.h"
#include "constants.h"

class Chromosome
{
    public:
        Gene **genes;

        Chromosome();
        Chromosome(bool);
        ~Chromosome();
        //unsigned int fitting();

        void randomize();
        int getValue();
        void crossingover(Chromosome *c2);

        void fitting();
        int getFittingValue();

        friend ostream& operator<<(ostream &s,Chromosome &c);

    private:
        int fittingValue;

};

#endif
