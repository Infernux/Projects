#include "dual_convol.h"

void DualConvol::convol(double* out, double* img, Filter filter, int x, int y, int stride)
{
  int n = 0.f, n2 = 0.f;
  n += img[x-1 + (y-1)*stride] * filter->matrix[0];
  n2+= img[x   + (y-1)*stride] * filter->matrix[0];
  n += img[x   + (y-1)*stride] * filter->matrix[1];
  n2+= img[x+1 + (y-1)*stride] * filter->matrix[1];
  n += img[x+1 + (y-1)*stride] * filter->matrix[2];
  n2+= img[x+2 + (y-1)*stride] * filter->matrix[2];
  n += img[x-1 + y*stride] * filter->matrix[3];
  n2+= img[x   + y*stride] * filter->matrix[3];
  n += img[x   + y*stride] * filter->matrix[4];
  n2+= img[x+1 + y*stride] * filter->matrix[4];
  n += img[x+1 + y*stride] * filter->matrix[5];
  n2+= img[x+2 + y*stride] * filter->matrix[5];
  n += img[x-1 + (y+1)*stride] * filter->matrix[6];
  n2+= img[x   + (y+1)*stride] * filter->matrix[6];
  n += img[x   + (y+1)*stride] * filter->matrix[7];
  n2+= img[x+1 + (y+1)*stride] * filter->matrix[7];
  n += img[x+1 + (y+1)*stride] * filter->matrix[8];
  n2+= img[x+2 + (y+1)*stride] * filter->matrix[8];

  n   = CLIP(n);
  n2  = CLIP(n2);

  int padding = 1;
  int width = stride - 2*padding;

  out[(x-padding) + (y-padding) * width] = n;
  out[(x+1-padding) + (y-padding) * width] = n2;
}

void DualConvol::apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding)
{
  for(int y=0 + padding; y<height + padding; ++y)
  {
    for(int x=0 + padding; x<width + padding; x+=2)
    {
      convol(out, padded_img, filter, x, y, (width+padding*2));
    }
  }
}

void DualConvol::whatIsMyName()
{
  std::cout << "DualConvol !" << std::endl;
}
