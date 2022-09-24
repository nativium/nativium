cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(darwin-toolchain CONFIG REQUIRED)

add_executable(example src/example.cpp)
set_target_properties(example PROPERTIES MACOSX_BUNDLE FALSE)
target_link_libraries(example darwin-toolchain::darwin-toolchain)
