#include <stdlib.h>
#include <stdio.h>

#include <cairo/cairo.h>
#include <cairo/cairo-xlib.h>

#include <inttypes.h>

int read_int(FILE *f)
{
  char reader;
  char buf[50];
  int current_index = 0;

  if(feof(f))
    return -1;

  while(fread(&reader, sizeof(char), 1, f))
  {
    if(current_index > 49)
    {
      return -1;
    }

    if(reader == ' ' || reader == '\n' || reader == '\r')
    {
      if(current_index != 0)
      {
        buf[current_index] = '\0';
        break;
      }
    }

    buf[current_index] = reader;
    current_index++;
  }

  return atoi(buf);
}

typedef struct win {
    Display *dpy;
    int scr;

    Window win;
    GC gc;

    int width, height;
    KeyCode quit_code;
} win_t;

#define SIZE 1

static void
square(cairo_t *cr, const uint16_t x, const uint16_t y)
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

static void
win_draw(win_t *win, FILE *f, int width, int height)
{
  cairo_surface_t *surface;
  cairo_t *cr;
  Visual *visual = DefaultVisual(win->dpy, DefaultScreen (win->dpy));

  XClearWindow(win->dpy, win->win);

  surface = cairo_xlib_surface_create (win->dpy, win->win, visual,
      win->width, win->height);
  cr = cairo_create(surface);

  int x=0, y=0;

  int16_t r, g, b;
  while(1)
  {
    r = read_int(f);
    g = read_int(f);
    b = read_int(f);

    if(r==-1)
      break;

    cairo_set_source_rgb(cr, r/255., g/255., b/255.);
    square(cr, x, y);
    x=(++x)%width;
    if(x==0)
    {
      y++;
    }
  }

  cairo_destroy(cr);
  cairo_surface_destroy (surface);
}

static void
win_init(win_t *win)
{
    Window root;

    win->width = 400;
    win->height = 400;

    root = DefaultRootWindow(win->dpy);
    win->scr = DefaultScreen(win->dpy);

    win->win = XCreateSimpleWindow(win->dpy, root, 0, 0,
        win->width, win->height, 0,
        BlackPixel(win->dpy, win->scr), BlackPixel(win->dpy, win->scr));

    win->quit_code = XKeysymToKeycode(win->dpy, XStringToKeysym("Q"));

    XSelectInput(win->dpy, win->win,
		KeyPressMask
		|StructureNotifyMask
		|ExposureMask);

    XMapWindow(win->dpy, win->win);
}

static void
win_deinit(win_t *win)
{
    XDestroyWindow(win->dpy, win->win);
}

static void
win_handle_events(win_t *win)
{
    XEvent xev;

    while (1) {
	XNextEvent(win->dpy, &xev);
	switch(xev.type) {
	case KeyPress:
	{
      XKeyEvent *kev = &xev.xkey;

      if (kev->keycode == win->quit_code) {
  	    return;
	    }
	}
	break;
	case ConfigureNotify:
	{
	    XConfigureEvent *cev = &xev.xconfigure;

	    win->width = cev->width;
	    win->height = cev->height;
	}
	break;
	case Expose:
	{
	    XExposeEvent *eev = &xev.xexpose;

	    /*if (eev->count == 0)
		    win_draw(win);*/
	}
	break;
	}
    }
}





int main(int argc, char **argv)
{
  //FILE *output = fopen("output.ppm", "w");
  FILE *f = fopen(argv[1], "r");

  char bufskip[50];
  fgets(bufskip, 50, f);

  int width = read_int(f);
  int height = read_int(f);
  int max = read_int(f);

  printf("height : %d, width : %d\n", height, width);

  /*fprintf(output, "P3\n%d %d\n255\n", width, height);
  int i;
  for(i=0; i<width * height; ++i)
  {
    unsigned char r = read_int(f);
    unsigned char g = read_int(f);
    unsigned char b = read_int(f);

    fprintf(output, " %03d %03d %03d ", r, g, b);
  }*/

  win_t win;

  win.dpy = XOpenDisplay(0);

  if (win.dpy == NULL) {
    fprintf(stderr, "Failed to open display\n");
    return 1;
  }

  win_init(&win);

  win_draw(&win, f, width, height);

  win_handle_events(&win);

  win_deinit(&win);

  XCloseDisplay(win.dpy);

  fclose(f);
  //fclose(output);

  return 0;
}
