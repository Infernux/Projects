#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

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

static inline int32_t filter_one_line(int32_t *filter, int32_t *image)
{
  int32_t tmp;

  tmp  = image[0] * filter[0];
  tmp += image[1] * filter[1];
  tmp += image[2] * filter[2];
  tmp += image[3] * filter[3];
  tmp += image[4] * filter[4];

  return tmp;
}

static void applyFilterToImage_opt(int32_t *filter, int32_t *image, int32_t *output, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  uint32_t h_offset[5] = {
    0,
    width,
    width*2,
    width*3,
    width*4
  };
  for(j=0; j<height-5; ++j)
  {
    for(i=0; i<width-5; i+=2)
    {
      int32_t tmp, tmp2;
      tmp   = filter_one_line(&image[h_offset[0]+i], &filter[0*5]);
      tmp  += filter_one_line(&image[h_offset[1]+i], &filter[1*5]);
      tmp  += filter_one_line(&image[h_offset[2]+i], &filter[2*5]);
      tmp  += filter_one_line(&image[h_offset[3]+i], &filter[3*5]);
      tmp  += filter_one_line(&image[h_offset[4]+i], &filter[4*5]);

      output[h_offset[0] + i] = tmp;

      tmp2   = filter_one_line(&image[h_offset[0]+i+1], &filter[0*5]);
      tmp2  += filter_one_line(&image[h_offset[1]+i+1], &filter[1*5]);
      tmp2  += filter_one_line(&image[h_offset[2]+i+1], &filter[2*5]);
      tmp2  += filter_one_line(&image[h_offset[3]+i+1], &filter[3*5]);
      tmp2  += filter_one_line(&image[h_offset[4]+i+1], &filter[4*5]);

      output[h_offset[0] + i + 1] = tmp2;
    }

    for(; i<width-5; ++i)
    {
      int32_t tmp = 0;
      tmp   = filter_one_line(&image[h_offset[0]+i], &filter[0*5]);
      tmp  += filter_one_line(&image[h_offset[1]+i], &filter[1*5]);
      tmp  += filter_one_line(&image[h_offset[2]+i], &filter[2*5]);
      tmp  += filter_one_line(&image[h_offset[3]+i], &filter[3*5]);
      tmp  += filter_one_line(&image[h_offset[4]+i], &filter[4*5]);

      output[h_offset[0] + i] = tmp;
    }
    h_offset[0]+=width;
    h_offset[1]+=width;
    h_offset[2]+=width;
    h_offset[3]+=width;
    h_offset[4]+=width;
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
}
