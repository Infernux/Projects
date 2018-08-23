#ifndef UNRAVEL__H_
#define UNRAVEL__H_

#include <iostream>
#include "common.h"
#include "convol.h"

class UnravelConvol : public Convol
{
  public:
    void apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding);
    void whatIsMyName();

  private:
    double convol(double* img, Filter filter, int x, int y, int stride);
};

#endif
