#include "mask.h"

void maskData(uint8_t *qrbuffer, const uint32_t width, MASK_TYPE mask_type) {
  switch(mask_type) {
    case MASK_1:
      for(uint32_t y=0; y<width; ++y) {
        for(uint32_t x=0; x<width; ++x) {
          if(((x+y) % 2) == 0) {
            qrbuffer[y*width+x] = !qrbuffer[y*width+x];
          }
        }
      }
      break;
    case MASK_2:
      break;
    case MASK_3:
      break;
    case MASK_4:
      break;
    case MASK_HOR_INTERLEAVE:
      break;
    case MASK_CHECKERBOARD:
      break;
    case MASK_DIAGONAL_WAVE:
      break;
    case MASK_VERTICAL_INTERLEAVE:
      for(uint32_t y=0; y<width; ++y) {
        for(uint32_t x=0; x<width; ++x) {
          if(y % 3 == 0) {
            qrbuffer[y*width+x] = !qrbuffer[y*width+x];
          }
        }
      }
      break;
  }
}
