#ifndef LINEAR_CONVOL__H_
#define LINEAR_CONVOL__H_

#include <iostream>
#include "common.h"
#include "convol.h"

class LinearConvol : public Convol
{
  public:
    void apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding);
    void whatIsMyName();

  private:
    void convol(double* out, double* img, Filter filter, const unsigned int padded_width, const unsigned int padded_height, const unsigned padding);
};

#endif //LINEAR_CONVOL__H_
