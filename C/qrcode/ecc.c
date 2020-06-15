#include "ecc.h"

#include <stdio.h>
#include <string.h>

#include "galois_helper.h"

#define max(a,b) (a>b?a:b)

static uint8_t message_polynome[256];
static uint8_t generator_polynome[68];
static uint8_t tmp_generator_polynome[68];
//static uint8_t tmp_generator_polynome2[68];
static int16_t tmp_generator_polynome2[68];

static void generateMessagePolynome(const uint8_t *message, const uint32_t length, uint8_t *polynome) {
  uint8_t curr;
  for(uint32_t i=0; i<length; ++i) {
    polynome[i] = message[i] << 7 |
      message[i+1] << 6 |
      message[i+2] << 5 |
      message[i+3] << 4 |
      message[i+4] << 3 |
      message[i+5] << 2 |
      message[i+6] << 1 |
      message[i+7] << 0
      ;
    printf("%d : %d\n", i, polynome[i]);
    message += 8;
  }
}

static void multiplyPolynomes(const uint8_t *polynome1, const uint32_t poly1_len, const uint8_t *polynome2, const uint32_t poly2_len) {
  for(uint32_t i = 0; i<68; ++i) {
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
  for(int i=max(len1-1, 2); i>=0; --i) {
    printf("%dx^%d + ", polynome[i], i);
  }
  printf("\n");
}

void computeECC(const uint8_t *message, const uint32_t data_codeword_count, const uint32_t ecc_codeword_count, uint8_t *ecc_output) {
  generateMessagePolynome(message, data_codeword_count, message_polynome);
  computeGeneratorPolynome(ecc_codeword_count, generator_polynome);
}
