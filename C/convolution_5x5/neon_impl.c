#include "neon_impl.h"

#ifdef __ARM_NEON
#include <arm_neon.h>
#include <stdio.h>

void applyFilterToImage_neon(int32_t *filter, int32_t *image, int32_t *output, uint32_t width, uint32_t height)
{
  uint32_t j;
  int32_t *traveler = image;
  int32_t *end;
  int32_t *output_trav = output;

  unsigned int BLOCK_SIZE = 2;

  int32x4_t neon_filt0 = vld1q_s32(&filter[0]);
  int32x4_t neon_filt1 = vld1q_s32(&filter[5]);
  int32x4_t neon_filt2 = vld1q_s32(&filter[10]);
  int32x4_t neon_filt3 = vld1q_s32(&filter[15]);
  int32x4_t neon_filt4 = vld1q_s32(&filter[20]);

  for(j=0; j<height-5; j++)
  {
    for(end = &traveler[width-5-BLOCK_SIZE]; traveler < end; traveler += BLOCK_SIZE, output_trav+=BLOCK_SIZE)
    {
      int32x4_t neon_data_batch0 = vld1q_s32(traveler);
      int32x4_t neon_data_batch1 = vld1q_s32(&traveler[1]);
      int32x4_t tmp1 = vmulq_s32(neon_filt0, neon_data_batch0);
      int32x4_t tmp2 = vmulq_s32(neon_filt0, neon_data_batch1);
      neon_data_batch0 = vld1q_s32(&traveler[width]);
      neon_data_batch1 = vld1q_s32(&traveler[width+1]);
      tmp1 = vmlaq_s32(tmp1, neon_filt1, neon_data_batch0);
      tmp2 = vmlaq_s32(tmp2, neon_filt1, neon_data_batch1);
      neon_data_batch0 = vld1q_s32(&traveler[width*2]);
      neon_data_batch1 = vld1q_s32(&traveler[width*2+1]);
      tmp1 = vmlaq_s32(tmp1, neon_filt2, neon_data_batch0);
      tmp2 = vmlaq_s32(tmp2, neon_filt2, neon_data_batch1);
      neon_data_batch0 = vld1q_s32(&traveler[width*3]);
      neon_data_batch1 = vld1q_s32(&traveler[width*3+1]);
      tmp1 = vmlaq_s32(tmp1, neon_filt3, neon_data_batch0);
      tmp2 = vmlaq_s32(tmp2, neon_filt3, neon_data_batch1);
      neon_data_batch0 = vld1q_s32(&traveler[width*4]);
      neon_data_batch1 = vld1q_s32(&traveler[width*4+1]);
      tmp1 = vmlaq_s32(tmp1, neon_filt4, neon_data_batch0);
      tmp2 = vmlaq_s32(tmp2, neon_filt4, neon_data_batch1);

      int32_t* tmps = ((int32_t*)&tmp1);
      output_trav[0] = tmps[0] + tmps[1] + tmps[2] + tmps[3] +
        traveler[4] * filter[4] +
        traveler[4+width] * filter[9] +
        traveler[4+width*2] * filter[14] +
        traveler[4+width*3] * filter[19] +
        traveler[4+width*4] * filter[24]
        ;

      tmps = ((int32_t*)&tmp2);
      output_trav[1] = tmps[0] + tmps[1] + tmps[2] + tmps[3] +
        traveler[5] * filter[4] +
        traveler[5+width] * filter[9] +
        traveler[5+width*2] * filter[14] +
        traveler[5+width*3] * filter[19] +
        traveler[5+width*4] * filter[24]
        ;


    }

    end += BLOCK_SIZE;

    for(; traveler<end; traveler++, output_trav++)
    {
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
    }

    output_trav += 5;
    traveler += 5;
  }
}
#endif /* __ARM_NEON */
