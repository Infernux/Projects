#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <math.h>

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

Number* multiply_add_omega_matrix_with_vector(const Number *omega_matrix, const uint32_t omega_matrix_size, const float *vector, const uint32_t vector_size) {
  Number *res = (Number*)malloc(sizeof(Number) * vector_size);
  for(uint32_t i = 0; i < vector_size; ++i) {
    res[i].real = 0.f;
    res[i].complex = 0.f;
    for(uint32_t j = 0; j < vector_size; ++j) {
      printf("%f * %f = %f\n", vector[i], omega_matrix[i*vector_size + j].real, res[i].real);
      res[i].real += vector[j] * omega_matrix[i*vector_size + j].real;
      res[i].complex += vector[j] * omega_matrix[i*vector_size + j].complex;
    }
  }

  return res;
}

#if 0
Number* naive_fft(const Number *samples, const uint32_t samples_count, const Number *omega_matrix, const uint32_t omega_matrix_size) {
  if(samples_count <= omega_matrix_size) {
    return multiply_add_omega_matrix_with_vector(samples, samples_count, omega_matrix, omega_matrix_size);
  }
}
#endif

int main() {
  printf("Test\n");

  float vector[] = {1,2,3,4,5,6,7,8};

  /* init */
  Number *omega_matrix = generate_omega_matrix(OMEGA_MATRIX_SIZE);
  /* init */
  Number *res = multiply_add_omega_matrix_with_vector(omega_matrix, OMEGA_MATRIX_SIZE, vector, OMEGA_MATRIX_SIZE);

  //float freq_list[5] = {50.f, 120.f, 192.f, 1200.f, 4000.f};

  //float *sample_list = generate_signal_from_list_of_freq(freq_list, 5, 0, 1, DELTA);

  //naive_fft(sample_list, sample_count, omega_matrix, OMEGA_MATRIX_SIZE);

  //printf("%f\n", sample_list[1]);

  //free(sample_list);
  free(omega_matrix);

  return 0;
}
