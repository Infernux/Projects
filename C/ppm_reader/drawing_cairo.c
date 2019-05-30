#include "drawing_cairo.h"

void square(cairo_t *cr, const uint16_t x, const uint16_t y)
{
  uint16_t real_x = SIZE * x;
  uint16_t real_y = SIZE * y;
    cairo_move_to(cr, real_x, real_y);
    cairo_rel_line_to(cr,  2*SIZE,   0);
    cairo_rel_line_to(cr,   0,  2*SIZE);
    cairo_rel_line_to(cr, -2*SIZE,   0);
    cairo_close_path(cr);
    cairo_stroke (cr);
}
