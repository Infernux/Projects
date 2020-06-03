#ifndef TLV_H__
#define TLV_H__

#include <inttypes.h>

typedef struct TLV_ {
  uint32_t type;
  uint32_t length;
  char *value;
} TLV;

#endif /* TLV_H__ */
