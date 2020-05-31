cmake_minimum_required(VERSION 3.10)

project(pss VERSION 1.0)

set(DEBUG ON)
if(DEBUG)
  add_definitions(
    -g
  )
endif()

add_executable(
  pss
  main.c
  pa_helpers.c
  client_socket.c
  socket_manager.c
  queue.c
)

target_include_directories(
  pss
  PUBLIC
  "${PROJECT_BINARY_DIR}"
)

find_library(
  PULSE_LIB
  pulse
)

target_link_libraries(
  pss
  PRIVATE
  -lpthread
  "${PULSE_LIB}"
)
