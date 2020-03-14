cmake_minimum_required(VERSION 3.10)

project(cuda_test LANGUAGES CUDA CXX)

#configure_file(version.h.in version.h)

add_executable(main
  main.cu
  kernel.cu
)

set(CXX nvcc)

target_include_directories(main PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          )
