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

  /* compute top line */
  double el = img[padding + padded_width];
  n[0]      += el * f[4];
  n[1]      += el * f[3];
  n[W]      += el * f[1];
  n[W + 1]  += el * f[0];

  for(int i=padding + 1; i < padded_width - padding - 1; ++i)
  {
    unsigned int i_dest = i - padding;
    double el = img[padded_width + i];

    n[i_dest - 1]        += el * f[5];
    n[i_dest]            += el * f[4];
    n[i_dest + 1]          += el * f[3];
    n[(1) * W + i_dest - 1]  += el * f[2];
    n[(1) * W + i_dest]      += el * f[1];
    n[(1) * W + i_dest + 1]  += el * f[0];
  }

  el = img[padded_width + padded_width - padding - 1];
  n[W-2]       += el * f[5];
  n[W-1]       += el * f[4];
  n[W + W - 2] += el * f[2];
  n[W + W - 1] += el * f[1];

  for(int j=padding + 1; j<padded_height-padding - 1; ++j)
  {
    unsigned int offset_y_orig = j * padded_width;
    unsigned int j_dest = j - padding;
    /*
     */
    double el = img[offset_y_orig + padding];
    /*
     * broadcast to the 6 adjacent elements
     */
    n[(j_dest-1) * W]     += el * f[7];
    n[(j_dest-1) * W + 1] += el * f[6];
    n[(j_dest) * W]       += el * f[4];
    n[(j_dest) * W + 1]   += el * f[3];
    n[(j_dest+1) * W]     += el * f[1];
    n[(j_dest+1) * W + 1] += el * f[0];

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

    el = img[offset_y_orig + padded_width - 2];
    /*
     * broadcast to the 6 adjacent elements
     */
    n[(j_dest-1) * W + (W - 1) - 1] += el * f[8];
    n[(j_dest-1) * W + (W - 1)]     += el * f[7];
    n[(j_dest) * W + (W - 1) - 1]   += el * f[5];
    n[(j_dest) * W + (W - 1)]       += el * f[4];
    n[(j_dest+1) * W + (W - 1) - 1] += el * f[2];
    n[(j_dest+1) * W + (W - 1)]     += el * f[1];
  }

  /* compute bottom line */
  el = img[(padded_width * (padded_height - 1 - padding)) + padding];
  n[(H-2)*W]      += el * f[7];
  n[(H-2)*W+1]    += el * f[6];
  n[(H-1)*W]      += el * f[4];
  n[(H-1)*W+1]    += el * f[3];

  unsigned int offset_y_orig = (padded_height - 1 - padding) * padded_width;
  for(int i=padding + 1; i < padded_width - padding - 1; ++i)
  {
    unsigned int i_dest = i - padding;
    double el = img[offset_y_orig + i];

    n[(H-1 - 1)*W + i_dest -1] += el * f[8];
    n[(H-1 - 1)*W + i_dest]    += el * f[7];
    n[(H-1 - 1)*W + i_dest+1]  += el * f[6];
    n[(H-1)*W + i_dest -1]     += el * f[5];
    n[(H-1)*W + i_dest]        += el * f[4];
    n[(H-1)*W + i_dest+1]      += el * f[3];
  }

  el = img[(padded_width * (padded_height - 1 - padding)) + padded_width - padding - 1];
  n[(H-2)*W + W - 2]       += el * f[8];
  n[(H-2)*W + W - 1]       += el * f[7];
  n[(H-1)*W + W - 2] += el * f[5];
  n[(H-1)*W + W - 1] += el * f[4];

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
