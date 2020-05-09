cmake_minimum_required(VERSION 3.16)

project(neon_tester)

add_executable(
  neon_tester
  neon_tester.c
)

add_definitions(
  -mfpu=neon
)

add_subdirectory(
  "${CMAKE_SOURCE_DIR}/../tools/bit_debug"
  bit_debug
)

target_link_libraries(
  neon_tester
  PUBLIC
  bit_debug
)

target_include_directories(
  neon_tester
  PUBLIC
  "${CMAKE_SOURCE_DIR}/../tools/bit_debug"
)
