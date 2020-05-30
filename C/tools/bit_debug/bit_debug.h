#ifndef BIT_DEBUG_H__
#define BIT_DEBUG_H__

#include <stdlib.h>

#define PRINT_BYTE(x) \
{\
\
for(uint32_t bit = 0; bit < 8; ++bit) { \
  printf("%d", (x&(1<<(7-bit)))>>(7-bit));\
} \
}

#ifdef __ARM_NEON
#include "arm_neon.h"
void print_int8x8_t(const char *title, int8x8_t v);
void print_int16x4_t(const char *title, int16x4_t v);
void print_uint8x8_t(const char *title, uint8x8_t v);
void print_uint8x16_t(const char *title, uint8x16_t v);
void print_uint16x4_t(const char *title, uint16x4_t v);
void print_uint16x8_t(const char *title, uint16x8_t v);
#endif /* __ARM_NEON */

#endif /* BIT_DEBUG_H__ */
