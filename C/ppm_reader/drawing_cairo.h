#ifndef DRAWING_CAIRO__
#define DRAWING_CAIRO__

#define SIZE 1

#include <cairo/cairo.h>
#include <cairo/cairo-xlib.h>
#include <inttypes.h>

void square(cairo_t *cr, const uint16_t x, const uint16_t y);

#endif /* DRAWING_CAIRO__ */
