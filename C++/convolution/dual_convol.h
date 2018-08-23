#ifndef DUAL_CONVOL__H_
#define DUAL_CONVOL__H_

#include "common.h"

void apply_filter_dual(double* out, double* padded_img, Filter filter, int width, int height, int padding);

#endif
