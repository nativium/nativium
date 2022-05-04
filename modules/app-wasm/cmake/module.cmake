# module config
set(MODULE_NAME "app-wasm")

if("${NATIVIUM_TARGET}" MATCHES "^(wasm)$")
    # files
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/include/*.h")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/include/*.hpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/src/*.cpp")
endif()
