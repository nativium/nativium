#include "nativium/core/ApplicationCore.hpp"
#include <iostream>

using namespace nativium::core;

int main(int argc, char **argv)
{
    // version
    {
        std::cout << "Module version: " << ApplicationCore::shared()->getVersion() << std::endl;
    }

    return EXIT_SUCCESS;
}
