# module config
set(MODULE_NAME "tests")

if("${NATIVIUM_TARGET}" MATCHES "^(tests)$")
    # header files
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/include/*.h")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/include/*.hpp")
    nativium_add_header_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/include/fixtures/*.hpp")

    # source files
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/src/*.cpp")
    nativium_add_source_files_g("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/src/app/*.cpp")

    # search paths
    nativium_add_search_path("${NATIVIUM_MODULES_PATH}/${MODULE_NAME}/implementation/cpp/include")
endif()
