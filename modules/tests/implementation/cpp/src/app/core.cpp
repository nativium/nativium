#include "fixtures/SampleFixture.hpp"
#include "gtest/gtest.h"

#include "nativium/core/ApplicationCore.hpp"

using namespace nativium::core;

// version test
TEST_F(SampleFixture, Version)
{
    auto version = ApplicationCore::shared()->getVersion();
    EXPECT_EQ(version, "1.0.0 (1)");
}

// multiply test
TEST_F(SampleFixture, Multiply)
{
    EXPECT_EQ(ApplicationCore::shared()->multiply(4, 5), 20);
}
