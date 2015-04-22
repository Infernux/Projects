#ifndef __GENE_H__
#define __GENE_H__

#include <unistd.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <random>
#include "constants.h"

using namespace std;

class Gene
{
    public:
        bool *values;
        //int geneSize = 5;

        Gene();
        Gene(bool);
        ~Gene();

        void random();
        friend ostream& operator<<(ostream &s, Gene &g);
        int getValue();
        bool isOperator();

    private:
        bool isValid();
};

#endif
