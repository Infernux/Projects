#ifndef IMAGE_PROCESSING__H_
#define IMAGE_PROCESSING__H_

#include <stdint.h>

int loadImage(const char *path, uint8_t *image, int *width, int *height, int *max_val);
int saveAsTextPgm(const char *path, const uint8_t *image, const int width, const int height, const int max_val);

#endif /* IMAGE_PROCESSING__H_ */
