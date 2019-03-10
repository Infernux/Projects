#ifndef NEON_IMPL_H__
#define NEON_IMPL_H__

#include <inttypes.h>

void applyFilterToImage_neon(int32_t *filter, int32_t *image, int32_t *output, uint32_t width, uint32_t height);

#endif /* NEON_IMPL_H__ */
