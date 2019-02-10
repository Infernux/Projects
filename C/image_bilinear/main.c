#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "interpolate.h"
#include "image_processing.h"

#define MAX_WIDTH   2000
#define MAX_HEIGHT  1500

void convertBinaryPGMToTextPGM(const char *path)
{
  uint8_t buff[MAX_WIDTH * MAX_HEIGHT];
  int width, height, max_val;
  loadImage(path, buff, &width, &height, &max_val);

  printf("width : %d, height : %d\n", width, height);
  printf("max val : %d\n", max_val);

  saveAsTextPgm("pgmed.pgm", buff, width, height, max_val);
}

void main(int argc, char **argv)
{
  uint8_t buff[MAX_WIDTH * MAX_HEIGHT];
  int width, height, max_val;
  loadImage(argv[1], buff, &width, &height, &max_val);

  printf("width : %d, height : %d\n", width, height);
  printf("max val : %d\n", max_val);

  uint8_t *output = addBorderToImage(buff, width, height, 0, 1, 0, 1);

  uint8_t *doubled_image = doubleImage(output, width, height, width + 1);
  free(output);

  saveAsTextPgm("pgmed.pgm", doubled_image, width * 2, height * 2, max_val);
  free(doubled_image);
}
