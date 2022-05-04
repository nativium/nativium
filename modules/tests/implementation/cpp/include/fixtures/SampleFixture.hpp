#include "gtest/gtest.h"

class SampleFixture : public ::testing::Test
{
protected:
    SampleFixture()
    {
        // you can do set-up work for each test here.
    }

    ~SampleFixture() override
    {
        // cleanup any pending stuff, but no exceptions allowed
    }

    void SetUp() override
    {
        // code here will be called immediately after the constructor (right before each test)
    }

    void TearDown() override
    {
        // code here will be called immediately after each test (right before the destructor)
    }

    // class members declared here can be used by all tests in the test suite
};
