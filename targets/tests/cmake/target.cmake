# conan
nativium_add_conan_build_info()

# modules
nativium_add_modules()

# source
include(${NATIVIUM_TARGETS_PATH}/${NATIVIUM_TARGET}/cmake/source.cmake)

# specific configuration by platform
if(NATIVIUM_SYSTEM_APPLE)
    include(${NATIVIUM_TARGETS_PATH}/${NATIVIUM_TARGET}/cmake/platforms/apple.cmake)
elseif(NATIVIUM_SYSTEM_LINUX)
    include(${NATIVIUM_TARGETS_PATH}/${NATIVIUM_TARGET}/cmake/platforms/linux.cmake)
elseif(NATIVIUM_SYSTEM_WINDOWS)
    include(${NATIVIUM_TARGETS_PATH}/${NATIVIUM_TARGET}/cmake/platforms/windows.cmake)
endif()
