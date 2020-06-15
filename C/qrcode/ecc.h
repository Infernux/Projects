#ifndef ECC_H__
#define ECC_H__

#include <inttypes.h>

#define QRCODE_ECC_MODULO 0x11D /* 100011101 */

/*
 * message: padded message
 * length : byte count
 * ecc_output : pointer to the head of the output buffer, typically the end of message
 * */
void computeECC(const uint8_t *message, const uint32_t data_codeword_count, const uint32_t ecc_codeword_count, uint8_t *ecc_output);

#endif /* ECC_H__ */
