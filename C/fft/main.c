#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>

#include "revert_bits.h"

#define DELTA 1e-6
#define PI 3.141592
#define OMEGA_MATRIX_SIZE 8

#define PRINT(a) printf("[%d] : %f+%fi\n", i, omega_matrix[i].real, omega_matrix[i].complex);

typedef struct Number_ {
  float real;
  float complex;
} Number;

Number* generate_omega_matrix(const uint32_t matrix_size) {
  Number *omega_matrix = (Number*)malloc(sizeof(Number) * matrix_size * matrix_size);

  float w = -2 * PI / (float)matrix_size;
  for(uint32_t j=0; j < matrix_size; ++j) {
    for(uint32_t k=0; k < matrix_size; ++k) {
      omega_matrix[j*matrix_size + k].real = cos(w * j * k);
      omega_matrix[j*matrix_size + k].complex = sin(w * j * k);
    }
  }

  return omega_matrix;
}

/* mallocs the returned array */
float* generate_signal_from_list_of_freq(const float *freq_list, const uint32_t freq_count, const float from, const float to, const float delta) {
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

void multiply_add_omega_matrix_with_vector(const Number *omega_matrix, const uint32_t omega_matrix_size, Number *vector, const uint32_t vector_size) {
  Number res[OMEGA_MATRIX_SIZE];
  for(uint32_t i = 0; i < vector_size; ++i) {
    res[i].real = 0.f;
    res[i].complex = 0.f;
    for(uint32_t j = 0; j < vector_size; ++j) {
      //printf("%f * %f = %f\n", vector[i].real, omega_matrix[i*vector_size + j].real, res[i].real);
      res[i].real += vector[j].real * omega_matrix[i*vector_size + j].real;
      res[i].complex += vector[j].real * omega_matrix[i*vector_size + j].complex;
    }
  }
  for(uint32_t i = 0; i < vector_size; ++i) {
    vector[i] = res[i];
  }
}

void rearrange_data_for_fft_mem(const Number *in, const uint32_t count, Number *out) {
  uint32_t omega_size_log2 = (uint32_t)log2(OMEGA_MATRIX_SIZE);
  uint32_t data_size_log2  = (uint32_t)log2(count);

  uint32_t iteration_count = data_size_log2 - omega_size_log2;
  uint32_t increment = (1 << (iteration_count));

  for(uint32_t i = 0; i < count; ++i) {
    uint32_t in_index = revert_bits(i, data_size_log2);
    out[i] = in[in_index];
    for(uint32_t ii = 0; ii < (OMEGA_MATRIX_SIZE - 1); ++ii) {
      in_index += increment;
      i++;
      out[i] = in[in_index];
    }
  }
}


#if 0
Number* naive_fft(const Number *samples, const uint32_t samples_count, const Number *omega_matrix, const uint32_t omega_matrix_size) {
  if(samples_count <= omega_matrix_size) {
    return multiply_add_omega_matrix_with_vector(samples, samples_count, omega_matrix, omega_matrix_size);
  }
}
#endif

//#define V 64
//#define V 65536
//#define V 262144
//#define V 2097152
#define V 4194304 //2^22

int main() {
  /* init */
  Number *omega_matrix = generate_omega_matrix(OMEGA_MATRIX_SIZE);

  Number *a=malloc(sizeof(Number) * V);
  Number *b=malloc(sizeof(Number) * V);
  for(int i=0; i<V; ++i) {
    a[i].real = i;
    a[i].complex = 0;
  }

  rearrange_data_for_fft_mem(a, V, b);

  for(int i=0; i < (V/OMEGA_MATRIX_SIZE); ++i) {
    uint32_t offset = OMEGA_MATRIX_SIZE * i;
    multiply_add_omega_matrix_with_vector(omega_matrix, OMEGA_MATRIX_SIZE, &b[offset], OMEGA_MATRIX_SIZE);
  }

  uint32_t omega_size_log2 = (uint32_t)log2(OMEGA_MATRIX_SIZE);
  uint32_t data_size_log2  = (uint32_t)log2(V);

  uint32_t iteration_count = data_size_log2 - omega_size_log2;
  uint32_t half_N = OMEGA_MATRIX_SIZE;

  Number *tmp = a;
  Number *vals = b;

  for(uint32_t i = 0; i < iteration_count; ++i) {
    float w = (-2. * PI) / (float)(half_N*2.);
    for(uint32_t y = 0; y < (V / half_N / 2); ++y) {
      Number *even = &vals[(y*2)*half_N];
      Number *odd  = &vals[((y*2)+1)*half_N];

      for(uint32_t half_idx = 0; half_idx < half_N; ++half_idx) {
        tmp[(y*2)*half_N+half_idx].real = even[half_idx].real + odd[half_idx].real * cos(w*half_idx) - odd[half_idx].complex * sin(w*half_idx);
        tmp[(y*2)*half_N+half_idx].complex = even[half_idx].complex + odd[half_idx].complex * cos(w*half_idx) + odd[half_idx].real * sin(w*half_idx);
        tmp[(y*2+1)*half_N+half_idx].real = even[half_idx].real + odd[half_idx].real * -cos(w*half_idx) - odd[half_idx].complex * -sin(w*half_idx);
        tmp[(y*2+1)*half_N+half_idx].complex = even[half_idx].complex + odd[half_idx].complex * -cos(w*half_idx) + odd[half_idx].real * -sin(w*half_idx);
      }
    }
    Number *a = tmp;
    tmp = vals;
    vals = a;

    half_N *= 2;
  }

  free(a);
  free(b);
  free(omega_matrix);

  return;

  //float freq_list[5] = {50.f, 120.f, 192.f, 1200.f, 4000.f};

  //float *sample_list = generate_signal_from_list_of_freq(freq_list, 5, 0, 1, DELTA);

  //naive_fft(sample_list, sample_count, omega_matrix, OMEGA_MATRIX_SIZE);

  //printf("%f\n", sample_list[1]);

  //free(sample_list);

  return 0;
}
