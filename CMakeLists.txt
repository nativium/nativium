# main configurations
cmake_minimum_required(VERSION 3.20.0)

set(NATIVIUM_PROJECT_NAME
    "nativium"
    CACHE STRING "Project Name"
)

set(NATIVIUM_CXX_STANDARD
    "17"
    CACHE STRING "Cpp Standard"
)

set(NATIVIUM_BUILD_TYPE
    ""
    CACHE STRING "Build Type"
)

set(NATIVIUM_TARGET
    ""
    CACHE STRING "Target Name"
)

set(NATIVIUM_VERSION
    "1.0.0"
    CACHE STRING "Version"
)

set(NATIVIUM_VERSION_CODE
    "1"
    CACHE STRING "Version Code"
)

set(NATIVIUM_ARCH
    "x86_64"
    CACHE STRING "Architecture"
)

set(NATIVIUM_PLATFORM_ARCH
    "arm64"
    CACHE STRING "Platform Architecture"
)

set(NATIVIUM_GROUP
    "ios"
    CACHE STRING "Group"
)

get_filename_component(CMAKE_SOURCE_REALPATH "${CMAKE_SOURCE_DIR}" REALPATH)
set(NATIVIUM_ROOT_PATH ${CMAKE_SOURCE_REALPATH})

# project
project(${NATIVIUM_PROJECT_NAME})

# common
include(${NATIVIUM_ROOT_PATH}/cmake/common.cmake)

# target
if(NATIVIUM_TARGET STREQUAL "")
    if(NATIVIUM_SYSTEM_WINDOWS)
        set(NATIVIUM_DEFAULT_TARGET "windows")
    endif()

    if(NATIVIUM_SYSTEM_APPLE)
        set(NATIVIUM_DEFAULT_TARGET "macos")
    endif()

    if(NATIVIUM_SYSTEM_LINUX)
        set(NATIVIUM_DEFAULT_TARGET "linux")
    endif()

    message(STATUS "Nativium: Using default target (${NATIVIUM_DEFAULT_TARGET})")

    set(NATIVIUM_TARGET "${NATIVIUM_DEFAULT_TARGET}")
endif()

# build type
if(NATIVIUM_BUILD_TYPE STREQUAL "")
    message(STATUS "Nativium: Using default cmake build type (${CMAKE_BUILD_TYPE})")
    string(TOLOWER ${CMAKE_BUILD_TYPE} NATIVIUM_BUILD_TYPE)
endif()

# version parts
nativium_version_to_ints(NATIVIUM_VERSION_MAJOR NATIVIUM_VERSION_MINOR NATIVIUM_VERSION_PATCH ${NATIVIUM_VERSION})

# platform configurations
if(NATIVIUM_SYSTEM_APPLE)
    if(NATIVIUM_TARGET STREQUAL "ios")
        set(NATIVIUM_SYSTEM_APPLE_MOBILE YES)
    else()
        set(NATIVIUM_SYSTEM_APPLE_MOBILE NO)
    endif()

    if(NATIVIUM_SYSTEM_APPLE_MOBILE)
        set(NATIVIUM_BUILD_PATH
            ${NATIVIUM_ROOT_PATH}/build/${NATIVIUM_TARGET}/${NATIVIUM_BUILD_TYPE}/${NATIVIUM_GROUP}/${NATIVIUM_ARCH}
            CACHE INTERNAL ""
        )
    else()
        set(NATIVIUM_BUILD_PATH
            ${NATIVIUM_ROOT_PATH}/build/${NATIVIUM_TARGET}/${NATIVIUM_BUILD_TYPE}/${NATIVIUM_ARCH}
            CACHE INTERNAL ""
        )
    endif()
else()
    set(NATIVIUM_BUILD_PATH
        ${NATIVIUM_ROOT_PATH}/build/${NATIVIUM_TARGET}/${NATIVIUM_BUILD_TYPE}/${NATIVIUM_ARCH}
        CACHE INTERNAL ""
    )
endif()

# specific configuration by target
include(${NATIVIUM_TARGETS_PATH}/${NATIVIUM_TARGET}/cmake/target.cmake)
