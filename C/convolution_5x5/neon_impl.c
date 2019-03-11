#include "neon_impl.h"

#ifdef __NEON__
#include <arm_neon.h>
#include <stdio.h>

void applyFilterToImage_neon(int32_t *filter, int32_t *image, int32_t *output, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  int32_t *traveler = image;
  int32_t *output_trav = output;

  for(j=0; j<height-5; j++)
  {
    for(i=0; i<width-5; i++)
    {
      int32x4_t neon_filt0 = vld1q_s32(&filter[0]);
      int32x4_t neon_filt1 = vld1q_s32(&filter[5]);
      int32x4_t neon_filt2 = vld1q_s32(&filter[10]);
      int32x4_t neon_filt3 = vld1q_s32(&filter[15]);
      int32x4_t neon_filt4 = vld1q_s32(&filter[20]);
      int32x4_t neon_data_batch0 = vld1q_s32(traveler);

      int32x4_t tmp1 = vmulq_s32(neon_filt0, neon_data_batch0);
      neon_data_batch0 = vld1q_s32(&traveler[width]);
      tmp1 = vmlaq_s32(tmp1, neon_filt1, neon_data_batch0);
      neon_data_batch0 = vld1q_s32(&traveler[width*2]);
      tmp1 = vmlaq_s32(tmp1, neon_filt2, neon_data_batch0);
      neon_data_batch0 = vld1q_s32(&traveler[width*3]);
      tmp1 = vmlaq_s32(tmp1, neon_filt3, neon_data_batch0);
      neon_data_batch0 = vld1q_s32(&traveler[width*4]);
      tmp1 = vmlaq_s32(tmp1, neon_filt4, neon_data_batch0);

      int32_t* tmps = ((int32_t*)&tmp1);
      output_trav[0] = tmps[0] + tmps[1] + tmps[2] + tmps[3] +
        traveler[4] * filter[4] +
        traveler[4+width] * filter[9] +
        traveler[4+width*2] * filter[14] +
        traveler[4+width*3] * filter[19] +
        traveler[4+width*4] * filter[24]
        ;

      output_trav+=1;
      traveler+=1;
    }

    /*for(; i<width-5; i++)
    {
      int32_t tmp;
      tmp  = traveler[0] * filter[0];
      tmp += traveler[1] * filter[1];
      tmp += traveler[2] * filter[2];
      tmp += traveler[3] * filter[3];
      tmp += traveler[4] * filter[4];
      tmp += traveler[0+width] * filter[5];
      tmp += traveler[1+width] * filter[6];
      tmp += traveler[2+width] * filter[7];
      tmp += traveler[3+width] * filter[8];
      tmp += traveler[4+width] * filter[9];
      tmp += traveler[0+width*2] * filter[10];
      tmp += traveler[1+width*2] * filter[11];
      tmp += traveler[2+width*2] * filter[12];
      tmp += traveler[3+width*2] * filter[13];
      tmp += traveler[4+width*2] * filter[14];
      tmp += traveler[0+width*3] * filter[15];
      tmp += traveler[1+width*3] * filter[16];
      tmp += traveler[2+width*3] * filter[17];
      tmp += traveler[3+width*3] * filter[18];
      tmp += traveler[4+width*3] * filter[19];
      tmp += traveler[0+width*4] * filter[20];
      tmp += traveler[1+width*4] * filter[21];
      tmp += traveler[2+width*4] * filter[22];
      tmp += traveler[3+width*4] * filter[23];
      tmp += traveler[4+width*4] * filter[24];

      output_trav[0] = tmp;

      output_trav++;
      traveler++;
    }*/

    output_trav = &output[width*(j+1)];
    traveler = &image[width*(j+1)];
  }
}
#endif /* __NEON__ */
