#ifndef DUAL_CONVOL__H_
#define DUAL_CONVOL__H_

#include <iostream>
#include "common.h"
#include "convol.h"

class DualConvol : public Convol
{
  public:
    void apply_filter(uint8_t* out, uint8_t* padded_img, Filter filter, int width, int height, int padding);
    void whatIsMyName();

  private:
    void convol(uint8_t* out, uint8_t* img, Filter filter, int x, int y, int stride);
};

#endif
