#ifndef __NAIVE_CONVOL_H
#define __NAIVE_CONVOL_H

#include <iostream>
#include "common.h"
#include "convol.h"

class NaiveConvol : public Convol
{
  public:
    void apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding);
    void whatIsMyName();

  private:
    double convol(double* img, Filter filter, int x, int y, int stride);
};

#endif
