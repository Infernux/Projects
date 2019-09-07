#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define WIDTH 300
#define HEIGHT 300

static uint8_t buffer[WIDTH * HEIGHT];

typedef struct {
  uint16_t x;
  uint16_t y;
  uint8_t val;
} Coord;

static void interpolate(uint8_t *u1_buffer, const Coord *c1, const Coord *c2, const Coord *c3, const Coord *c4)
{
  uint8_t avg_val = (uint8_t)(((uint16_t)c1->val + (uint16_t)c2->val + (uint16_t)c3->val + (uint16_t)c4->val) / 4);

  for(uint32_t y = c1->y; y <= c3->y; ++y)
  {
    for(uint32_t x = c1->x; x <= c2->x; ++x)
    {
      u1_buffer[y * WIDTH + x] = avg_val;
    }
  }
}

static void drawCoord(uint8_t *u1_buffer, const Coord *coord)
{
  u1_buffer[coord->y * WIDTH + coord->x] = coord->val;
}

static void writeBufferToFile(const char *filename, const uint8_t *u1_buffer, uint32_t length)
{
  FILE *f = fopen(filename, "w");

  fprintf(f, "P2\n");
  fprintf(f, "%d %d\n", WIDTH, HEIGHT);
  fprintf(f, "255\n");

  for(uint32_t y = 0; y < HEIGHT; ++y)
  {
    for(uint32_t x = 0; x < WIDTH; ++x)
    {
      fprintf(f, "%d ", u1_buffer[(y * WIDTH) + x]);
    }
  }

  fclose(f);
}

int main()
{
  printf("test\n");

  memset(buffer, 0, sizeof(uint8_t) * WIDTH * HEIGHT);

  Coord tl = {20, 20, 255}, tr = {30, 20, 255}, bl = {20, 50, 255}, br = {30, 50, 255};
  drawCoord(buffer, &tl);
  drawCoord(buffer, &tr);
  drawCoord(buffer, &bl);
  drawCoord(buffer, &br);

  interpolate(buffer, &tl, &tr, &bl, &br);

  writeBufferToFile("output.pgm", buffer, WIDTH*HEIGHT);

  return 0;
}
