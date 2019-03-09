#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "utils.h"

#define IMG_HEIGHT  500
#define IMG_WIDTH   500

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
  uint32_t i,j,k,l;
  for(j=0; j<height-5; ++j)
  {
    for(i=0; i<width-5; ++i)
    {
      int32_t tmp = 0;
      for(k=0; k<5; k++)
      {
        tmp += image[(j+k)*width+i] * filter[k*5];
        tmp += image[(j+k)*width+i+1] * filter[k*5+1];
        tmp += image[(j+k)*width+i+2] * filter[k*5+2];
        tmp += image[(j+k)*width+i+3] * filter[k*5+3];
        tmp += image[(j+k)*width+i+4] * filter[k*5+4];
      }
      output[j*width + i] = tmp;
    }
  }
}

int main()
{
  printf("Convolution 5x5\n");
  int32_t filter5x5[5*5];
  static int32_t img[IMG_WIDTH * IMG_HEIGHT];
  static int32_t ref_output[IMG_WIDTH * IMG_HEIGHT];
  static int32_t opt_output[IMG_WIDTH * IMG_HEIGHT];

  memset(ref_output, 0, IMG_WIDTH * IMG_HEIGHT);
  memset(opt_output, 0, IMG_WIDTH * IMG_HEIGHT);

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
