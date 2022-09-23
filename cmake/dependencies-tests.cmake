if(NATIVIUM_TARGET STREQUAL "tests")
    find_package(GTest CONFIG REQUIRED)
    target_link_libraries(${NATIVIUM_PROJECT_NAME} PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)
endif()
