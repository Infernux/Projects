#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include <cuda_runtime.h>

#include "kernel.cuh"

#define N 100000
#define BLOCK_SIZE 256

void compareBuffers(const float *a, const float *b, const uint32_t arr_size)
{
  uint32_t total_failed = 0;
  for(uint32_t i = 0; i < arr_size; ++i)
  {
    if(a[i] != b[i]) {
      printf("Failed index %d\n", i);
      total_failed++;
    }
  }
  printf("failed (%d/%d)\n", total_failed, arr_size);
}

void referenceAdd(const float *a, const float *b, float *c, const uint32_t arr_size)
{
  for(uint32_t i = 0; i < arr_size; ++i)
  {
    c[i] = a[i] + b[i];
  }
}

void randomizeFloatArray(float *arr, const uint32_t arr_size, const uint32_t seed)
{
  srand(seed);
  for(uint32_t i = 0; i < arr_size; ++i)
  {
    arr[i] = rand();
  }
}

void initSimpleFloatArray(float *arr, const uint32_t arr_size, const uint32_t offset)
{
  for(uint32_t i = 0; i < arr_size; ++i)
  {
    arr[i] = i + offset;
  }
}

void printFloatArray(float *arr, const uint32_t arr_size)
{
  for(uint32_t i = 0; i < arr_size; ++i)
  {
    printf("%f, ", arr[i]);
  }
  printf("\n");
}

int main()
{
  float *a, *b, *c, *ref_c;
  float *c_in_a, *c_in_b, *c_out_c;

  a = (float*)malloc(sizeof(float) * N);
  b = (float*)malloc(sizeof(float) * N);
  c = (float*)malloc(sizeof(float) * N);
  ref_c = (float*)malloc(sizeof(float) * N);

  initSimpleFloatArray(a, N, 0);
  initSimpleFloatArray(b, N, 43);

  //printFloatArray(a, N);
  //printFloatArray(b, N);

  cudaMalloc((void **) &c_in_a, N * sizeof(float));
  cudaMalloc((void **) &c_in_b, N * sizeof(float));
  cudaMalloc((void **) &c_out_c, N * sizeof(float));

  cudaMemcpy(c_in_a, a, N * sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(c_in_b, b, N * sizeof(float), cudaMemcpyHostToDevice);

  //const uint32_t el_per_thread = (uint32_t)ceil((double)N / (double)BLOCK_SIZE);
  const uint32_t el_per_thread = 1;
  const uint32_t block_count = (uint32_t)ceil(((double)N / el_per_thread) / (double)BLOCK_SIZE);

  printf("el per thread : %d, block_count : %d\n", el_per_thread, block_count);

  kadd<<<block_count, BLOCK_SIZE>>>(c_in_a, c_in_b, c_out_c, el_per_thread);

  cudaMemcpy(c, c_out_c, N * sizeof(float), cudaMemcpyDeviceToHost);

  //printFloatArray(c, N);

  cudaFree(c_in_a);
  cudaFree(c_in_b);
  cudaFree(c_out_c);

  referenceAdd(a, b, ref_c, N);
  compareBuffers(ref_c, c, N);

  free(a);
  free(b);
  free(c);
  free(ref_c);
}
