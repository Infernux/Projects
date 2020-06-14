#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "bit_debug.h"
#include "image_dump_tools.h"

#define FORMAT_LENGTH 15

#define ZERO_SET 2
#define SEPARATOR_SIZE 1

#define PADDING_PATTERN_1 0xEC
#define PADDING_PATTERN_2 0x11

#define V1_L_CODEWORD_COUNT 19
#define V1_M_CODEWORD_COUNT 16
#define V1_Q_CODEWORD_COUNT 13
#define V1_H_CODEWORD_COUNT 9
#define V1_L_EC_COUNT 7
#define V1_M_EC_COUNT 10
#define V1_Q_EC_COUNT 13
#define V1_H_EC_COUNT 17

#define min(a,b) (a<b?a:b)

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

typedef enum ENCODING_ {
  ENCODING_NUMERIC = 0x1,
  ENCODING_ALPHANUMERIC = 0x2,
  ENCODING_BYTE = 0x4,
  ENCODING_KANJI = 0x8,
  ENCODING_ECI = 0x7 /* ? */
} ENCODING;

#define ENCODING_LEN 4

#define V1_ENCODING_LEN_NUMERIC 10
#define V1_ENCODING_LEN_ALPHA   9
#define V1_ENCODING_LEN_BYTE    8
#define V1_ENCODING_LEN_KANJI   8

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
    info[i] = (format & 1<<((FORMAT_LENGTH-1)-i)) ? 1 : ZERO_SET;
  }
}

void drawFormat(uint8_t *buf, const uint8_t *info, uint32_t width) {
  /* top left */
  uint32_t info_index = FORMAT_LENGTH-1;
  for(uint32_t i=0; i<6; ++i) {
    buf[(i) * width + (POSITION_MARKER_SIZE + 1)] = info[info_index--];
  }
  buf[(POSITION_MARKER_SIZE * width + (POSITION_MARKER_SIZE+1))] = info[info_index--];
  buf[((POSITION_MARKER_SIZE+1) * width + (POSITION_MARKER_SIZE+1))] = info[info_index--];
  buf[((POSITION_MARKER_SIZE+1) * width + (POSITION_MARKER_SIZE))] = info[info_index--];

  for(int32_t i=5; i>=0; --i) {
    buf[(POSITION_MARKER_SIZE + 1) * width + i] = info[info_index];
    info_index--;
  }

  /* bottom left && top right */
  info_index = 0;
  for(uint32_t i=0; i<7; ++i) {
    buf[(width - 1 - i) * width + (POSITION_MARKER_SIZE + 1)] = info[info_index++];
  }
  for(uint32_t i=0; i<8; ++i) {
    buf[(POSITION_MARKER_SIZE + 2) * width - (POSITION_MARKER_SIZE + 1) + i] = info[info_index++];
  }
}

void drawTiming(uint8_t *buf, uint32_t width, VERSION version) {
  uint32_t realEstate = width - 2 * POSITION_MARKER_SIZE;
  for(uint32_t i=0; i<realEstate; ++i) {
    if(i & 1) {
      buf[(width * 6) + (POSITION_MARKER_SIZE + i)] = 1;
    } else {
      buf[(width * 6) + (POSITION_MARKER_SIZE + i)] = ZERO_SET;
    }
  }
  for(uint32_t i=0; i<realEstate; ++i) {
    if(i & 1) {
      buf[(width * (POSITION_MARKER_SIZE + i)) + 6] = 1;
    } else {
      buf[(width * (POSITION_MARKER_SIZE + i)) + 6] = ZERO_SET;
    }
  }
  buf[(4 * version + 9) * width + 8] = 1; /* dark module */
}

void drawMarker(uint8_t *buf, uint32_t width) {
  memset(buf, 1, sizeof(uint8_t) * POSITION_MARKER_SIZE);
  buf[width * 1 + 0] = 1;
  memset(&buf[width * 1 + 1], ZERO_SET, sizeof(uint8_t) * 5);
  buf[width * 1 + 6] = 1;
  for(uint32_t i=0; i<3; ++i) {
    buf[(width * (2 + i)) + 0] = 1;
    buf[(width * (2 + i)) + 1] = ZERO_SET;
    memset(&buf[(width * (2 + i)) + 2], 1, sizeof(uint8_t) * 3);
    buf[(width * (2 + i)) + 5] = ZERO_SET;
    buf[(width * (2 + i)) + 6] = 1;
  }
  buf[width * 5 + 0] = 1;
  memset(&buf[width * 5 + 1], ZERO_SET, sizeof(uint8_t) * 5);
  buf[width * 5 + 6] = 1;
  memset(&buf[width * 6], 1, sizeof(uint8_t) * POSITION_MARKER_SIZE);
}

void setPositionMarker(uint8_t *buf, uint32_t width) {
  drawMarker(buf, width);
  drawMarker(&buf[width-POSITION_MARKER_SIZE], width);
  drawMarker(&buf[(width-POSITION_MARKER_SIZE) * width], width);
}

static void setSeparators(uint8_t *buf, uint32_t width) {
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

static inline uint8_t convertCharToAlphanumeric(const char character) {
    uint8_t res = 0;
    switch(character) {
      case '0':
        res = 0;
        break;
      case '1':
        res = 1;
        break;
      case 'D':
        res = 13;
        break;
      case 'E':
        res = 14;
        break;
      case 'H':
        res = 17;
        break;
      case 'L':
        res = 21;
        break;
      case 'O':
        res = 24;
        break;
      case 'R':
        res = 27;
        break;
      case 'W':
        res = 32;
        break;
      case ' ':
        res = 36;
        break;
      default:
        printf("Invalid character %c\n", character);
        break;
    }
    return res;
}

/* encode by pairs */
static uint32_t encodeMessageAlphanumeric(const char *string, const uint32_t length, uint8_t *encoded) {
  uint32_t i = 0;
  uint32_t index = 0;
  for(i = 0; i < length-1; i+=2) {
    uint8_t char1 = convertCharToAlphanumeric(string[i]);
    uint8_t char2 = convertCharToAlphanumeric(string[i+1]);
    uint16_t charpair = char1 * 45 + char2; /* 45 is the maximum char */
    for(uint32_t ind = 0; ind < 11; ++ind) {
      encoded[index++] = charpair & (1 << ind) ? 1 : ZERO_SET;
    }
  }
  if(length - index) { /* length % 2 != 0 */
    uint8_t char1 = convertCharToAlphanumeric(string[i]);
    for(uint32_t ind = 0; ind < 6; ++ind) {
      encoded[index++] = char1 & (1 << ind) ? 1 : ZERO_SET;
    }
  }

  return index;
}

void encodeMessage(const char *string, const uint32_t length, const ENCODING encoding, const uint32_t max_len, uint8_t *encoded) {
  uint32_t bit_count = 0;
  encoded[0] = encoding & 1 ? 1 : ZERO_SET;
  encoded[1] = encoding & 2 ? 1 : ZERO_SET;
  encoded[2] = encoding & 4 ? 1 : ZERO_SET;
  encoded[3] = encoding & 8 ? 1 : ZERO_SET;
  bit_count = 4;

  switch(encoding) {
    case ENCODING_NUMERIC:
      encoded[ENCODING_LEN + 9] = length & (1 << 9) ? 1 : ZERO_SET;
      bit_count++;
    case ENCODING_ALPHANUMERIC:
      encoded[ENCODING_LEN + 8] = length & (1 << 8) ? 1 : ZERO_SET;
      bit_count++;
    case ENCODING_BYTE:
    case ENCODING_KANJI:
      encoded[ENCODING_LEN + 7] = length & (1 << 7) ? 1 : ZERO_SET;
      encoded[ENCODING_LEN + 6] = length & (1 << 6) ? 1 : ZERO_SET;
      encoded[ENCODING_LEN + 5] = length & (1 << 5) ? 1 : ZERO_SET;
      encoded[ENCODING_LEN + 4] = length & (1 << 4) ? 1 : ZERO_SET;
      encoded[ENCODING_LEN + 3] = length & (1 << 3) ? 1 : ZERO_SET;
      encoded[ENCODING_LEN + 2] = length & (1 << 2) ? 1 : ZERO_SET;
      encoded[ENCODING_LEN + 1] = length & (1 << 1) ? 1 : ZERO_SET;
      encoded[ENCODING_LEN + 0] = length & (1 << 0) ? 1 : ZERO_SET;
      bit_count += 8;
  }

  switch(encoding) {
    case ENCODING_NUMERIC:
      break;
    case ENCODING_ALPHANUMERIC:
      bit_count += encodeMessageAlphanumeric(string, length, &encoded[ENCODING_LEN + 8 + 1]);
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
    encoded[bit_count++] = ZERO_SET;
  }

  printf("bit count after terminator : %d\n", bit_count);

  /* add zeroes to make it a multiple of 8 */
  for(uint32_t i = bit_count % 8; i < 8; ++i) {
    encoded[bit_count++] = ZERO_SET;
  }

  printf("bit count after 8 rounding : %d\n", bit_count);

  /* pad the remaining codewords */
  uint32_t remaining_bytes = (max_len - bit_count) / 8;
  if(remaining_bytes != 0) {
    for(uint32_t needed_pads = remaining_bytes; needed_pads > 0; --needed_pads) {
      if((needed_pads % 2)) {
        for(uint32_t i=0; i<8; i++) {
          encoded[bit_count++] = PADDING_PATTERN_1 & (1<<i) ? 1 : ZERO_SET;
        }
      } else {
        for(uint32_t i=0; i<8; i++) {
          encoded[bit_count++] = PADDING_PATTERN_2 & (1<<i) ? 1 : ZERO_SET;
        }
      }
    }
  }
  printf("bit count after padding : %d\n", bit_count);
}

static void drawData(uint8_t *buf, const uint8_t *message, const uint32_t width) {
  uint32_t index = 0;
  uint32_t x = 0;
  for(uint32_t x = 0; x < width - 1; x+=2) {
    if(x == (width - POSITION_MARKER_SIZE)) {
      /* skip timing */
      x++;
    }

    uint32_t startPoint = 0;
    if(x % 4) {
      startPoint = width - x - 1;
      for(uint32_t y = 0; y < width; y++) {
        for(uint32_t xind = 0; xind < 2; xind++) {
          if(buf[startPoint + (y*width) - xind] == 0) {
            buf[startPoint + (y*width) - xind] = message[index];
            index++;
          }
        }
      }
    } else {
      startPoint = (width * width) - x - 1;
      for(uint32_t y = 0; y < width; y++) {
        for(uint32_t xind = 0; xind < 2; xind++) {
          if(buf[startPoint - (y*width) - xind] == 0) {
            buf[startPoint - (y*width) - xind] = message[index];
            index++;
          }
        }
      }
    }
  }
}

int main() {
  printf("Qrcode\n");
  setPositionMarker(qrbuffer, 21);
  setSeparators(qrbuffer, 21);
  drawTiming(qrbuffer, 21, VERSION_1);

  uint8_t format[FORMAT_LENGTH] = {0};
  generateFormat(format, EC_LEVEL_Q, MASK_HOR_INTERLEAVE);
  drawFormat(qrbuffer, format, 21);

  /*
   * should pack into a single byte but ... not for now
   * right now, a single output bit is stored into one byte
   * */
  uint8_t message[1024] = {0};
  encodeMessage("HELLO WORLD", 11, ENCODING_ALPHANUMERIC, V1_Q_CODEWORD_COUNT * 8, message);

  drawData(qrbuffer, message, 21);

  saveAsTextPbm("image.ppm", qrbuffer, 21, 21, RESIZE_FACTOR);
  return 0;
}
