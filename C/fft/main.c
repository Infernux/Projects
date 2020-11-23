#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>

#include "measure_tools.h"
#include "revert_bits.h"

#define DELTA 1e-6
#define PI 3.141592
#define OMEGA_MATRIX_SIZE 8

#define PRINT(a) printf("[%d] : %f+%fi\n", i, a.real, a.complex);

typedef struct Number_ {
  double real;
  double complex;
} Number;

Number* generate_omega_matrix(const uint32_t matrix_size) {
  Number *omega_matrix = (Number*)malloc(sizeof(Number) * matrix_size * matrix_size);

  double w = -2 * PI / (double)matrix_size;
  for(uint32_t j=0; j < matrix_size; ++j) {
    for(uint32_t k=0; k < matrix_size; ++k) {
      omega_matrix[j*matrix_size + k].real = cos(w * j * k);
      omega_matrix[j*matrix_size + k].complex = sin(w * j * k);
    }
  }

  return omega_matrix;
}

/* mallocs the returned array */
Number* generate_signal_from_list_of_freq(const double *freq_list, const uint32_t freq_count, const double from, const double to, const double delta, const uint8_t needs_padding, uint32_t *count, uint32_t *padded_count) {
  if(from > to) {
    printf("From is bigger than to\n");
    return NULL;
  }
  if(freq_count == 0) {
    printf("Frequency count is 0\n");
    return NULL;
  }

  double diff = to - from;
  double t = 0.f;
  *count = (uint32_t)(diff / delta);

  printf("data_count %d\n", *count);
  if(needs_padding) {
    uint32_t floor_size = ((uint32_t)log2(*count));
    *padded_count = 1 << (floor_size+1);
    printf("padding: %d\n", *padded_count);
  } else {
    *padded_count = *count;
  }

  Number *out = (Number*)malloc(sizeof(Number) * *padded_count);

  for(uint32_t i = 0; i < *count; ++i) {
    double acc = 0.f;
    for(uint32_t freq_idx = 0; freq_idx < freq_count; ++freq_idx) {
      acc += sin(2*PI*freq_list[freq_idx]*t);
    }
    out[i].real = acc;
    out[i].complex = 0;
    t += delta;
  }

  printf("ccount : %d\n", *count);

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

Number* naive_fft(Number *samples, const uint32_t samples_count, const Number *omega_matrix, const uint32_t omega_matrix_size, Number *inter_buffer) {
  rearrange_data_for_fft_mem(samples, samples_count, inter_buffer);

  for(int i=0; i < (samples_count/omega_matrix_size); ++i) {
    uint32_t offset = omega_matrix_size * i;
    multiply_add_omega_matrix_with_vector(omega_matrix, omega_matrix_size, &inter_buffer[offset], omega_matrix_size);
  }

  uint32_t omega_size_log2 = (uint32_t)log2(omega_matrix_size);
  uint32_t data_size_log2  = (uint32_t)log2(samples_count);

  uint32_t iteration_count = data_size_log2 - omega_size_log2;
  uint32_t half_N = omega_matrix_size;

  Number *tmp = samples;
  Number *vals = inter_buffer;

  for(uint32_t i = 0; i < iteration_count; ++i) {
    double w = (-2. * PI) / (double)(half_N*2.);
    for(uint32_t y = 0; y < (samples_count / half_N / 2); ++y) {
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

  return vals;
}

#define V 64
//#define V 65536
//#define V 262144
//#define V 2097152
//#define V 4194304 //2^22
//#define V 33554432

int main() {
  /* init */
  Number *omega_matrix = generate_omega_matrix(OMEGA_MATRIX_SIZE);

  double freq_list[5] = {50.f, 120.f, 192.f, 1200.f, 4000.f};

  uint32_t count = 0, padded_count = 0;
  Number *sample_list = generate_signal_from_list_of_freq(freq_list, 5, 0, 1, DELTA, 1, &count, &padded_count);

  Number *b=malloc(sizeof(Number) * padded_count);

  TIME_INIT
  TIME_START
  Number *res = naive_fft(sample_list, padded_count, omega_matrix, OMEGA_MATRIX_SIZE, b);
  TIME_END("fast")

#ifdef DEBUG_OUTPUT
  for(int i = 0; i < count; ++i) {
    PRINT(res[i]);
  }
#endif

  free(sample_list);
  free(omega_matrix);
  free(b);

  return 0;
}
