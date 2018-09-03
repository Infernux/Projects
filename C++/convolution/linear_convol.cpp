#include "linear_convol.h"

#include <string.h>

void line(double* n, double* f, double* img, const unsigned y, const unsigned int padded_width, const unsigned width)
{
  int yy = y;
    n[(yy-1)*width + 1]  += img[padded_width*y + 1] * f[6];
    n[(yy-1)*width + 0]  += img[padded_width*y + 1] * f[7];
    n[yy*width + 1]      += img[padded_width*y + 1] * f[3];
    n[yy*width + 0]      += img[padded_width*y + 1] * f[4];
    n[(yy*width+1)+1]    += img[padded_width*y + 1] * f[0];
    n[(yy*width+1)+0]    += img[padded_width*y + 1] * f[1];

    for(int i=2; i<padded_width-1; ++i)
    {
      n[(yy-1)*width + i]    += img[padded_width*y + i] * f[6];
      n[(yy-1)*width + i-1]  += img[padded_width*y + i] * f[7];
      n[(yy-1)*width + i-2]  += img[padded_width*y + i] * f[8];

      n[yy*width + i]    += img[padded_width*y + i] * f[3];
      n[yy*width + i-1]  += img[padded_width*y + i] * f[4];
      n[yy*width + i-2]  += img[padded_width*y + i] * f[5];

      n[(yy*width+1)+i]    += img[padded_width*y + i] * f[0];
      n[(yy*width+1)+i-1]  += img[padded_width*y + i] * f[1];
      n[(yy*width+1)+i-2]  += img[padded_width*y + i] * f[2];
    }

}

void LinearConvol::convol(double* out, double* img, Filter filter, const unsigned int padded_width, const unsigned int padded_height, const unsigned padding)
{
  //non padded values
  unsigned H = padded_height - padding*2;
  unsigned W = padded_width  - padding*2;
  unsigned total_size = H * W;

  unsigned S = padded_width, P = padding;

  //output
  double *n   = new double[total_size];
  double f[9] = { filter->matrix[0], filter->matrix[1], filter->matrix[2], filter->matrix[3], filter->matrix[4], filter->matrix[5], filter->matrix[6], filter->matrix[7], filter->matrix[8] };

  for(int j=0; j<H; j++)
  {
    for(int i=0; i<W; ++i)
    {
      n[(j*W)+i]  = f[0] * img[S*j      +P+i-1];
      n[(j*W)+i] += f[1] * img[S*j      +P+i];
      n[(j*W)+i] += f[2] * img[S*j      +P+i+1];
      n[(j*W)+i] += f[3] * img[S*(j+1)  +P+i-1];
      n[(j*W)+i] += f[4] * img[S*(j+1)  +P+i];
      n[(j*W)+i] += f[5] * img[S*(j+1)  +P+i+1];
      n[(j*W)+i] += f[6] * img[S*(j+2)  +P+i-1];
      n[(j*W)+i] += f[7] * img[S*(j+2)  +P+i];
      n[(j*W)+i] += f[8] * img[S*(j+2)  +P+i+1];
    }
  }

  for(int i=0; i<total_size; ++i)
  {
    out[i] = CLIP(n[i]);
  }

  free(n);
}

void LinearConvol::apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding)
{
  convol(out, padded_img, filter, (width+padding*2), (height+padding*2), padding);
}

void LinearConvol::whatIsMyName()
{
  std::cout << "LinearConvol !" << std::endl;
}
