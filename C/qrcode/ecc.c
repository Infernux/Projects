#include "ecc.h"

#include <stdio.h>
#include <string.h>

#include "galois_helper.h"

#define max(a,b) (a>b?a:b)
#define MAX_POL_SIZE 68

static uint8_t message_polynome[256];
static uint8_t generator_polynome[MAX_POL_SIZE];
static uint8_t division_generator_polynome[MAX_POL_SIZE];
static uint8_t tmp_generator_polynome[MAX_POL_SIZE];
//static uint8_t tmp_generator_polynome2[MAX_POL_SIZE];
static int16_t tmp_generator_polynome2[MAX_POL_SIZE];

#define print_polynome(pol, size) \
{ \
  for(int i=0; i<size; ++i) { \
    printf("%dx^%d + ", pol[i], size-1-i); \
  } \
  printf("\n"); \
}

#define pp(m) \
{ \
  for(uint32_t j=0; j<8; ++j) { \
    printf("%d", m[j]); \
  } \
  printf("\n"); \
}

static void generateMessagePolynome(const uint8_t *message, const uint32_t length, uint8_t *polynome) {
  uint8_t curr;
  for(uint32_t i=0; i<length; ++i) {
    polynome[i] = message[0] << 7 |
      message[1] << 6 |
      message[2] << 5 |
      message[3] << 4 |
      message[4] << 3 |
      message[5] << 2 |
      message[6] << 1 |
      message[7] << 0
      ;

    message += 8;
  }
}

static void convertPolynome_antialpha(uint8_t *polynome, const uint32_t length) {
  for(uint32_t i1 = 0; i1 < length; ++i1) {
    polynome[i1] = gf256[polynome[i1]];
  }
}

static void convertPolynome_alpha(uint8_t *polynome, const uint32_t length) {
  for(uint32_t i1 = 0; i1 < length; ++i1) {
    polynome[i1] = gf256_antilog[polynome[i1]];
  }
}

static void multiplyPolynomes(const uint8_t *polynome1, const uint32_t poly1_len, const uint8_t *polynome2, const uint32_t poly2_len) {
  for(uint32_t i = 0; i<MAX_POL_SIZE; ++i) {
    tmp_generator_polynome2[i] = -1;
  }

  for(uint32_t i1 = 0; i1 < poly1_len; ++i1) {
    for(uint32_t i2 = 0; i2 < poly2_len; ++i2) {
      /* addition in gf256 is done via XOR */
      uint16_t cur_val = polynome1[i1] + polynome2[i2];
      cur_val %= 255;
      uint8_t cur_val_anti = gf256[cur_val];
      if(tmp_generator_polynome2[i1+i2] != -1) {
        uint8_t pol_anti = gf256[tmp_generator_polynome2[i1+i2]];
        tmp_generator_polynome2[i1+i2] = gf256_antilog[cur_val_anti ^ pol_anti];
      } else {
        tmp_generator_polynome2[i1+i2] = cur_val;
      }
    }
  }
}

/*
 * TODO: find a way to multiply 2 random sized polynomes while having
 * the highest exponent being index 0
 * */
static void computeGeneratorPolynome(const uint32_t ecc_codeword_count, uint8_t *polynome) {
  polynome[0] = 0; /* alpha 0 */
  polynome[1] = 0; /* alpha 0 */
  uint32_t len1 = 2;

  for(uint32_t i=1; i<ecc_codeword_count; ++i) {
    tmp_generator_polynome[0] = i; /* alpha 0 */
    tmp_generator_polynome[1] = 0; /* alpha 1 */
    uint32_t len2 = 2;
    multiplyPolynomes(polynome, len1, tmp_generator_polynome, len2);
    len1 = len1 + 1;
    for(uint32_t copy_idx = 0; copy_idx < len1; copy_idx++) {
      polynome[copy_idx] = tmp_generator_polynome2[copy_idx];
    }
  }
  /* unoptimized */
  for(uint32_t copy_idx = 0; copy_idx < len1; copy_idx++) {
    polynome[len1-1-copy_idx] = tmp_generator_polynome2[copy_idx];
  }
  memset(&polynome[len1], 0, 20);
}

void computeECC_words(uint8_t *message_polynome, const uint32_t data_codeword_count, uint8_t *generator_polynome, const uint32_t ecc_codeword_count, uint8_t *ecc_output) {
  /* need to raise the message's polynome by the power of the ecc_codeword_count */
  uint32_t message_len = data_codeword_count + ecc_codeword_count;
  /* need to raise the message's polynome by the power of the ecc_codeword_count */
  print_polynome(message_polynome, message_len);
  print_polynome(generator_polynome, message_len); /* goes from x^ecc_codeword_count to x^0 */
  printf("-----\n");
  for(uint32_t i=0; i<data_codeword_count; ++i) {
    uint8_t factor = gf256_antilog[message_polynome[i==0?0:1]]; /* highest factor */
    printf("factor %d\n", factor);
    for(uint32_t j=0; j<=ecc_codeword_count; j++) {
      uint16_t tmp = generator_polynome[j] + factor;
      tmp %= 255;
      division_generator_polynome[j] = tmp;
    }
    convertPolynome_antialpha(division_generator_polynome, ecc_codeword_count+1);
    print_polynome(division_generator_polynome, message_len);
    printf("-----\n");
    for(uint32_t j=0; j<data_codeword_count; j++) {
      message_polynome[j] = division_generator_polynome[j] ^ message_polynome[j+(i==0?0:1)];
    }
    print_polynome(message_polynome, message_len);
    message_len--;
  }

  uint32_t index = 0;
  for(uint32_t i = 0; i < ecc_codeword_count; i++) {
    for(int32_t ind = 7; ind >= 0; --ind) {
      ecc_output[index++] = message_polynome[i] & (1 << ind) ? 1 : 0;
    }
  }
}

void computeECC(const uint8_t *message, const uint32_t data_codeword_count, const uint32_t ecc_codeword_count, uint8_t *ecc_output) {
  generateMessagePolynome(message, data_codeword_count, message_polynome);
  computeGeneratorPolynome(ecc_codeword_count, generator_polynome);
  computeECC_words(message_polynome, data_codeword_count, generator_polynome, ecc_codeword_count, ecc_output);
}
