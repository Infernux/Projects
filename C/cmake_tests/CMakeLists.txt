cmake_minimum_required(VERSION 3.10)

project(main VERSION 1.0)

configure_file(version.h.in version.h)

add_subdirectory(math_library)
add_executable(main main.c)

target_link_libraries(main PUBLIC my_math)

target_include_directories(main PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          "${PROJECT_BINARY_DIR}/math_library"
                          )
