#include <stdio.h>
#include <stdlib.h>

#include <gtest/gtest.h>

#include <cstdio>

class TestSuite : public testing::Test
{
  void SetUp() {}

  void TearDown(){};
};

TEST_F(TestSuite, testcase1) {
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
