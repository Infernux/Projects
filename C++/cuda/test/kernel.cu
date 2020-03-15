__global__ void kadd(float *a, float *b, float *c, const unsigned int el_per_thread)
{
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  unsigned int offset = i * el_per_thread;

  for(unsigned int idx = 0; idx < el_per_thread; idx++) {
    c[offset+idx] = a[offset+idx] + b[offset+idx];
  }
}
