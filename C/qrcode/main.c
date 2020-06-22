#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "ecc.h"
#include "galois_helper.h"
#include "image_dump_tools.h"
#include "mask.h"
#include "message_encoding_helpers.h"
#include "qrcode_constants.h"

#define pp(m, count) \
{ \
  for(uint32_t i=0; i<count; ++i) { \
    printf("%d", m[i]); \
  } \
  printf("\n"); \
}

#define FORMAT_LENGTH 15

#define ONE_SET  3
#define ZERO_SET 2
#define SEPARATOR_SIZE 1

#define PADDING_PATTERN_1 0xEC
#define PADDING_PATTERN_2 0x11

#define min(a,b) (a<b?a:b)

static void drawData(uint8_t *buf, const uint8_t *message, const uint32_t width);
static void drawPlaceholders(uint8_t *qrbuffer, const uint32_t width, const VERSION version);

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

#define ENCODING_LEN 4

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

void debugDrawData(const uint32_t width, const uint32_t version) {
  uint8_t message_buffer[1024] = {0};
  char path[100];
  memset(message_buffer, 0, 1024);
  for(int i=0; i<208; ++i) {
    sprintf(path, "dump/image_%03d.ppm", i);
    message_buffer[i] = 1;
    drawPlaceholders(qrbuffer, width, version);
    drawData(qrbuffer, message_buffer, COMPUTE_SIZE(version));
    saveAsTextPbm(path, qrbuffer, COMPUTE_SIZE(version), COMPUTE_SIZE(version), RESIZE_FACTOR);

    memset(qrbuffer, 0, sizeof(uint8_t) * COMPUTE_SIZE(VERSION_1)*COMPUTE_SIZE(VERSION_1));
  }
}

void generateFormat(uint8_t *info, EC_LEVEL ec_level, MASK_TYPE mask_type) {
  ERROR_CORRECTION_MASK_BITS ec_mask;
  switch(ec_level) {
    case EC_LEVEL_MED:
      ec_mask = ERROR_CORRECTION_MASK_BITS_M;
      break;
    case EC_LEVEL_Q:
      ec_mask = ERROR_CORRECTION_MASK_BITS_Q;
      break;
    case EC_LEVEL_HIGH:
      ec_mask = ERROR_CORRECTION_MASK_BITS_H;
      break;
    case EC_LEVEL_LOW:
      ec_mask = ERROR_CORRECTION_MASK_BITS_L;
      break;
  }
  printf("error %d\n", ec_mask);
  uint16_t format = generateErrorCorrectionBits(ec_mask, mask_type);
  #if 1
  for(uint32_t i=0; i<15; i++) {
    info[i] = (format & (1<<i)) ? 1 : 0;
  }
  printf("format %d\n", format);
  #endif
}

void drawFormat(uint8_t *buf, const uint8_t *info, uint32_t width) {
  /* top left */
  uint32_t info_index = 0;
  for(uint32_t i=0; i<6; ++i) {
    buf[(i) * width + (POSITION_MARKER_SIZE + 1)] = info[info_index++];
  }
  buf[(POSITION_MARKER_SIZE * width + (POSITION_MARKER_SIZE+1))] = info[info_index++];
  buf[((POSITION_MARKER_SIZE+1) * width + (POSITION_MARKER_SIZE+1))] = info[info_index++];
  buf[((POSITION_MARKER_SIZE+1) * width + (POSITION_MARKER_SIZE))] = info[info_index++];

  for(int32_t i=5; i>=0; --i) {
    buf[(POSITION_MARKER_SIZE + 1) * width + i] = info[info_index];
    info_index++;
  }

  /* bottom left && top right */
  info_index = FORMAT_LENGTH-1;
  for(uint32_t i=0; i<7; ++i) {
    buf[(width - 1 - i) * width + (POSITION_MARKER_SIZE + 1)] = info[info_index--];
  }
  for(uint32_t i=0; i<8; ++i) {
    buf[(POSITION_MARKER_SIZE + 2) * width - (POSITION_MARKER_SIZE + 1) + i] = info[info_index--];
  }
}

void drawTiming(uint8_t *buf, uint32_t width, VERSION version) {
  uint32_t realEstate = width - 2 * POSITION_MARKER_SIZE;
  for(uint32_t i=0; i<realEstate; ++i) {
    if(i & 1) {
      buf[(width * 6) + (POSITION_MARKER_SIZE + i)] = 1;
    } else {
      buf[(width * 6) + (POSITION_MARKER_SIZE + i)] = 0;
    }
  }
  for(uint32_t i=0; i<realEstate; ++i) {
    if(i & 1) {
      buf[(width * (POSITION_MARKER_SIZE + i)) + 6] = 1;
    } else {
      buf[(width * (POSITION_MARKER_SIZE + i)) + 6] = 0;
    }
  }
  buf[(4 * version + 9) * width + 8] = 1; /* dark module */
}

void drawMarker(uint8_t *buf, uint32_t width) {
  memset(buf, 1, sizeof(uint8_t) * POSITION_MARKER_SIZE);
  buf[width * 1 + 0] = 1;
  memset(&buf[width * 1 + 1], 0, sizeof(uint8_t) * 5);
  buf[width * 1 + 6] = 1;
  for(uint32_t i=0; i<3; ++i) {
    buf[(width * (2 + i)) + 0] = 1;
    buf[(width * (2 + i)) + 1] = 0;
    memset(&buf[(width * (2 + i)) + 2], 1, sizeof(uint8_t) * 3);
    buf[(width * (2 + i)) + 5] = 0;
    buf[(width * (2 + i)) + 6] = 1;
  }
  buf[width * 5 + 0] = 1;
  memset(&buf[width * 5 + 1], 0, sizeof(uint8_t) * 5);
  buf[width * 5 + 6] = 1;
  memset(&buf[width * 6], 1, sizeof(uint8_t) * POSITION_MARKER_SIZE);
}

void setPositionMarker(uint8_t *buf, const uint32_t width) {
  drawMarker(buf, width);
  drawMarker(&buf[width-POSITION_MARKER_SIZE], width);
  drawMarker(&buf[(width-POSITION_MARKER_SIZE) * width], width);
}

static void setSeparators(uint8_t *buf, uint32_t width) {
  /* top left */
  memset(&buf[POSITION_MARKER_SIZE * width], 0, POSITION_MARKER_SIZE+1);
  for(uint32_t i=0; i<(POSITION_MARKER_SIZE + SEPARATOR_SIZE); ++i) {
    buf[(i*width) + (POSITION_MARKER_SIZE)] = 0;
  }

  /* top right */
  memset(&buf[POSITION_MARKER_SIZE * width + (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE)], 0, POSITION_MARKER_SIZE+SEPARATOR_SIZE);
  for(uint32_t i=0; i<(POSITION_MARKER_SIZE + SEPARATOR_SIZE); ++i) {
    buf[(i*width) + (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE)] = 0;
  }

  /* bottom left */
  memset(&buf[width * (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE)], 0, POSITION_MARKER_SIZE+SEPARATOR_SIZE);
  for(uint32_t i=0; i<(POSITION_MARKER_SIZE + SEPARATOR_SIZE); ++i) {
    buf[(width * (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE + i)) + (POSITION_MARKER_SIZE)] = 0;
  }
}

static void setPlaceHolderSeparators(uint8_t *buf, uint32_t width) {
  /* top left */
  memset(&buf[POSITION_MARKER_SIZE * width], ZERO_SET, POSITION_MARKER_SIZE+1);
  for(uint32_t i=0; i<(POSITION_MARKER_SIZE + SEPARATOR_SIZE); ++i) {
    buf[(i*width) + (POSITION_MARKER_SIZE)] = ZERO_SET;
  }

  /* top right */
  memset(&buf[POSITION_MARKER_SIZE * width + (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE)], ZERO_SET, POSITION_MARKER_SIZE+SEPARATOR_SIZE);
  for(uint32_t i=0; i<(POSITION_MARKER_SIZE + SEPARATOR_SIZE); ++i) {
    buf[(i*width) + (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE)] = ZERO_SET;
  }

  /* bottom left */
  memset(&buf[width * (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE)], ZERO_SET, POSITION_MARKER_SIZE+SEPARATOR_SIZE);
  for(uint32_t i=0; i<(POSITION_MARKER_SIZE + SEPARATOR_SIZE); ++i) {
    buf[(width * (width - POSITION_MARKER_SIZE - SEPARATOR_SIZE + i)) + (POSITION_MARKER_SIZE)] = ZERO_SET;
  }
}

void encodeMessage(const char *string, const uint32_t length, const ENCODING encoding, const uint32_t max_len, uint8_t *encoded) {
  uint32_t bit_count = 0;
  encoded[bit_count++] = encoding & 8 ? 1 : 0;
  encoded[bit_count++] = encoding & 4 ? 1 : 0;
  encoded[bit_count++] = encoding & 2 ? 1 : 0;
  encoded[bit_count++] = encoding & 1 ? 1 : 0;

  switch(encoding) {
    case ENCODING_NUMERIC:
      encoded[bit_count++] = length & (1 << 9) ? 1 : 0;
    case ENCODING_ALPHANUMERIC:
      encoded[bit_count++] = length & (1 << 8) ? 1 : 0;
    case ENCODING_BYTE:
    case ENCODING_KANJI:
      encoded[bit_count++] = length & (1 << 7) ? 1 : 0;
      encoded[bit_count++] = length & (1 << 6) ? 1 : 0;
      encoded[bit_count++] = length & (1 << 5) ? 1 : 0;
      encoded[bit_count++] = length & (1 << 4) ? 1 : 0;
      encoded[bit_count++] = length & (1 << 3) ? 1 : 0;
      encoded[bit_count++] = length & (1 << 2) ? 1 : 0;
      encoded[bit_count++] = length & (1 << 1) ? 1 : 0;
      encoded[bit_count++] = length & (1 << 0) ? 1 : 0;
  }

  switch(encoding) {
    case ENCODING_NUMERIC:
      bit_count += encodeMessageNumeric(string, length, &encoded[bit_count]);
      break;
    case ENCODING_ALPHANUMERIC:
      bit_count += encodeMessageAlphanumeric(string, length, &encoded[bit_count]);
      break;
    case ENCODING_BYTE:
      break;
    case ENCODING_KANJI:
      break;
    case ENCODING_ECI:
      break;
    default:
      printf("Unknown encoding\n");
      exit(1);
  }

  printf("bit count : %d\n", bit_count);

  /* if there's enough space, add "the" terminator */
  for(uint32_t i = 0; i < min(4, max_len - bit_count); i++) {
    encoded[bit_count++] = 0;
  }

  printf("bit count after terminator : %d\n", bit_count);

  /* add zeroes to make it a multiple of 8 */
  if((bit_count & 0x7) != 0) {
    for(uint32_t i = bit_count % 8; i < 8; ++i) {
      encoded[bit_count++] = 0;
    }
  }

  printf("bit count after 8 rounding : %d\n", bit_count);

  /* pad the remaining codewords */
  uint32_t remaining_bytes = (max_len - bit_count) / 8;
  if(remaining_bytes != 0) {
    for(uint32_t needed_pads = remaining_bytes; needed_pads > 0; --needed_pads) {
      if((needed_pads % 2)) {
        for(int32_t i=7; i>=0; i--) {
          encoded[bit_count++] = PADDING_PATTERN_2 & (1<<i) ? 1 : 0;
        }
      } else {
        for(int32_t i=7; i>=0; i--) {
          encoded[bit_count++] = PADDING_PATTERN_1 & (1<<i) ? 1 : 0;
        }
      }
    }
  }
  printf("bit count after padding : %d\n", bit_count);

#if 0
  for(uint32_t i = 0; i<bit_count; ++i) {
    if(i%8==0)
      printf(" ");
    printf("%d", encoded[i]);
  }
  printf("\n");
#endif
}

static void drawData(uint8_t *buf, const uint8_t *message, const uint32_t width) {
  uint32_t index = 0;
  uint8_t direction = 1;
  for(uint32_t x = 0; x < width - 1; x+=2) {
    if(x == (width - POSITION_MARKER_SIZE)) {
      /* skip timing */
      x++;
    }

    uint32_t startPoint = 0;
    if(direction == 0) {
      startPoint = width - x - 1;
      for(uint32_t y = 0; y < width; y++) {
        for(uint32_t xind = 0; xind < 2; xind++) {
          if(buf[startPoint + (y*width) - xind] == 0) {
            buf[startPoint + (y*width) - xind] = message[index++];
          }
        }
      }
      direction = !direction;
    } else {
      startPoint = (width * width) - x - 1;
      for(uint32_t y = 0; y < width; y++) {
        for(uint32_t xind = 0; xind < 2; xind++) {
          if(buf[startPoint - (y*width) - xind] == 0) {
            buf[startPoint - (y*width) - xind] = message[index++];
          }
        }
      }
      direction = !direction;
    }
  }
  printf("Drew : %d\n", index);
}

static void drawPlaceholderMarker(uint8_t *qrbuffer, uint32_t width) {
  memset(qrbuffer, ZERO_SET, POSITION_MARKER_SIZE);
  memset(&qrbuffer[width*1], ZERO_SET, POSITION_MARKER_SIZE);
  memset(&qrbuffer[width*2], ZERO_SET, POSITION_MARKER_SIZE);
  memset(&qrbuffer[width*3], ZERO_SET, POSITION_MARKER_SIZE);
  memset(&qrbuffer[width*4], ZERO_SET, POSITION_MARKER_SIZE);
  memset(&qrbuffer[width*5], ZERO_SET, POSITION_MARKER_SIZE);
  memset(&qrbuffer[width*6], ZERO_SET, POSITION_MARKER_SIZE);
}

void drawPlaceholderTimings(uint8_t *qrbuffer, const uint32_t width, const VERSION version) {
  uint32_t realEstate = width - 2 * POSITION_MARKER_SIZE;
  for(uint32_t i=0; i<realEstate; ++i) {
    qrbuffer[(width * 6) + (POSITION_MARKER_SIZE + i)] = ZERO_SET;
  }
  for(uint32_t i=0; i<realEstate; ++i) {
    qrbuffer[(width * (POSITION_MARKER_SIZE + i)) + 6] = ZERO_SET;
  }
  qrbuffer[(4 * version + 9) * width + 8] = ZERO_SET; /* dark module */
}

void drawFormatPlaceholder(uint8_t *qrqrbufferfer, const uint32_t width) {
  /* top left */
  for(uint32_t i=0; i<6; ++i) {
    qrbuffer[(i) * width + (POSITION_MARKER_SIZE + 1)] = ZERO_SET;
  }
  qrbuffer[(POSITION_MARKER_SIZE * width + (POSITION_MARKER_SIZE+1))] = ZERO_SET;
  qrbuffer[((POSITION_MARKER_SIZE+1) * width + (POSITION_MARKER_SIZE+1))] = ZERO_SET;
  qrbuffer[((POSITION_MARKER_SIZE+1) * width + (POSITION_MARKER_SIZE))] = ZERO_SET;

  for(int32_t i=5; i>=0; --i) {
    qrbuffer[(POSITION_MARKER_SIZE + 1) * width + i] = ZERO_SET;
  }

  /* bottom left && top right */
  for(uint32_t i=0; i<7; ++i) {
    qrbuffer[(width - 1 - i) * width + (POSITION_MARKER_SIZE + 1)] = ZERO_SET;
  }
  for(uint32_t i=0; i<8; ++i) {
    qrbuffer[(POSITION_MARKER_SIZE + 2) * width - (POSITION_MARKER_SIZE + 1) + i] = ZERO_SET;
  }
}

static void drawPlaceholders(uint8_t *qrbuffer, const uint32_t width, const VERSION version) {
  /* finders */
  drawPlaceholderMarker(qrbuffer, width);
  drawPlaceholderMarker(&qrbuffer[width-POSITION_MARKER_SIZE], width);
  drawPlaceholderMarker(&qrbuffer[(width-POSITION_MARKER_SIZE) * width], width);

  /* spacings */
  setPlaceHolderSeparators(qrbuffer, width);

  /* format */
  drawFormatPlaceholder(qrbuffer, width);

  /* timings */
  drawPlaceholderTimings(qrbuffer, width, version);
}

void drawRealFixed(uint8_t *qrbuffer, const uint32_t width, const VERSION version, const EC_LEVEL ec_level, const MASK_TYPE masktype) {
  setPositionMarker(qrbuffer, width);
  setSeparators(qrbuffer, width);
  drawTiming(qrbuffer, width, version);

  uint8_t format[FORMAT_LENGTH] = {0};
  generateFormat(format, ec_level, masktype);
  drawFormat(qrbuffer, format, width);
}

void encodeMessageAndECC(uint8_t *message_buffer, const char *message_to_encode, const uint32_t message_length, const ENCODING encoding, const uint32_t codeword_count, const uint32_t ecc_count) {
  encodeMessage(message_to_encode, message_length, encoding, codeword_count * 8, message_buffer);

  computeECC(message_buffer, codeword_count, ecc_count, &message_buffer[codeword_count * 8]);
}

void getWordsCountFromECCLevel(const EC_LEVEL eclevel, uint32_t *data_codeword_count, uint32_t *ecc_codeword_count) {
  switch(eclevel) {
    case EC_LEVEL_LOW:
      *data_codeword_count = V1_L_CODEWORD_COUNT;
      *ecc_codeword_count  = V1_L_EC_COUNT;
      break;
    case EC_LEVEL_MED:
      *data_codeword_count = V1_M_CODEWORD_COUNT;
      *ecc_codeword_count  = V1_M_EC_COUNT;
      break;
    case EC_LEVEL_Q:
      *data_codeword_count = V1_Q_CODEWORD_COUNT;
      *ecc_codeword_count  = V1_Q_EC_COUNT;
      break;
    case EC_LEVEL_HIGH:
      *data_codeword_count = V1_H_CODEWORD_COUNT;
      *ecc_codeword_count  = V1_H_EC_COUNT;
      break;
  }
}

int main() {
  initialize_gf256(QRCODE_ECC_MODULO);
  memset(qrbuffer, 0, sizeof(uint8_t) * COMPUTE_SIZE(VERSION_1)*COMPUTE_SIZE(VERSION_1));

  printf("Qrcode\n");
  VERSION version = VERSION_1;
  EC_LEVEL eclevel = EC_LEVEL_MED;
  uint32_t codewordcount, eccount;
  getWordsCountFromECCLevel(eclevel, &codewordcount, &eccount);
  MASK_TYPE mask_type = MASK_1;
  uint32_t width = COMPUTE_SIZE(version);
  drawPlaceholders(qrbuffer, width, version);

  /*
   * should pack into a single byte but ... not for now
   * right now, a single output bit is stored into one byte
   * */
  uint8_t message_buffer[1024] = {0};
#if 1
  memset(message_buffer, 0, 1024);
  encodeMessageAndECC(message_buffer, "BONJOUR", 7, ENCODING_ALPHANUMERIC, codewordcount, eccount);

  drawData(qrbuffer, message_buffer, COMPUTE_SIZE(version));
  maskData(qrbuffer, width, mask_type);
  drawRealFixed(qrbuffer, width, version, eclevel, mask_type);
  saveAsTextPbm("image.pbm", qrbuffer, COMPUTE_SIZE(version), COMPUTE_SIZE(version), RESIZE_FACTOR);
#else
  debugDrawData(width, version);
#endif
  return 0;
}
