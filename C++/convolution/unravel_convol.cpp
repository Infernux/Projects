#include "unravel_convol.h"

double unravel_convol(double* img, Filter filter, int x, int y, int stride)
{
  int n = 0.f;
  n += img[x-1 + (y-1)*stride] * filter->matrix[0];
  n += img[x   + (y-1)*stride] * filter->matrix[1];
  n += img[x+1 + (y-1)*stride] * filter->matrix[2];
  n += img[x-1 + y*stride] * filter->matrix[3];
  n += img[x   + y*stride] * filter->matrix[4];
  n += img[x+1 + y*stride] * filter->matrix[5];
  n += img[x-1 + (y+1)*stride] * filter->matrix[6];
  n += img[x   + (y+1)*stride] * filter->matrix[7];
  n += img[x+1 + (y+1)*stride] * filter->matrix[8];
  if(n < 0.)
  {
    return 0.;
  }
  else if(n > 255.)
  {
    return 255.;
  }
  return n;

}

void apply_filter_unravel(double* out, double* padded_img, Filter filter, int width, int height, int padding)
{
  for(int y=0 + padding; y<height + padding; ++y)
  {
    for(int x=0 + padding; x<width + padding; ++x)
    {
      out[(x-padding) + (y-padding) * width] = unravel_convol(padded_img, filter, x, y, (width+padding*2));
    }
  }
}
