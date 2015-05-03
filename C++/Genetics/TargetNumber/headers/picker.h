#ifndef __PICKER_H__
#define __PICKER_H__

#include <random>
#include "constants.h"
#include "chromosome.h"

typedef struct strCouple
{
    int id;
    int val;
}Couple;

class Picker
{
    public:
        Picker();

        void addContender(int id, int fitting);
        void reset();
        bool isConsanguin();
        Chromosome* pick(Chromosome **);
        long sum;

    private:
        Chromosome* findChrom(Chromosome *g[], int value, int pivot=generationSize/2, int lastInc=generationSize/2);

        Couple values[generationSize];
        int currentlyFilled;

        long prevSum;
};

#endif
