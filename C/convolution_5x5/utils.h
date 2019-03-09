#ifndef UTILS_H__
#define UTILS_H__

#include <inttypes.h>
#include <time.h>

void setup5x5Filter(int32_t *filter);
void setupImage(int32_t *img, uint32_t width, uint32_t height);
uint32_t verifyImages(int32_t *image_1, int32_t *image_2, uint32_t width, uint32_t height);
void print_timediff(char *text, struct timespec *start, struct timespec *end);

#endif /* UTILS_H__ */
