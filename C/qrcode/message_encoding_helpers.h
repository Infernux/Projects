#ifndef MESSAGE_ENCODING_HELPERS__
#define MESSAGE_ENCODING_HELPERS__

#include <inttypes.h>

#define KANJI_CONSTANT_1 0x8140
#define KANJI_CONSTANT_2 0xC140

uint32_t encodeMessageAlphanumeric(const char *string, const uint32_t length, uint8_t *encoded);
uint32_t encodeMessageNumeric(const char *string, const uint32_t length, uint8_t *encoded);
uint32_t encodeMessageKanji(const char *string, const uint32_t length, uint8_t *encoded);
uint32_t encodeMessageByte(const char *string, const uint32_t length, uint8_t *encoded);

#endif /* MESSAGE_ENCODING_HELPERS__ */
