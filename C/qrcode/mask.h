#ifndef MASK_H__
#define MASK_H__

#include <inttypes.h>

typedef enum MASK_TYPE_ {
  MASK_1=0, /* (i+j) % 2 == 0 */
  MASK_2, /* j % 2 == 0 */
  MASK_3, /* x % 3 == 0 */
  MASK_4, /* (i+j) % 3 == 0 */
  MASK_HOR_INTERLEAVE, /* (floor(j/2) + floor(i/3) % 2) == 0 */
  MASK_CHECKERBOARD, /* (((i*j) % 2) + ((i*j)%3)) == 0 */
  MASK_DIAGONAL_WAVE, /* (((i*j)%2)+(i*j)%3)%2 == 0*/
  MASK_VERTICAL_INTERLEAVE /* (((i*j)%2)+((i*j)%3))%2 == 0 */
} MASK_TYPE;

void maskData(uint8_t *qrbuffer, const uint32_t width, MASK_TYPE mask_type);

#endif /* MASK_H__ */
