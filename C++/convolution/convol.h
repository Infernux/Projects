#ifndef __CONVOL_H__
#define __CONVOL_H__

#include "common.h"

class Convol
{
  public:
    virtual void apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding) = 0;
    virtual void whatIsMyName() = 0;
};

#endif //__CONVOL_H__
