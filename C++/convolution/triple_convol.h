#ifndef TRIPLE_CONVOL__H_
#define TRIPLE_CONVOL__H_

#include <iostream>
#include "common.h"
#include "convol.h"

class TripleConvol : public Convol
{
  public:
    void apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding);
    void whatIsMyName();

  private:
    void convol(double* out, double* img, Filter filter, int x, int y, int stride);
};

#endif
