#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include <cuda_runtime.h>

#include "kernel.cuh"

#define N 10

void randomizeFloatArray(float *arr, const uint32_t arr_size, const uint32_t seed)
{
  srand(seed);
  for(uint32_t i = 0; i < arr_size; ++i)
  {
    arr[i] = rand();
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
  float a[N], b[N], c[N];
  float *c_in_a, *c_in_b, *c_out_c;

  randomizeFloatArray(a, N, 42);
  randomizeFloatArray(b, N, 43);

  printFloatArray(a, N);
  printFloatArray(b, N);

  cudaMalloc((void **) &c_in_a, N * sizeof(float));
  cudaMalloc((void **) &c_in_b, N * sizeof(float));
  cudaMalloc((void **) &c_out_c, N * sizeof(float));

  cudaMemcpy(c_in_a, a, N * sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(c_in_b, b, N * sizeof(float), cudaMemcpyHostToDevice);

  kadd<<<1, N>>>(c_in_a,c_in_b,c_out_c);

  cudaMemcpy(c, c_out_c, N * sizeof(float), cudaMemcpyDeviceToHost);

  printFloatArray(c, N);

  cudaFree(c_in_a);
  cudaFree(c_in_b);
  cudaFree(c_out_c);
}
