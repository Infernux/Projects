#ifndef GALOIS_HELPER_H__
#define GALOIS_HELPER_H__

#include <inttypes.h>

extern uint8_t gf256[256];
extern uint8_t gf256_antilog[256];

void initialize_gf256(uint16_t modulo);

#endif /* GALOIS_HELPER_H__ */
