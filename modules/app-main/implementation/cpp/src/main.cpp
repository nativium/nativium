#include "nativium/core/ApplicationCore.hpp"
#include <iostream>

using namespace nativium::core;

int main(int argc, char **argv)
{
    // multiply
    {
        std::cout << "Multiply result: " << ApplicationCore::shared()->multiply(4, 5) << std::endl;
    }

    // version
    {
        std::cout << "Version: " << ApplicationCore::shared()->getVersion() << std::endl;
    }

    return EXIT_SUCCESS;
}
