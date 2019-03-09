#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define IMG_HEIGHT  50
#define IMG_WIDTH   50

static void setup5x5Filter(int32_t *filter)
{
  uint32_t i;
  for(i=0; i<25; ++i)
  {
    filter[i] = i%5;
  }
}

static void setupImage(int32_t *img, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  for(j=0; j<height; ++j)
  {
    for(i=0; i<width; ++i)
    {
      img[j*width + i] = j*width + i;
    }
  }
}

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

static uint32_t verifyImages(int32_t *image_1, int32_t *image_2, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  uint32_t missmatches = 0;
  for(j=0; j<height-5; ++j)
  {
    for(i=0; i<width-5; ++i)
    {
      if(image_1[j*width + i] != image_2[j*width + i])
      {
        missmatches++;
      }
    }
  }
  return missmatches;
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

  applyFilterToImage_ref(filter5x5, img, ref_output, IMG_WIDTH, IMG_HEIGHT);
  applyFilterToImage_ref(filter5x5, img, opt_output, IMG_WIDTH, IMG_HEIGHT);

  uint32_t missmatches = verifyImages(ref_output, opt_output, IMG_WIDTH, IMG_HEIGHT);
  printf("Missmatched %d/%d\n", missmatches, IMG_WIDTH*IMG_HEIGHT);
}
