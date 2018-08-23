#ifndef __NAIVE_CONVOL_H
#define __NAIVE_CONVOL_H

#include "common.h"

void apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding);

#endif
