# module config
set(MODULE_NAME "support-lib")

# platform data
if(NATIVIUM_TARGET STREQUAL "android")
    # header files
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.hpp" GLOB)
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.hpp" GLOB)
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/jni/*.hpp" GLOB)

    # source files
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.cpp" GLOB)
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.cpp" GLOB)
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/jni/*.cpp" GLOB FILTER "djinni_main.cpp")

    # module files
    if(NATIVIUM_ENTRYPOINT STREQUAL "main")
        nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/jni/djinni_main.cpp" GLOB)
    elseif(NATIVIUM_ENTRYPOINT STREQUAL "loader")
        nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/nativium/jni/djinni_main.cpp" GLOB)
    endif()

    # search paths
    nativium_add_search_path("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}")
elseif(NATIVIUM_TARGET STREQUAL "ios")
    # header files
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.hpp" GLOB)
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.hpp" GLOB)
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/objc/*.h" GLOB)
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/objc/*.hpp" GLOB)

    # source files
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.cpp" GLOB)
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.cpp" GLOB)
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/objc/*.mm" GLOB)

    # search paths
    nativium_add_search_path("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}")
elseif(NATIVIUM_TARGET STREQUAL "wasm")
    # header files
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.hpp" GLOB)
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.hpp" GLOB)
    nativium_add_header_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/wasm/*.hpp" GLOB)

    # source files
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.cpp" GLOB)
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.cpp" GLOB)
    nativium_add_source_files("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/wasm/*.cpp" GLOB)

    # search paths
    nativium_add_search_path("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}")
endif()
