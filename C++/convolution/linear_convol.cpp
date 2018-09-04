#include "linear_convol.h"

#include <string.h>

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

  int count = 0, A = 0, i;
  img   = &img[P];
  double *img2  = &img[S];
  double *img3  = &img[2*S];
  for(int j=0; j<H; j++, A += S)
  {
    n[count]  = f[1] * img  [0];
    n[count] += f[2] * img  [1];
    n[count] += f[4] * img2 [0];
    n[count] += f[5] * img2 [1];
    n[count] += f[7] * img3 [0];
    n[count] += f[8] * img3 [1];
    ++count;

    for(int i=1; i<W-1; ++i, ++count)
    {
      n[count]  = f[0] * img[i-1];
      n[count] += f[1] * img[i  ];
      n[count] += f[2] * img[i+1];
      n[count] += f[3] * img2[i-1];
      n[count] += f[4] * img2[i  ];
      n[count] += f[5] * img2[i+1];
      n[count] += f[6] * img3[i-1];
      n[count] += f[7] * img3[i  ];
      n[count] += f[8] * img3[i+1];
    }

    n[count]  = f[0] * img  [W-1-1];
    n[count] += f[1] * img  [W-1  ];
    n[count] += f[3] * img2 [W-1-1];
    n[count] += f[4] * img2 [W-1  ];
    n[count] += f[6] * img3 [W-1-1];
    n[count] += f[7] * img3 [W-1  ];
    ++count;
    img = img2;
    img2 = img3;
    img3 = &img3[S];
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
