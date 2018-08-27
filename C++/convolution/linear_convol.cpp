#include "linear_convol.h"

#include <string.h>

void LinearConvol::convol(double* out, double* img, Filter filter, int x, int y, int stride)
{
  double n[stride-2]; //2 == padding*2
  int padding = 1;
  int width = stride - 2*padding;

  memset(n, 0, (stride-2)*sizeof(double));

  for(int j=y-1; j<y+2; ++j)
  {
    double f0 = filter->matrix[(j-y+1)*filter->width];
    double f1 = filter->matrix[(j-y+1)*filter->width + 1];
    double f2 = filter->matrix[(j-y+1)*filter->width + 2];

    //n[0] += f0 * img[j*stride];
    n[0] += f1 * img[j*stride+1];
    n[1] += f0 * img[j*stride+1];

    int i;
    for(i=2; i<stride-2; ++i)
    {
      n[i]   += f0 * img[(j*stride)+i];
      n[i-1] += f1 * img[(j*stride)+i];
      n[i-2] += f2 * img[(j*stride)+i];
    }

    //n[stride-2]   += f1 * img[(j*stride)+(stride-1)];
    //n[stride-2]   += f2 * img[(j*stride)+(stride-2)];
    //n[stride-3]   += f2 * img[(j*stride)+(stride-1)];
  }

  for(int i=0; i<width; ++i)
  {
    out[(y-padding)*width+i] = CLIP(n[i]);
  }
}

void LinearConvol::apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding)
{
  for(int y=0 + padding; y<height + padding; ++y)
  {
      convol(out, padded_img, filter, 0, y, (width+padding*2));
  }
}

void LinearConvol::whatIsMyName()
{
  std::cout << "LinearConvol !" << std::endl;
}
