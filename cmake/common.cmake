# system
if(MSVC
   OR MSYS
   OR MINGW
)
    # for detecting Windows compilers
    set(NATIVIUM_SYSTEM_WINDOWS YES)
    set(NATIVIUM_DEFAULT_TARGET "windows")
endif()

if(APPLE)
    # for MacOS X or iOS, watchOS, tvOS (since 3.10.3)
    set(NATIVIUM_SYSTEM_APPLE YES)
    set(NATIVIUM_DEFAULT_TARGET "macos")
endif()

if(UNIX AND NOT APPLE)
    # for Linux, BSD, Solaris, Minix
    set(NATIVIUM_SYSTEM_LINUX YES)
    set(NATIVIUM_DEFAULT_TARGET "linux")
endif()

# header files
set(NATIVIUM_HEADER_FILES
    ""
    CACHE INTERNAL ""
)

# source files
set(NATIVIUM_SOURCE_FILES
    ""
    CACHE INTERNAL ""
)

# header search paths
set(NATIVIUM_HEADER_SEARCH_PATHS
    ""
    CACHE INTERNAL ""
)

# source files merged
set(NATIVIUM_SOURCE_FILES_MERGED
    ""
    CACHE INTERNAL ""
)

# library search paths
set(NATIVIUM_LIBRARY_SEARCH_PATHS
    ""
    CACHE INTERNAL ""
)

# framework links
set(NATIVIUM_FRAMEWORK_LINKS
    ""
    CACHE INTERNAL ""
)

# library links
set(NATIVIUM_LIBRARY_LINKS
    ""
    CACHE INTERNAL ""
)

# c flags
set(NATIVIUM_C_FLAGS
    "${NATIVIUM_C_FLAGS} -Wall"
    CACHE INTERNAL ""
)

# cxx flags
set(NATIVIUM_CXX_FLAGS
    "${NATIVIUM_CXX_FLAGS} -std=c++${NATIVIUM_CXX_STANDARD} -Wall"
    CACHE INTERNAL ""
)

# compile options
set(NATIVIUM_COMPILE_OPTIONS
    ""
    CACHE INTERNAL ""
)

# functions
include(${NATIVIUM_ROOT_PATH}/cmake/functions.cmake)

# paths
set(NATIVIUM_MODULES_PATH
    "${NATIVIUM_ROOT_PATH}/modules"
    CACHE INTERNAL ""
)

set(NATIVIUM_TARGETS_PATH
    "${NATIVIUM_ROOT_PATH}/targets"
    CACHE INTERNAL ""
)
