cmake_minimum_required(VERSION 3.22)

set(project_name ppm_reader)
project(${project_name})

add_library(
  ppm_lib
  utils.c
  file_readers.c
)

target_include_directories(
  ppm_lib
  PUBLIC
  .
)

add_executable(
  ${project_name}
  ppm_reader.c
  drawing_cairo.c
)

target_link_libraries(
  ${project_name}
  PUBLIC
  ppm_lib
  cairo
  X11
)
