#include "naive_convol.h"

double NaiveConvol::convol(double* img, Filter filter, int x, int y, int stride)
{
  //flip kernel
  int n = 0.f;
  for(int j=-1; j<2; ++j)
  {
    for(int i=-1; i<2; ++i)
    {
      n += img[x+i + (y+j)*stride] * filter->matrix[i+1 + (j+1)*filter->width];
    }
  }
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

void NaiveConvol::apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding)
{
  for(int y=0 + padding; y<height + padding; ++y)
  {
    for(int x=0 + padding; x<width + padding; ++x)
    {
      out[(x-padding) + (y-padding) * width] = convol(padded_img, filter, x, y, (width+padding*2));
    }
  }
}

void NaiveConvol::whatIsMyName()
{
  std::cout << "NaiveConvol !" << std::endl;
}
