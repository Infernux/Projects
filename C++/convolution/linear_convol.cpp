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

  int count = 0, A = 0, i;
  double* trav = img;
  for(int j=0; j<H; j++, A += S)
  {
    trav = &img[A+P];
    n[count]  = f[1] * trav[     0  ];
    n[count] += f[2] * trav[     1];
    n[count] += f[4] * trav[S      ];
    n[count] += f[5] * trav[S    +1];
    n[count] += f[7] * trav[S+S    ];
    n[count] += f[8] * trav[S+S  +1];
    ++count;

    for(int i=1; i<W-1; ++i, ++count)
    {
      n[count]  = f[0] * trav[     i-1];
      n[count] += f[1] * trav[     i  ];
      n[count] += f[2] * trav[     i+1];
      n[count] += f[3] * trav[S    +i-1];
      n[count] += f[4] * trav[S    +i  ];
      n[count] += f[5] * trav[S    +i+1];
      n[count] += f[6] * trav[S+S  +i-1];
      n[count] += f[7] * trav[S+S  +i  ];
      n[count] += f[8] * trav[S+S  +i+1];
    }

    n[count]  = f[0] * trav[     W-1-1];
    n[count] += f[1] * trav[     W-1  ];
    n[count] += f[3] * trav[S    +W-1-1];
    n[count] += f[4] * trav[S    +W-1  ];
    n[count] += f[6] * trav[S+S  +W-1-1];
    n[count] += f[7] * trav[S+S  +W-1  ];
    ++count;
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
