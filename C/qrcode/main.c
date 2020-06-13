#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "bit_debug.h"
#include "image_dump_tools.h"

#define FORMAT_LENGTH 15

static uint32_t get_significant_bit_count(uint32_t val, uint32_t max_length)
{
  uint32_t length = max_length;
  for(int32_t i=max_length-1; i>=0; i--) {
    if((val & (1 << i)) == 0) {
      length--;
    } else {
      break;
    }
  }
  return length;
}

#define REMOVE_HEAD_0_U16(val, starting) \
{ \
  for(int32_t i=0; i<starting; i++) { \
    if((val & (1<<(starting-1)))==0) { \
      val<<=1; \
    } else { \
      break; \
    } \
  } \
}

#define RESIZE_FACTOR 20

#define POSITION_MARKER_SIZE 7
#define QR_BASE_SIZE 17
#define COMPUTE_SIZE(version) (QR_BASE_SIZE + 4*version)

typedef enum VERSION_ {
  VERSION_1=1,
  VERSION_2
} VERSION;

typedef enum EC_LEVEL_ {
  EC_LEVEL_HIGH = 0,
  EC_LEVEL_Q,
  EC_LEVEL_MED,
  EC_LEVEL_LOW
} EC_LEVEL;

typedef enum MASK_TYPE_ {
  MASK_1=0,
  MASK_2,
  MASK_3,
  MASK_4,
  MASK_HOR_INTERLEAVE,
  MASK_CHECKERBOARD,
  MASK_DIAGONAL_WAVE,
  MASK_VERTICAL_INTERLEAVE /* j % 3 == 0 */
} MASK_TYPE;

typedef enum ERROR_CORRECTION_MASK_BITS_ {
  ERROR_CORRECTION_MASK_BITS_M=0,
  ERROR_CORRECTION_MASK_BITS_L,
  ERROR_CORRECTION_MASK_BITS_H,
  ERROR_CORRECTION_MASK_BITS_Q
} ERROR_CORRECTION_MASK_BITS;

static uint8_t qrbuffer[COMPUTE_SIZE(VERSION_1)*COMPUTE_SIZE(VERSION_1)];

/* polynome : x^10 + x^8 + x^5 + x^4 + x^2 + x + 1 */
#define GENERATOR_POLYNOME ((1<<10)|(1<<8)|(1<<5)|(1<<4)|(1<<2)|(1<<1)|(1))
#define GENERATOR_POLYNOME_LENGTH (11)
#define ERROR_CORRECTION_BIT_XOR_MASK (0x5412) /* 101010000010010 */
static uint16_t generateErrorCorrectionBits(const ERROR_CORRECTION_MASK_BITS ecmb, const MASK_TYPE mt) {
  uint16_t base_ecb = (ecmb << 3) + mt;
  base_ecb <<= 10;
  uint16_t ecb = base_ecb;
  uint32_t ecb_len = get_significant_bit_count(ecb, 15);
  while(ecb_len >= GENERATOR_POLYNOME_LENGTH) {
    uint32_t padded_generator_polynome = GENERATOR_POLYNOME << (ecb_len - GENERATOR_POLYNOME_LENGTH);
    ecb = ecb ^ padded_generator_polynome;
    ecb_len = get_significant_bit_count(ecb, 15);
  }
  base_ecb += ecb;
  base_ecb = base_ecb ^ ERROR_CORRECTION_BIT_XOR_MASK;
  return base_ecb;
}

void generateFormat(uint8_t *info, EC_LEVEL ec_level, MASK_TYPE mask_type) {
  uint16_t format = generateErrorCorrectionBits(ERROR_CORRECTION_MASK_BITS_L, mask_type);
  for(uint32_t i=0; i<15; i++) {
    info[i] = (format & 1<<((FORMAT_LENGTH-1)-i)) ? 1 : 0;
  }
}

void drawFormat(uint8_t *buf, const uint8_t *info, uint32_t width) {
  uint32_t info_index = FORMAT_LENGTH-1;
  for(uint32_t i=0; i<6; ++i) {
    buf[(i) * width + 8] = info[info_index--];
  }
  buf[(7 * width + 8)] = info[info_index--];
  buf[(8 * width + 8)] = info[info_index--];
  buf[(8 * width + 7)] = info[info_index--];

  for(int32_t i=5; i>=0; --i) {
    buf[(POSITION_MARKER_SIZE + 1) * width + i] = info[info_index];
    info_index--;
  }
}

void drawTiming(uint8_t *buf, uint32_t width) {
  uint32_t realEstate = width - 2 * POSITION_MARKER_SIZE;
  for(uint32_t i=0; i<realEstate; ++i) {
    if(i & 1) {
      buf[(width * 6) + (7 + i)] = 1;
    }
  }
  for(uint32_t i=0; i<realEstate; ++i) {
    if(i & 1) {
      buf[(width * (7 + i)) + 6] = 1;
    }
  }
  buf[(width - 8) * width + 8] = 1;
}

void drawMarker(uint8_t *buf, uint32_t width) {
  memset(buf, 1, sizeof(uint8_t) * POSITION_MARKER_SIZE);
  buf[width * 1 + 0] = 1;
  buf[width * 1 + 6] = 1;
  for(uint32_t i=0; i<3; ++i) {
    buf[(width * (2 + i)) + 0] = 1;
    memset(&buf[(width * (2 + i)) + 2], 1, sizeof(uint8_t) * 3);
    buf[(width * (2 + i)) + 6] = 1;
  }
  buf[width * 5 + 0] = 1;
  buf[width * 5 + 6] = 1;
  memset(&buf[width * 6], 1, sizeof(uint8_t) * POSITION_MARKER_SIZE);
}

void setPositionMarker(uint8_t *buf, uint32_t width) {
  drawMarker(buf, width);
  drawMarker(&buf[width-7], width);
  drawMarker(&buf[(width-7) * width], width);
}

int main() {
  printf("Qrcode\n");
  setPositionMarker(qrbuffer, 21);
  drawTiming(qrbuffer, 21);

  uint8_t format[FORMAT_LENGTH] = {0};
  generateFormat(format, EC_LEVEL_LOW, MASK_HOR_INTERLEAVE);
  drawFormat(qrbuffer, format, 21);

  saveAsTextPbm("image.ppm", qrbuffer, 21, 21, RESIZE_FACTOR);
  return 0;
}
