#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "bit_debug.h"
#include "ecc.h"
#include "galois_helper.h"
#include "image_dump_tools.h"
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

void generateFormat(uint8_t *info, EC_LEVEL ec_level, MASK_TYPE mask_type) {
  uint16_t format = generateErrorCorrectionBits(ERROR_CORRECTION_MASK_BITS_L, mask_type);
  for(uint32_t i=0; i<15; i++) {
    info[i] = (format & 1<<((FORMAT_LENGTH-1)-i)) ? ONE_SET : ZERO_SET;
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
      buf[(width * 6) + (POSITION_MARKER_SIZE + i)] = ONE_SET;
    } else {
      buf[(width * 6) + (POSITION_MARKER_SIZE + i)] = ZERO_SET;
    }
  }
  for(uint32_t i=0; i<realEstate; ++i) {
    if(i & 1) {
      buf[(width * (POSITION_MARKER_SIZE + i)) + 6] = ONE_SET;
    } else {
      buf[(width * (POSITION_MARKER_SIZE + i)) + 6] = ZERO_SET;
    }
  }
  buf[(4 * version + 9) * width + 8] = ONE_SET; /* dark module */
}

void drawMarker(uint8_t *buf, uint32_t width) {
  memset(buf, ONE_SET, sizeof(uint8_t) * POSITION_MARKER_SIZE);
  buf[width * 1 + 0] = ONE_SET;
  memset(&buf[width * 1 + 1], ZERO_SET, sizeof(uint8_t) * 5);
  buf[width * 1 + 6] = ONE_SET;
  for(uint32_t i=0; i<3; ++i) {
    buf[(width * (2 + i)) + 0] = ONE_SET;
    buf[(width * (2 + i)) + 1] = ZERO_SET;
    memset(&buf[(width * (2 + i)) + 2], ONE_SET, sizeof(uint8_t) * 3);
    buf[(width * (2 + i)) + 5] = ZERO_SET;
    buf[(width * (2 + i)) + 6] = ONE_SET;
  }
  buf[width * 5 + 0] = ONE_SET;
  memset(&buf[width * 5 + 1], ZERO_SET, sizeof(uint8_t) * 5);
  buf[width * 5 + 6] = ONE_SET;
  memset(&buf[width * 6], ONE_SET, sizeof(uint8_t) * POSITION_MARKER_SIZE);
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
      case '2':
        res = 2;
        break;
      case '3':
        res = 3;
        break;
      case 'A':
        res = 10;
        break;
      case 'B':
        res = 11;
        break;
      case 'C':
        res = 12;
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
    for(int32_t ind = 10; ind >= 0; --ind) {
      encoded[index++] = charpair & (1 << ind) ? 1 : 0;
    }
  }
  if(length - index) { /* length % 2 != 0 */
    uint8_t char1 = convertCharToAlphanumeric(string[i]);
    for(int32_t ind = 5; ind >= 0; --ind) {
      encoded[index++] = char1 & (1 << ind) ? 1 : 0;
    }
  }

  return index;
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
  for(uint32_t i = bit_count % 8; i < 8; ++i) {
    encoded[bit_count++] = 0;
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
  generateFormat(format, EC_LEVEL_MED, MASK_HOR_INTERLEAVE);
  drawFormat(qrbuffer, format, 21);

  initialize_gf256(QRCODE_ECC_MODULO);

  /*
   * should pack into a single byte but ... not for now
   * right now, a single output bit is stored into one byte
   * */
  uint8_t message[1024] = {0};
  encodeMessage("HELLO WORLD", 11, ENCODING_ALPHANUMERIC, V1_M_CODEWORD_COUNT * 8, message);

  computeECC(message, V1_M_CODEWORD_COUNT, V1_M_EC_COUNT, &message[V1_M_CODEWORD_COUNT * 8]);

  drawData(qrbuffer, message, 21);

  saveAsTextPbm("image.ppm", qrbuffer, 21, 21, RESIZE_FACTOR);
  return 0;
}
