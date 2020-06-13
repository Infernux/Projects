#ifndef IMAGE_DUMP_TOOLS__
#define IMAGE_DUMP_TOOLS__

#include <inttypes.h>

void convertBinaryPGMToTextPGM(const char *path);
int loadImage(const char *path, uint8_t *image, int *width, int *height, int *max_val);
int saveAsTextPgm(const char *path, const uint8_t *image, const int width, const int height, const int max_val);
int saveAsTextPbm(const char *path, const uint8_t *image, const int width, const int height, const uint32_t resize_factor);

#endif /* IMAGE_DUMP_TOOLS__ */
