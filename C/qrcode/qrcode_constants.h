#ifndef QRCODE_CONSTANTS_H__
#define QRCODE_CONSTANTS_H__

#define V1_L_CODEWORD_COUNT 19
#define V1_M_CODEWORD_COUNT 16
#define V1_Q_CODEWORD_COUNT 13
#define V1_H_CODEWORD_COUNT 9
#define V1_L_EC_COUNT 7
#define V1_M_EC_COUNT 10
#define V1_Q_EC_COUNT 13
#define V1_H_EC_COUNT 17

#define V1_ENCODING_LEN_NUMERIC 10
#define V1_ENCODING_LEN_ALPHA   9
#define V1_ENCODING_LEN_BYTE    8
#define V1_ENCODING_LEN_KANJI   8

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
  MASK_1=0, /* (i+j) % 2 == 0 */
  MASK_2, /* j % 2 == 0 */
  MASK_3, /* x % 3 == 0 */
  MASK_4, /* (i+j) % 3 == 0 */
  MASK_HOR_INTERLEAVE, /* (floor(j/2) + floor(i/3) % 2) == 0 */
  MASK_CHECKERBOARD, /* (((i*j) % 2) + ((i*j)%3)) == 0 */
  MASK_DIAGONAL_WAVE, /* (((i*j)%2)+(i*j)%3)%2 == 0*/
  MASK_VERTICAL_INTERLEAVE /* (((i*j)%2)+((i*j)%3))%2 == 0 */
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

#define QR_BASE_SIZE 17
#define POSITION_MARKER_SIZE 7

#endif /* QRCODE_CONSTANTS_H__ */
