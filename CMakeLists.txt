# disable cmake format only for this file
# cmake-format: off

# cmake data
cmake_minimum_required(VERSION 3.20.0)

# system
if(MSVC OR MSYS OR MINGW)
    # for detecting Windows compilers
    set(NATIVIUM_SYSTEM_WINDOWS YES)
    set(NATIVIUM_DEFAULT_TARGET "windows")
endif()

if(APPLE)
    # for macOS X or iOS, watchOS, tvOS (since 3.10.3)
    set(NATIVIUM_SYSTEM_APPLE YES)
    set(NATIVIUM_DEFAULT_TARGET "macos")
endif()

if(UNIX AND NOT APPLE)
    # for Linux, BSD, Solaris, Minix
    set(NATIVIUM_SYSTEM_LINUX YES)
    set(NATIVIUM_DEFAULT_TARGET "linux")
endif()

# output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "$<0:>${CMAKE_BINARY_DIR}/bin") # .exe and .dll
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "$<0:>${CMAKE_BINARY_DIR}/lib") # .so and .dylib
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "$<0:>${CMAKE_BINARY_DIR}/lib") # .lib and .a

# main configurations
get_filename_component(CMAKE_SOURCE_REALPATH "${CMAKE_SOURCE_DIR}" REALPATH)
set(NATIVIUM_ROOT_PATH ${CMAKE_SOURCE_REALPATH})

set(NATIVIUM_PROJECT_NAME "nativium" CACHE STRING "Project Name")
set(NATIVIUM_CXX_STANDARD "17" CACHE STRING "Cpp Standard")
set(NATIVIUM_BUILD_TYPE "" CACHE STRING "Build Type")
set(NATIVIUM_TARGET "" CACHE STRING "Target Name")
set(NATIVIUM_VERSION "1.0.0" CACHE STRING "Version")
set(NATIVIUM_VERSION_CODE "1" CACHE STRING "Version Code")
set(NATIVIUM_GROUP "ios" CACHE STRING "Group")
set(NATIVIUM_CODE_COVERAGE OFF CACHE BOOL "Code Coverage")

set(NATIVIUM_HEADER_FILES "" CACHE STRING "Header Files")
set(NATIVIUM_SOURCE_FILES "" CACHE STRING "Source Files")
set(NATIVIUM_HEADER_SEARCH_PATHS "" CACHE STRING "Header Search Paths")
set(NATIVIUM_SOURCE_FILES_MERGED "" CACHE STRING "Source Files Merged")
set(NATIVIUM_LIBRARY_SEARCH_PATHS "" CACHE STRING "Library Search Paths")
set(NATIVIUM_FRAMEWORK_LINKS "" CACHE STRING "Framework Links")
set(NATIVIUM_LIBRARY_LINKS "" CACHE STRING "Library Links")

set(NATIVIUM_ENTRYPOINT "" CACHE STRING "Android Entrypoint Name (empty string or main or loader)")

# project
project(${NATIVIUM_PROJECT_NAME})

# flags
set(NATIVIUM_C_FLAGS "-Wall" CACHE STRING "Custom C Flags")
set(NATIVIUM_CXX_FLAGS "-Wall" CACHE STRING "Custom CXX Flags")
set(NATIVIUM_EXE_LINKER_FLAGS "" CACHE STRING "Custom EXE Linker Flags")

# coverage flags
if(NATIVIUM_CODE_COVERAGE)
    if (CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        set(CODE_COVERAGE_COMPILE_FLAGS "--coverage")
        set(CODE_COVERAGE_LINKER_FLAGS "--coverage")

        message(STATUS "Nativium: Code coverage enabled (${CMAKE_CXX_COMPILER_ID})")
    else()
        set(CODE_COVERAGE_COMPILE_FLAGS "")
        set(CODE_COVERAGE_LINKER_FLAGS "")
    endif()

    set(NATIVIUM_EXE_LINKER_FLAGS "${NATIVIUM_EXE_LINKER_FLAGS} ${CODE_COVERAGE_LINKER_FLAGS}")
    set(NATIVIUM_C_FLAGS "${NATIVIUM_C_FLAGS} ${CODE_COVERAGE_COMPILE_FLAGS}")
    set(NATIVIUM_CXX_FLAGS "${NATIVIUM_CXX_FLAGS} ${CODE_COVERAGE_COMPILE_FLAGS}")
endif()

# compile options
set(NATIVIUM_COMPILE_OPTIONS "" CACHE STRING "Compile Options")

# paths
set(NATIVIUM_MODULES_PATH "${NATIVIUM_ROOT_PATH}/modules" CACHE STRING "Modules Path")
set(NATIVIUM_TARGETS_PATH "${NATIVIUM_ROOT_PATH}/targets" CACHE STRING "Targets Path")

# functions
include(${NATIVIUM_ROOT_PATH}/cmake/functions.cmake)

# architecture
nativium_set_current_arch()

set(NATIVIUM_ARCH ${NATIVIUM_CURRENT_ARCH} CACHE STRING "Architecture")
set(NATIVIUM_PLATFORM_ARCH ${NATIVIUM_CURRENT_ARCH} CACHE STRING "Platform Architecture")

# target
if(NATIVIUM_TARGET STREQUAL "")
    nativium_set_default_target()
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
        set(NATIVIUM_BUILD_PATH ${NATIVIUM_ROOT_PATH}/build/${NATIVIUM_TARGET}/${NATIVIUM_BUILD_TYPE}/${NATIVIUM_GROUP}/${NATIVIUM_ARCH} CACHE STRING "Nativium Build Path")
    else()
        set(NATIVIUM_BUILD_PATH ${NATIVIUM_ROOT_PATH}/build/${NATIVIUM_TARGET}/${NATIVIUM_BUILD_TYPE}/${NATIVIUM_ARCH} CACHE STRING "Nativium Build Path")
    endif()
else()
    set(NATIVIUM_BUILD_PATH ${NATIVIUM_ROOT_PATH}/build/${NATIVIUM_TARGET}/${NATIVIUM_BUILD_TYPE}/${NATIVIUM_ARCH} CACHE STRING "Nativium Build Path")
endif()

# modules
nativium_add_modules()

# source
list(APPEND NATIVIUM_SOURCE_FILES_MERGED ${NATIVIUM_SOURCE_FILES})
list(APPEND NATIVIUM_SOURCE_FILES_MERGED ${NATIVIUM_HEADER_FILES})

# ios platform settings
if(NATIVIUM_TARGET STREQUAL "ios")
    set(CMAKE_OSX_ARCHITECTURES "${NATIVIUM_PLATFORM_ARCH}")
    set(CMAKE_OSX_DEPLOYMENT_TARGET "${NATIVIUM_DEPLOYMENT_TARGET}")

    set(DEVELOPMENT_TEAM_ID "" CACHE STRING "Development Team ID")
    set(CODE_SIGN_IDENTITY "" CACHE STRING "Sign Identity")
    set(FRAMEWORK_NAME "${NATIVIUM_PROJECT_NAME}" CACHE STRING "Framework Name")
    set(FRAMEWORK_BUNDLE_IDENTIFIER "com.nativium.library" CACHE STRING "Bundle Identifier")

    if(NATIVIUM_GROUP STREQUAL "ios" OR "ios_simulator")
        set(DEVICE_FAMILY "1,2" CACHE STRING "Device Family")
    elseif(NATIVIUM_GROUP STREQUAL "tvos" OR "tvos_simulator")
        set(DEVICE_FAMILY "3" CACHE STRING "Device Family")
    elseif(NATIVIUM_GROUP STREQUAL "watchos")
        set(DEVICE_FAMILY "4" CACHE STRING "Device Family")
        set(CMAKE_SYSTEM_VERSION "10.5")
    elseif(NATIVIUM_GROUP STREQUAL "watchos_simulator")
        set(DEVICE_FAMILY "4" CACHE STRING "Device Family")
        set(CMAKE_SYSTEM_VERSION "10.5")
    endif()

    set(NATIVIUM_FRAMEWORK_LINKS ${NATIVIUM_FRAMEWORK_LINKS} "-framework Foundation" CACHE STRING "")
    set(NATIVIUM_C_FLAGS "${NATIVIUM_C_FLAGS} -fobjc-arc -fobjc-abi-version=2" CACHE STRING "")
    set(NATIVIUM_CXX_FLAGS "${NATIVIUM_CXX_FLAGS} -fobjc-arc -fobjc-abi-version=2" CACHE STRING "")
endif()

# macos platform settings
if(NATIVIUM_TARGET STREQUAL "macos")
    set(CMAKE_OSX_ARCHITECTURES "${NATIVIUM_PLATFORM_ARCH}")
    set(CMAKE_OSX_DEPLOYMENT_TARGET "${NATIVIUM_DEPLOYMENT_TARGET}")

    set(DEVELOPMENT_TEAM_ID "" CACHE STRING "Development Team ID")
    set(CODE_SIGN_IDENTITY "" CACHE STRING "Sign Identity")

    set(NATIVIUM_FRAMEWORK_LINKS ${NATIVIUM_FRAMEWORK_LINKS} "-framework Foundation" CACHE STRING "")
endif()

# wasm platform settings
if(NATIVIUM_TARGET STREQUAL "wasm")
    set(NATIVIUM_WASM_LINK_FLAGS "--bind -s MALLOC=emmalloc -s WASM_BIGINT=1")
endif()

# flags
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${NATIVIUM_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${NATIVIUM_CXX_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${NATIVIUM_EXE_LINKER_FLAGS}")

set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_DEBUG} -O0 -g")
set(CMAKE_CXX_FLAGS_MINSIZEREL "${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_MINSIZEREL} -Os")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_RELWITHDEBINFO} -O2 -g")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_RELEASE} -O3")

# specify project type
if("${NATIVIUM_TARGET}" MATCHES "^(ios|android)$")
    add_library(${NATIVIUM_PROJECT_NAME} SHARED ${NATIVIUM_SOURCE_FILES_MERGED})
else()
    add_executable(${NATIVIUM_PROJECT_NAME} ${NATIVIUM_SOURCE_FILES_MERGED})
endif()

# search directories
target_include_directories(${NATIVIUM_PROJECT_NAME} PRIVATE ${NATIVIUM_HEADER_SEARCH_PATHS})
target_link_directories(${NATIVIUM_PROJECT_NAME} PRIVATE ${NATIVIUM_LIBRARY_SEARCH_PATHS})

# linkages
target_link_libraries(${NATIVIUM_PROJECT_NAME} PRIVATE "${NATIVIUM_LIBRARY_LINKS}")
target_link_libraries(${NATIVIUM_PROJECT_NAME} PRIVATE "${NATIVIUM_FRAMEWORK_LINKS}")

# properties
set_target_properties(
    ${NATIVIUM_PROJECT_NAME}
    PROPERTIES
    CXX_STANDARD "${NATIVIUM_CXX_STANDARD}"
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
    CXX_VISIBILITY_PRESET default
    VERSION "${NATIVIUM_VERSION}" # "current version" in semantic format in Mach-O binary file
    SOVERSION "${NATIVIUM_VERSION_MAJOR}" # "compatibility version" in semantic format in Mach-O binary file
    PUBLIC_HEADER "${NATIVIUM_HEADER_FILES}"
)

if(NATIVIUM_TARGET STREQUAL "ios")
    set_target_properties(
        ${NATIVIUM_PROJECT_NAME}
        PROPERTIES
        # framework
        FRAMEWORK TRUE
        FRAMEWORK_VERSION A
        MACOSX_FRAMEWORK_IDENTIFIER "${FRAMEWORK_BUNDLE_IDENTIFIER}"
        # machine readable
        MACOSX_FRAMEWORK_BUNDLE_VERSION "${NATIVIUM_VERSION}"
        # user visible
        MACOSX_FRAMEWORK_SHORT_VERSION_STRING "${NATIVIUM_VERSION}"
        # xcode
        XCODE_ATTRIBUTE_PRODUCT_BUNDLE_IDENTIFIER "${FRAMEWORK_BUNDLE_IDENTIFIER}"
        XCODE_ATTRIBUTE_IPHONEOS_DEPLOYMENT_TARGET "${CMAKE_OSX_DEPLOYMENT_TARGET}"
        XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY "${CODE_SIGN_IDENTITY}"
        XCODE_ATTRIBUTE_CODE_SIGNING_REQUIRED NO
        XCODE_ATTRIBUTE_DEVELOPMENT_TEAM "${DEVELOPMENT_TEAM_ID}"
        XCODE_ATTRIBUTE_TARGETED_DEVICE_FAMILY "${DEVICE_FAMILY}"
        XCODE_ATTRIBUTE_ONLY_ACTIVE_ARCH YES
        XCODE_ATTRIBUTE_SKIP_INSTALL YES
    )

    if(NATIVIUM_GROUP STREQUAL "ios_catalyst")
        set_target_properties(${NATIVIUM_PROJECT_NAME} PROPERTIES INSTALL_RPATH "@loader_path/../../..")
    else()
        set_target_properties(${NATIVIUM_PROJECT_NAME} PROPERTIES XCODE_ATTRIBUTE_INSTALL_PATH "@loader_path/Frameworks")
    endif()
elseif(NATIVIUM_TARGET STREQUAL "macos")
    set_target_properties(
        ${NATIVIUM_PROJECT_NAME}
        PROPERTIES
        XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY "${CODE_SIGN_IDENTITY}"
        XCODE_ATTRIBUTE_DEVELOPMENT_TEAM "${DEVELOPMENT_TEAM_ID}"
        XCODE_ATTRIBUTE_ONLY_ACTIVE_ARCH YES
        XCODE_ATTRIBUTE_SKIP_INSTALL YES
        MACOSX_DEPLOYMENT_TARGET "${CMAKE_OSX_DEPLOYMENT_TARGET}"
    )
elseif(NATIVIUM_TARGET STREQUAL "wasm")
    set_target_properties(
        ${NATIVIUM_PROJECT_NAME}
        PROPERTIES
        LINK_FLAGS
        ${NATIVIUM_WASM_LINK_FLAGS}
    )
endif()

# compile options
target_compile_options(${NATIVIUM_PROJECT_NAME} PRIVATE "${NATIVIUM_COMPILE_OPTIONS}")

# compile definitions
target_compile_definitions(${NATIVIUM_PROJECT_NAME} PRIVATE NATIVIUM_VERSION="${NATIVIUM_VERSION}" NATIVIUM_VERSION_CODE="${NATIVIUM_VERSION_CODE}")
target_compile_definitions(${NATIVIUM_PROJECT_NAME} PRIVATE HAS_UNCAUGHT_EXCEPTIONS=0)

# dependencies
include(${NATIVIUM_ROOT_PATH}/cmake/dependencies.cmake)

# cmake enable format
# cmake-format: on
