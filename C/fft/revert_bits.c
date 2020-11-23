#include "revert_bits.h"

#include <math.h>

uint32_t revert_bits(const uint32_t val, const uint32_t bitcount) {
  uint32_t acc = 0;
  uint32_t mask = (uint32_t)pow(2, bitcount - 1); /* obviously use shift */
  uint32_t shift = (bitcount - 1);

  for(int i = 0; i < (bitcount / 2); ++i) {
    acc |= ((val & mask) >> shift);
    mask /= 2;
    shift -= 2;
  }

  if(bitcount & 1) {
    acc |= (val & mask);
    mask /= 2;
  }

  for(int i = 0; i < (bitcount / 2); ++i) {
    shift += 2;
    acc |= ((val & mask) << shift);
    mask /= 2;
  }

  return acc;
}
