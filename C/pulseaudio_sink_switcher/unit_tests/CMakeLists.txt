cmake_minimum_required(VERSION 3.10)

project(pss_unit_tester VERSION 1.0)

enable_testing()
find_package(GTest REQUIRED)
include(GoogleTest)

add_executable(
  pss_unit
  pss_test.cpp
)

target_link_libraries(
  pss_unit
  GTest::GTest
  GTest::Main
)

gtest_discover_tests(
  pss_unit
)



target_include_directories(
  pss_unit
  PUBLIC
  "${PROJECT_BINARY_DIR}"
)
