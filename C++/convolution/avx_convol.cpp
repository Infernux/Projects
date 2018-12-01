#include "avx_convol.h"

#include <immintrin.h>

#include <string.h>

void AVXConvol::convol(double* out, double* img, Filter filter, const unsigned int padded_width, const unsigned int padded_height, const unsigned padding)
{
  //non padded values
  unsigned H = padded_height - padding*2;
  unsigned W = padded_width  - padding*2;
  unsigned total_size = H * W;

  unsigned S = padded_width, P = padding;

  //output
  double *n   = new double[total_size];
  memset(n, 0, sizeof(double) * total_size);
  double f[9] = { filter->matrix[0], filter->matrix[1], filter->matrix[2], filter->matrix[3], filter->matrix[4], filter->matrix[5], filter->matrix[6], filter->matrix[7], filter->matrix[8] };

  __m256d f1 = _mm256_set_pd(f[0], f[2], f[1], f[0]);
  __m256d f2 = _mm256_set_pd(f[0], f[5], f[4], f[3]);
  __m256d f3 = _mm256_set_pd(f[0], f[8], f[7], f[6]);

  for(int j=padding + 1; j<padded_height-padding - 1; ++j)
  {
    unsigned int offset_y_orig = j * padded_width;
    unsigned int j_dest = j - padding;
    for(int i=padding + 1; i<padded_width-padding - 1; ++i)
    {
      unsigned int i_dest = i - padding;
      __m256d v    = _mm256_set_pd(img[offset_y_orig + i], img[offset_y_orig + i], img[offset_y_orig + i], img[offset_y_orig + i]);
      __m256d res  = _mm256_mul_pd(f3, v);

      n[(j_dest-1)*W + i_dest-1]  += res[2]; //左上
      n[(j_dest-1)*W + i_dest]    += res[1]; //上
      n[(j_dest-1)*W + i_dest+1]  += res[0]; //右上

      res  = _mm256_mul_pd(f2, v);

      n[(j_dest)*W + i_dest-1]  += res[2]; //左
      n[(j_dest)*W + i_dest]    += res[1]; //真ん中
      n[(j_dest)*W + i_dest+1]  += res[0]; //右

      res  = _mm256_mul_pd(f1, v);

      n[(j_dest+1)*W + i_dest-1]  += res[2]; //左
      n[(j_dest+1)*W + i_dest]    += res[1]; //真ん中
      n[(j_dest+1)*W + i_dest+1]  += res[0]; //右
    }
  }

  for(int i=0; i<total_size; ++i)
  {
    out[i] = CLIP(n[i]);
  }

  delete n;
}

void AVXConvol::apply_filter(double* out, double* padded_img, Filter filter, int width, int height, int padding)
{
  convol(out, padded_img, filter, (width+padding*2), (height+padding*2), padding);
}

void AVXConvol::whatIsMyName()
{
  std::cout << "AVXConvol !" << std::endl;
}
