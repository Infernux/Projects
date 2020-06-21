#include "message_encoding_helpers.h"

#include <stdio.h>

static inline uint8_t convertCharToAlphanumeric(const char character) {
    char res = character;

    if(character >= 48 && character <= 57) {
      res -= 48;
    } else if (character >= 65 && character <= 90) {
      res -= 55;
    } else {
      switch(character) {
        case ' ':
          res = 36;
          break;
        case '$':
          res = 37;
          break;
        case '%':
          res = 38;
          break;
        case '*':
          res = 39;
          break;
        case '+':
          res = 40;
          break;
        case '-':
          res = 41;
          break;
        case '.':
          res = 42;
          break;
        case '/':
          res = 43;
          break;
        case ':':
          res = 44;
          break;
        default:
          printf("Invalid character %d (%c)\n", character, character);
          break;
      }
    }

    return res;
}

/* encode by pairs */
uint32_t encodeMessageAlphanumeric(const char *string, const uint32_t length, uint8_t *encoded) {
  uint32_t i = 0;
  uint32_t index = 0;
  for(i = 0; i < length-1; i+=2) {
    uint8_t char1 = convertCharToAlphanumeric(string[i]);
    uint8_t char2 = convertCharToAlphanumeric(string[i+1]);
    uint16_t charpair = char1 * 45 + char2; /* 45 is the maximum char */
    //printf("c1 %c, c2 %c -> %d\n", string[i], string[i+1], charpair);
    for(int32_t ind = 10; ind >= 0; --ind) {
      encoded[index++] = charpair & (1 << ind) ? 1 : 0;
    }
  }
  if(length % 2) { /* rest : length % 2 != 0 */
    uint8_t char1 = convertCharToAlphanumeric(string[i]);
    for(int32_t ind = 5; ind >= 0; --ind) {
      encoded[index++] = char1 & (1 << ind) ? 1 : 0;
    }
  }

  return index;
}
