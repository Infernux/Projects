#include "triple_convol.h"

void TripleConvol::convol(double* out, double* img, Filter filter, int x, int y, int stride)
{
  double n = 0.f, n2 = 0.f, n3 = 0.f;

  n += img[x-2  + (y-1)*stride] * filter->matrix[0];
  n2+= img[x-1  + (y-1)*stride] * filter->matrix[0];
  n3+= img[x    + (y-1)*stride] * filter->matrix[0];
  n += img[x-1  + (y-1)*stride] * filter->matrix[1];
  n2+= img[x    + (y-1)*stride] * filter->matrix[1];
  n3+= img[x+1  + (y-1)*stride] * filter->matrix[1];
  n += img[x    + (y-1)*stride] * filter->matrix[2];
  n2+= img[x+1  + (y-1)*stride] * filter->matrix[2];
  n3+= img[x+2  + (y-1)*stride] * filter->matrix[2];

  n += img[x-2 + (y)*stride] * filter->matrix[3];
  n2+= img[x-1 + (y)*stride] * filter->matrix[3];
  n3+= img[x   + (y)*stride] * filter->matrix[3];
  n += img[x-1  + (y)*stride] * filter->matrix[4];
  n2+= img[x    + (y)*stride] * filter->matrix[4];
  n3+= img[x+1  + (y)*stride] * filter->matrix[4];
  n += img[x    + (y)*stride] * filter->matrix[5];
  n2+= img[x+1  + (y)*stride] * filter->matrix[5];
  n3+= img[x+2  + (y)*stride] * filter->matrix[5];

  n += img[x-2 + (y+1)*stride] * filter->matrix[6];
  n2+= img[x-1 + (y+1)*stride] * filter->matrix[6];
  n3+= img[x   + (y+1)*stride] * filter->matrix[6];
  n += img[x-1  + (y+1)*stride] * filter->matrix[7];
  n2+= img[x    + (y+1)*stride] * filter->matrix[7];
  n3+= img[x+1  + (y+1)*stride] * filter->matrix[7];
  n += img[x    + (y+1)*stride] * filter->matrix[8];
  n2+= img[x+1  + (y+1)*stride] * filter->matrix[8];
  n3+= img[x+2  + (y+1)*stride] * filter->matrix[8];

  n = CLIP(n);
  n2 = CLIP(n2);
  n3 = CLIP(n3);

  int padding = 1;
  int width = stride - 2*padding;

  out[(x-1-padding) + (y-padding) * width] = n;
  out[(x-padding) + (y-padding) * width] = n2;
  out[(x+1-padding) + (y-padding) * width] = n3;
}

void TripleConvol::apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding)
{
  for(int y=0 + padding; y<height + padding; ++y)
  {
    for(int x=1 + padding; x<width + padding; x+=3)
    {
      convol(out, padded_img, filter, x, y, (width+padding*2));
    }
  }
}

void TripleConvol::whatIsMyName()
{
  std::cout << "TripleConvol !" << std::endl;
}
