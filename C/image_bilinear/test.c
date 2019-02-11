#include <stdio.h>
#include <stdlib.h>
#include <cstdio>

#include <gtest/gtest.h>

extern "C" {
  #include "interpolate.h"
}

void printImage(const uint8_t *img, const int width, const int height)
{
  int x, y;
  for(y=0; y<height; ++y)
  {
    for(x=0; x<width; ++x)
    {
      printf("%03d ", img[y * width + x]);
    }
    printf("\n");
  }
}

bool compareImages(const uint8_t *img1, const uint8_t *img2, const int width, const int height, const int stride1, const int stride2)
{
  int x, y, index1, index2;
  for(y=0; y<height; ++y)
  {
    for(x=0; x<width; ++x)
    {
      index1 = y * stride1 + x;
      index2 = y * stride2 + x;
      if(img1[index1] != img2[index2])
      {
        return false;
      }
    }
  }

  return true;
}

class TestSuite : public testing::Test
{
  void SetUp() {}

  void TearDown(){};
};

TEST_F(TestSuite, addBorderLeft) {
  uint8_t image[] = {
                    3, 4,
                    5, 6
  };

  uint8_t expected[] = {
                    0, 3, 4,
                    0, 5, 6
  };

  uint8_t *output = addBorderToImage(image, 2, 2, 0, 0, 1, 0);

  bool res = compareImages(expected, output, 3, 2, 3, 3);
  free(output);

  ASSERT_TRUE(res);
}

TEST_F(TestSuite, addBorderRight) {
  uint8_t image[] = {
                    3, 4,
                    5, 6
  };

  uint8_t expected[] = {
                    3, 4, 0,
                    5, 6, 0
  };

  uint8_t *output = addBorderToImage(image, 2, 2, 0, 0, 0, 1);

  bool res = compareImages(expected, output, 3, 2, 3, 3);
  free(output);

  ASSERT_TRUE(res);
}

TEST_F(TestSuite, addBorderRightBottom) {
  uint8_t image[] = {
                    3, 4,
                    5, 6
  };

  uint8_t expected[] = {
                    3, 4, 0,
                    5, 6, 0,
                    0, 0, 0
  };

  uint8_t *output = addBorderToImage(image, 2, 2, 0, 1, 0, 1);

  bool res = compareImages(expected, output, 3, 3, 3, 3);
  free(output);

  ASSERT_TRUE(res);
}

TEST_F(TestSuite, double_image) {
  uint8_t image[] = {
                    3, 4,
                    5, 6
  };

  uint8_t expected[] = {
                    3, 3, 4, 2,         //3,    3.5,  4, 2,
                    4, 4, 5, 2,         //4,    4.5,  5, 2.5,
                    5, 5, 6, 3,         //5,    5.5,  6, 3,
                    2, 2, 3, 3          //2.5,  2.75, 3, 3
  };

  uint8_t *output = addBorderToImage(image, 2, 2, 0, 1, 0, 1);

  uint8_t *doubled_image = doubleImage(output, 2, 2, 3);
  free(output);

  bool res = compareImages(expected, doubled_image, 4, 4, 4, 4);
  free(doubled_image);

  ASSERT_TRUE(res);
}

TEST_F(TestSuite, half_image_skip) {
  uint8_t image[] = {
                1, 2, 3, 4,
                5, 6, 7, 8,
                9,10,11,12,
                13,14,15,16
  };

  uint8_t expected[] = {
                1, 3,
                9, 11
  };

  uint8_t *half_image = halfImage_skip(image, 4, 4, 4);

  bool res = compareImages(expected, half_image, 2, 2, 2, 2);
  free(half_image);

  ASSERT_TRUE(res);
}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
