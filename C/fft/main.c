#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>

#define DELTA 1e-6
#define PI 3.141596

/* mallocs the returned array */
float* generate_signal_from_list_of_freq(float *freq_list, uint32_t freq_count, float from, float to, float delta) {
  if(from > to) {
    printf("From is bigger than to\n");
    return NULL;
  }
  if(freq_count == 0) {
    printf("Frequency count is 0\n");
    return NULL;
  }

  float diff = to - from;
  float t = 0.f;
  uint32_t count = (uint32_t)(diff / delta);

  float *out = (float*)malloc(sizeof(float) * count);
  printf("count %d\n", count);
  for(uint32_t i = 0; i < count; ++i) {
    float acc = 0.f;
    for(uint32_t freq_idx = 0; freq_idx < freq_count; ++freq_idx) {
      acc += sin(2*PI*freq_list[freq_idx]*t);
    }
    out[i] = acc;
    t += delta;
  }

  return out;
}

int main() {
  printf("Test\n");

  float freq_list[5] = {50.f, 120.f, 192.f, 1200.f, 4000.f};

  float *sample_list = generate_signal_from_list_of_freq(freq_list, 5, 0, 1, DELTA);

  printf("%f\n", sample_list[1]);

  free(sample_list);

  return 0;
}
