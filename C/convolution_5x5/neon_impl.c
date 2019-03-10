#include "neon_impl.h"

#include <arm_neon.h>
#include <stdio.h>

void applyFilterToImage_neon(int32_t *filter, int32_t *image, int32_t *output, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  int32_t *traveler = image;
  int32_t *output_trav = output;
  for(j=0; j<height-5; j++)
  {
    for(i=0; i<width-5; i+=4)
    {
      int32x4_t neon_filt0 = vdupq_n_s32(filter[0]);
      int32x4_t neon_filt1 = vdupq_n_s32(filter[1]);
      int32x4_t neon_filt2 = vdupq_n_s32(filter[2]);
      int32x4_t neon_filt3 = vdupq_n_s32(filter[3]);
      int32x4_t neon_filt4 = vdupq_n_s32(filter[4]);
      int32x4_t neon_data_batch0 = vld1q_s32(traveler);
      int32x4_t neon_data_batch1 = vld1q_s32(&traveler[1]);
      int32x4_t neon_data_batch2 = vld1q_s32(&traveler[2]);
      int32x4_t neon_data_batch3 = vld1q_s32(&traveler[3]);
      int32x4_t neon_data_batch4 = vld1q_s32(&traveler[4]);

      int32x4_t neon_batch0 = vmulq_s32(neon_filt0, neon_data_batch0);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt1, neon_data_batch1);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt2, neon_data_batch2);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt3, neon_data_batch3);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt4, neon_data_batch4);

      neon_filt0 = vdupq_n_s32(filter[5]);
      neon_filt1 = vdupq_n_s32(filter[6]);
      neon_filt2 = vdupq_n_s32(filter[7]);
      neon_filt3 = vdupq_n_s32(filter[8]);
      neon_filt4 = vdupq_n_s32(filter[9]);

      neon_data_batch0 = vld1q_s32(&traveler[width]);
      neon_data_batch1 = vld1q_s32(&traveler[width+1]);
      neon_data_batch2 = vld1q_s32(&traveler[width+2]);
      neon_data_batch3 = vld1q_s32(&traveler[width+3]);
      neon_data_batch4 = vld1q_s32(&traveler[width+4]);

      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt0, neon_data_batch0);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt1, neon_data_batch1);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt2, neon_data_batch2);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt3, neon_data_batch3);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt4, neon_data_batch4);

      neon_filt0 = vdupq_n_s32(filter[10]);
      neon_filt1 = vdupq_n_s32(filter[11]);
      neon_filt2 = vdupq_n_s32(filter[12]);
      neon_filt3 = vdupq_n_s32(filter[13]);
      neon_filt4 = vdupq_n_s32(filter[14]);

      int32x4_t neon_data_batch10 = {traveler[0+width*2], traveler[1+width*2], traveler[2+width*2], traveler[3+width*2]};
      int32x4_t neon_data_batch11 = {traveler[1+width*2], traveler[2+width*2], traveler[3+width*2], traveler[4+width*2]};
      int32x4_t neon_data_batch12 = {traveler[2+width*2], traveler[3+width*2], traveler[4+width*2], traveler[5+width*2]};
      int32x4_t neon_data_batch13 = {traveler[3+width*2], traveler[4+width*2], traveler[5+width*2], traveler[6+width*2]};
      int32x4_t neon_data_batch14 = {traveler[4+width*2], traveler[5+width*2], traveler[6+width*2], traveler[7+width*2]};

      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt0, neon_data_batch10);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt1, neon_data_batch11);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt2, neon_data_batch12);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt3, neon_data_batch13);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt4, neon_data_batch14);

      neon_filt0 = vdupq_n_s32(filter[15]);
      neon_filt1 = vdupq_n_s32(filter[16]);
      neon_filt2 = vdupq_n_s32(filter[17]);
      neon_filt3 = vdupq_n_s32(filter[18]);
      neon_filt4 = vdupq_n_s32(filter[19]);

      int32x4_t neon_data_batch15 = {traveler[0+width*3], traveler[1+width*3], traveler[2+width*3], traveler[3+width*3]};
      int32x4_t neon_data_batch16 = {traveler[1+width*3], traveler[2+width*3], traveler[3+width*3], traveler[4+width*3]};
      int32x4_t neon_data_batch17 = {traveler[2+width*3], traveler[3+width*3], traveler[4+width*3], traveler[5+width*3]};
      int32x4_t neon_data_batch18 = {traveler[3+width*3], traveler[4+width*3], traveler[5+width*3], traveler[6+width*3]};
      int32x4_t neon_data_batch19 = {traveler[4+width*3], traveler[5+width*3], traveler[6+width*3], traveler[7+width*3]};

      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt0, neon_data_batch15);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt1, neon_data_batch16);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt2, neon_data_batch17);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt3, neon_data_batch18);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt4, neon_data_batch19);

      neon_filt0 = vdupq_n_s32(filter[20]);
      neon_filt1 = vdupq_n_s32(filter[21]);
      neon_filt2 = vdupq_n_s32(filter[22]);
      neon_filt3 = vdupq_n_s32(filter[23]);
      neon_filt4 = vdupq_n_s32(filter[24]);

      int32x4_t neon_data_batch20 = {traveler[0+width*4], traveler[1+width*4], traveler[2+width*4], traveler[3+width*4]};
      int32x4_t neon_data_batch21 = {traveler[1+width*4], traveler[2+width*4], traveler[3+width*4], traveler[4+width*4]};
      int32x4_t neon_data_batch22 = {traveler[2+width*4], traveler[3+width*4], traveler[4+width*4], traveler[5+width*4]};
      int32x4_t neon_data_batch23 = {traveler[3+width*4], traveler[4+width*4], traveler[5+width*4], traveler[6+width*4]};
      int32x4_t neon_data_batch24 = {traveler[4+width*4], traveler[5+width*4], traveler[6+width*4], traveler[7+width*4]};

      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt0, neon_data_batch20);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt1, neon_data_batch21);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt2, neon_data_batch22);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt3, neon_data_batch23);
      neon_batch0 = vmlaq_s32(neon_batch0, neon_filt4, neon_data_batch24);

      int32_t* tmps = ((int32_t*)&neon_batch0);

      output_trav[0] = tmps[0];
      output_trav[1] = tmps[1];
      output_trav[2] = tmps[2];
      output_trav[3] = tmps[3];

      output_trav+=4;
      traveler+=4;
    }

    for(; i<width-5; i++)
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
    }

    output_trav += 4;
    traveler += 4;
  }
}
