#include "utils.h"

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void setup5x5Filter(int32_t *filter)
{
  uint32_t i;
  srand(time(NULL));
  for(i=0; i<25; ++i)
  {
#ifdef RANDOM_VALS
    filter[i] = rand();
#else
    filter[i] = i%5;
#endif
  }
}

void setupImage(int32_t *img, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  srand(time(NULL));
  for(j=0; j<height; ++j)
  {
    for(i=0; i<width; ++i)
    {
#ifdef RANDOM_VALS
      img[j*width + i] = rand();
#else
      img[j*width + i] = i + j*width;
#endif
    }
  }
}

uint32_t verifyImages(int32_t *image_1, int32_t *image_2, uint32_t width, uint32_t height)
{
  uint32_t i,j;
  uint32_t missmatches = 0;
  for(j=0; j<height; ++j)
  {
    for(i=0; i<width; ++i)
    {
      if(image_1[j*width + i] != image_2[j*width + i])
      {
#ifdef PRINT_DIFF
        printf("x:%d y:%d (%d instead of %d)\n", i, j, image_2[j*width + i], image_1[j*width + i]);
#endif /* PRINT_DIFF */
        missmatches++;
      }
    }
  }
  return missmatches;
}

void print_timediff(char *text, struct timespec *start, struct timespec *end)
{
  int s = end->tv_sec - start->tv_sec;
  long ns = end->tv_nsec - start->tv_nsec;
  if(end->tv_sec != start->tv_sec)
  {
    ns = 1e9 - ns;
  }

  printf("%s : %ds %10ldns (%ldus)\n", text, s, ns, (long)(ns / 10e3));
}
