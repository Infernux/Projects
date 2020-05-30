cmake_minimum_required(VERSION 3.10)

project(pthread_tester VERSION 1.0)

set(DEBUG ON)
if(DEBUG)
  add_definitions(
    -g
  )
endif()

add_executable(
  pthread_tester
  main.c
)

target_link_libraries(
  pthread_tester
  -lpthread
  )
