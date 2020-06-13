#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "image_dump_tools.h"

#define POSITION_MARKER_SIZE 7
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

static uint8_t qrbuffer[21*21];

void generateFormat(uint8_t *info, EC_LEVEL ec_level, MASK_TYPE mask_type) {
  printf("EC level : %d\n", ec_level);
  info[0] = 1;
  info[1] = 0;
  info[2] = 1;
  info[13] = (ec_level & 1) ? 1 : 0;
  info[14] = (ec_level & 2) ? 1 : 0;
}

void drawFormat(uint8_t *buf, const uint8_t *info, uint32_t width) {
  uint32_t info_index = 0;
  for(uint32_t i=0; i<6; ++i) {
    buf[(i) * width + 8] = info[info_index];
    info_index++;
  }
  /*for(uint32_t i=0; i<POSITION_MARKER_SIZE - 1; ++i) {
    buf[(POSITION_MARKER_SIZE + 1) * width + i] = info[info_index];
    info_index++;
  }*/
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
  buf[(width - 7) * width + 8] = 1;
  printf("Width %u\n", realEstate);
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

  uint8_t format[15] = {0};
  generateFormat(format, EC_LEVEL_LOW, MASK_HOR_INTERLEAVE);
  drawFormat(qrbuffer, format, 21);

  saveAsTextPbm("image.ppm", qrbuffer, 21, 21);
  return 0;
}
