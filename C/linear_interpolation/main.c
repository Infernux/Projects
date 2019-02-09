#include <stdio.h>
#include <stdlib.h>

#include <gtest/gtest.h>

#include "interpolate.h"

#include <cstdio>

class TestSuite : public testing::Test
{
  void SetUp() {}

  void TearDown(){};
};

TEST_F(TestSuite, testcase1) {
  Point p1 = { .x = 0, .y = 0 };
  Point p2 = { .x = 2, .y = 2 };
  Point output;
  interpolate(&output, &p1, &p2);

  EXPECT_EQ(output.x, 1);
  EXPECT_EQ(output.y, 1);
}

TEST_F(TestSuite, testcase2) {
  Point p1 = { .x = 0, .y = 0 };
  Point p2 = { .x = 1, .y = 1 };
  Point output;
  interpolate(&output, &p1, &p2);

  EXPECT_EQ(output.x, 0.5);
  EXPECT_EQ(output.y, 0.5);
}

TEST_F(TestSuite, testcase3) {
  Point p1 = { .x = 0, .y = 0 };
  Point p2 = { .x = 1, .y = 0 };
  Point output;
  interpolate(&output, &p1, &p2);

  EXPECT_EQ(output.x, 0.5);
  EXPECT_EQ(output.y, 0);
}

TEST_F(TestSuite, testcase4) {
  Point p1 = { .x = 1, .y = 1 };
  Point p2 = { .x = 2, .y = 2 };
  Point output;
  interpolate(&output, &p1, &p2);

  EXPECT_EQ(output.x, 1.5);
  EXPECT_EQ(output.y, 1.5);
}

TEST_F(TestSuite, testcase5) {
  Point p1 = { .x = 2, .y = 2 };
  Point p2 = { .x = 1, .y = 1 };
  Point output;
  interpolate(&output, &p1, &p2);

  EXPECT_EQ(output.x, 1.5);
  EXPECT_EQ(output.y, 1.5);
}

TEST_F(TestSuite, testcase6) {
  Point p1 = { .x = 0, .y = 1 };
  Point p2 = { .x = 0, .y = 2 };
  Point output;
  interpolate(&output, &p1, &p2);

  EXPECT_EQ(output.x, 0);
  EXPECT_EQ(output.y, 1.5);
}

TEST_F(TestSuite, vertical2) {
  Point p1 = { .x = 0, .y = 2 };
  Point p2 = { .x = 0, .y = 1 };
  Point output;
  interpolate(&output, &p1, &p2);

  EXPECT_EQ(output.x, 0);
  EXPECT_EQ(output.y, 1.5);
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
