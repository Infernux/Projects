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
        Gene(Gene*);
        Gene(bool);
        ~Gene();

        void random();
        int getValue();
        bool isOperator();

        friend ostream& operator<<(ostream &s, Gene &g);
        friend bool operator==(Gene &l, Gene &r);

    private:
        bool isValid();
};

#endif
