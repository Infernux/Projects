#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "neon_impl.h"
#include "utils.h"

#define IMG_HEIGHT  1000
#define IMG_WIDTH   1000

static void applyFilterToImage_ref(int32_t *filter, int32_t *image, int32_t *output, uint32_t width, uint32_t height)
{
  uint32_t i,j,k,l;
  for(j=0; j<height-5; ++j)
  {
    for(i=0; i<width-5; ++i)
    {
      int32_t tmp = 0;
      for(k=0; k<5; k++)
      {
        for(l=0; l<5; l++)
        {
          tmp += image[(j+k)*width+i+l] * filter[k*5+l];
        }
      }
      output[j*width + i] = tmp;
    }
  }
}

static void applyFilterToImage_opt(int32_t *filter, int32_t *image, int32_t *output, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  int32_t *traveler = image;
  int32_t *output_trav = output;
  for(j=0; j<height-5; j++)
  {
    for(i=0; i<width-5; i+=4)
    {
      int32_t tmp, tmp2, tmp3, tmp4;
      tmp   = traveler[0] * filter[0];
      tmp  += traveler[1] * filter[1];
      tmp2  = traveler[1] * filter[0];
      tmp  += traveler[2] * filter[2];
      tmp2 += traveler[2] * filter[1];
      tmp3  = traveler[2] * filter[0];
      tmp  += traveler[3] * filter[3];
      tmp2 += traveler[3] * filter[2];
      tmp3 += traveler[3] * filter[1];
      tmp4  = traveler[3] * filter[0];
      tmp  += traveler[4] * filter[4];
      tmp2 += traveler[4] * filter[3];
      tmp3 += traveler[4] * filter[2];
      tmp4 += traveler[4] * filter[1];
      tmp2 += traveler[5] * filter[4];
      tmp3 += traveler[5] * filter[3];
      tmp4 += traveler[5] * filter[2];
      tmp3 += traveler[6] * filter[4];
      tmp4 += traveler[6] * filter[3];
      tmp4 += traveler[7] * filter[4];
      tmp  += traveler[0+width] * filter[5];
      tmp  += traveler[1+width] * filter[6];
      tmp2 += traveler[1+width] * filter[5];
      tmp  += traveler[2+width] * filter[7];
      tmp2 += traveler[2+width] * filter[6];
      tmp3 += traveler[2+width] * filter[5];
      tmp  += traveler[3+width] * filter[8];
      tmp2 += traveler[3+width] * filter[7];
      tmp3 += traveler[3+width] * filter[6];
      tmp4 += traveler[3+width] * filter[5];
      tmp  += traveler[4+width] * filter[9];
      tmp2 += traveler[4+width] * filter[8];
      tmp3 += traveler[4+width] * filter[7];
      tmp4 += traveler[4+width] * filter[6];
      tmp2 += traveler[5+width] * filter[9];
      tmp3 += traveler[5+width] * filter[8];
      tmp4 += traveler[5+width] * filter[7];
      tmp3 += traveler[6+width] * filter[9];
      tmp4 += traveler[6+width] * filter[8];
      tmp4 += traveler[7+width] * filter[9];
      tmp  += traveler[0+width*2] * filter[10];
      tmp  += traveler[1+width*2] * filter[11];
      tmp2 += traveler[1+width*2] * filter[10];
      tmp  += traveler[2+width*2] * filter[12];
      tmp2 += traveler[2+width*2] * filter[11];
      tmp3 += traveler[2+width*2] * filter[10];
      tmp  += traveler[3+width*2] * filter[13];
      tmp2 += traveler[3+width*2] * filter[12];
      tmp3 += traveler[3+width*2] * filter[11];
      tmp4 += traveler[4+width*2] * filter[10];
      tmp  += traveler[4+width*2] * filter[14];
      tmp2 += traveler[4+width*2] * filter[13];
      tmp3 += traveler[4+width*2] * filter[12];
      tmp4 += traveler[4+width*2] * filter[11];
      tmp2 += traveler[5+width*2] * filter[14];
      tmp3 += traveler[5+width*2] * filter[13];
      tmp4 += traveler[5+width*2] * filter[12];
      tmp3 += traveler[6+width*2] * filter[14];
      tmp4 += traveler[6+width*2] * filter[13];
      tmp4 += traveler[7+width*2] * filter[14];
      tmp  += traveler[0+width*3] * filter[15];
      tmp  += traveler[1+width*3] * filter[16];
      tmp2 += traveler[1+width*3] * filter[15];
      tmp  += traveler[2+width*3] * filter[17];
      tmp2 += traveler[2+width*3] * filter[16];
      tmp3 += traveler[2+width*3] * filter[15];
      tmp  += traveler[3+width*3] * filter[18];
      tmp2 += traveler[3+width*3] * filter[17];
      tmp3 += traveler[3+width*3] * filter[16];
      tmp4 += traveler[3+width*3] * filter[15];
      tmp  += traveler[4+width*3] * filter[19];
      tmp2 += traveler[4+width*3] * filter[18];
      tmp3 += traveler[4+width*3] * filter[17];
      tmp4 += traveler[4+width*3] * filter[16];
      tmp2 += traveler[5+width*3] * filter[19];
      tmp3 += traveler[5+width*3] * filter[18];
      tmp4 += traveler[5+width*3] * filter[17];
      tmp3 += traveler[6+width*3] * filter[19];
      tmp4 += traveler[6+width*3] * filter[18];
      tmp4 += traveler[7+width*3] * filter[19];
      tmp  += traveler[0+width*4] * filter[20];
      tmp  += traveler[1+width*4] * filter[21];
      tmp2 += traveler[1+width*4] * filter[20];
      tmp  += traveler[2+width*4] * filter[22];
      tmp2 += traveler[2+width*4] * filter[21];
      tmp3 += traveler[2+width*4] * filter[20];
      tmp  += traveler[3+width*4] * filter[23];
      tmp2 += traveler[3+width*4] * filter[22];
      tmp3 += traveler[3+width*4] * filter[21];
      tmp4 += traveler[3+width*4] * filter[20];
      tmp  += traveler[4+width*4] * filter[24];
      tmp2 += traveler[4+width*4] * filter[23];
      tmp3 += traveler[4+width*4] * filter[22];
      tmp4 += traveler[4+width*4] * filter[21];
      tmp2 += traveler[5+width*4] * filter[24];
      tmp3 += traveler[5+width*4] * filter[23];
      tmp4 += traveler[5+width*4] * filter[22];
      tmp3 += traveler[6+width*4] * filter[24];
      tmp4 += traveler[6+width*4] * filter[23];
      tmp4 += traveler[7+width*4] * filter[24];

      output_trav[0] = tmp;
      output_trav[1] = tmp2;
      output_trav[2] = tmp3;
      output_trav[3] = tmp4;

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

int main()
{
  printf("Convolution 5x5\n");
  int32_t filter5x5[5*5];
  static int32_t img[IMG_WIDTH * IMG_HEIGHT];
  static int32_t ref_output[IMG_WIDTH * IMG_HEIGHT];
  static int32_t opt_output[IMG_WIDTH * IMG_HEIGHT];

  memset(ref_output, 0, sizeof(uint32_t) * IMG_WIDTH * IMG_HEIGHT);
  memset(opt_output, 0, sizeof(uint32_t) * IMG_WIDTH * IMG_HEIGHT);

  setup5x5Filter(filter5x5);
  setupImage(img, IMG_WIDTH, IMG_HEIGHT);

  struct timespec start, end;

  clock_gettime(CLOCK_MONOTONIC, &start);
  applyFilterToImage_ref(filter5x5, img, ref_output, IMG_WIDTH, IMG_HEIGHT);
  clock_gettime(CLOCK_MONOTONIC, &end);
  print_timediff("Reference", &start, &end);

  clock_gettime(CLOCK_MONOTONIC, &start);
  applyFilterToImage_opt(filter5x5, img, opt_output, IMG_WIDTH, IMG_HEIGHT);
  clock_gettime(CLOCK_MONOTONIC, &end);
  print_timediff("Optimized", &start, &end);

  uint32_t missmatches = verifyImages(ref_output, opt_output, IMG_WIDTH, IMG_HEIGHT);
  if(missmatches != 0)
  {
    printf("\e[38;5;1;5mMissmatched %d/%d\e[0m\n", missmatches, IMG_WIDTH*IMG_HEIGHT);
  } else {
    printf("\e[38;5;46mMissmatched %d/%d\e[0m\n", missmatches, IMG_WIDTH*IMG_HEIGHT);
  }

  //#ifdef __NEON__
  clock_gettime(CLOCK_MONOTONIC, &start);
  applyFilterToImage_neon(filter5x5, img, opt_output, IMG_WIDTH, IMG_HEIGHT);
  clock_gettime(CLOCK_MONOTONIC, &end);
  print_timediff("Neon     ", &start, &end);
  missmatches = verifyImages(ref_output, opt_output, IMG_WIDTH, IMG_HEIGHT);
  if(missmatches != 0)
  {
    printf("\e[38;5;1;5mMissmatched %d/%d\e[0m\n", missmatches, IMG_WIDTH*IMG_HEIGHT);
  } else {
    printf("\e[38;5;46mMissmatched %d/%d\e[0m\n", missmatches, IMG_WIDTH*IMG_HEIGHT);
  }
  //#endif /* __NEON__ */
}
