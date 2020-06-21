cmake_minimum_required(VERSION 3.10)

project(qrcode_reader VERSION 1.0)

set(DEBUG ON)
if(DEBUG)
  add_definitions(
    -g
  )
endif()

add_executable(
  qrcode_reader
  main.c
  ecc.c
  galois_helper.c
  image_dump_tools.c
  mask.c
  message_encoding_helpers.c
)

target_include_directories(
  qrcode_reader
  PUBLIC
  "${PROJECT_BINARY_DIR}"
)

add_custom_target(
  mem
  valgrind ./qrcode_reader
  )
