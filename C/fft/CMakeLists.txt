cmake_minimum_required(VERSION 3.10)

project(main VERSION 1.0)

add_executable(main
  main.c
  revert_bits.c
  )

add_definitions(
  -g
  )

target_link_libraries(main
  PUBLIC
  -lm
  )
