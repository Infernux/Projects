#ifndef BIT_HACKS_H__
#define BIT_HACKS_H__

#define PACK_8_U1_IN_U8(a,b,c,d,e,f,g,h) ((a)|(b << 8)|(c << 16)|(d << 24)|(e << 32)|(f << 40)|(g << 48)|(h << 56))
#define PACK_4_U1_IN_U4(a,b,c,d) ((a)|(b << 8)|(c << 16)|(d << 24))

#endif
