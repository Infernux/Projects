#include "utils.h"

#include <stdio.h>

void setup5x5Filter(int32_t *filter)
{
  uint32_t i;
  for(i=0; i<25; ++i)
  {
    filter[i] = i%5;
  }
}

void setupImage(int32_t *img, uint32_t width, uint32_t height)
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

  printf("%s : %ds %10ldns\n", text, s, ns);
}
