# module config
set(MODULE_NAME "support-lib")

# platform data
if(NATIVIUM_TARGET STREQUAL "android")
    # header files
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.hpp")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.hpp")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/jni/*.hpp")

    # source files
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.cpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.cpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/jni/*.cpp")

    # remove auto-include main
    list(REMOVE_ITEM NATIVIUM_SOURCE_FILES "${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/jni/djinni_main.cpp")

    # module files
    if(NATIVIUM_ENTRYPOINT STREQUAL "main")
        nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/jni/djinni_main.cpp")
    elseif(NATIVIUM_ENTRYPOINT STREQUAL "loader")
        nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/nativium/jni/djinni_main.cpp")
    endif()

    # search paths
    nativium_add_search_path("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}")
elseif(NATIVIUM_TARGET STREQUAL "ios")
    # header files
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.hpp")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.hpp")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/objc/*.h")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/objc/*.hpp")

    # source files
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.cpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.cpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/objc/*.mm")

    # search paths
    nativium_add_search_path("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}")
elseif(NATIVIUM_TARGET STREQUAL "wasm")
    # header files
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.hpp")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.hpp")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/wasm/*.hpp")

    # source files
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/*.cpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/cpp/*.cpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/djinni/wasm/*.cpp")

    # search paths
    nativium_add_search_path("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}")
endif()
