# add module
macro(nativium_add_module name)
    message(STATUS "Nativium: Adding module ${name}")
    include(${NATIVIUM_MODULES_PATH}/${name}/cmake/module.cmake)
endmacro()

# add all modules
macro(nativium_add_modules)
    message(STATUS "Nativium: Adding modules...")

    nativium_list_subdirs(modules ${NATIVIUM_MODULES_PATH} TRUE)

    foreach(module ${modules})
        if(EXISTS "${NATIVIUM_MODULES_PATH}/${module}/cmake/module.cmake")
            nativium_add_module(${module})
        endif()
    endforeach()

    message(STATUS "Nativium: Modules added")
endmacro()

# list all subdirs
macro(nativium_list_subdirs retval curdir return_relative)
    file(
        GLOB sub-dir
        RELATIVE ${curdir}
        ${curdir}/*
    )

    set(${retval} "")

    foreach(dir ${sub-dir})
        if(IS_DIRECTORY ${curdir}/${dir})
            if(${return_relative})
                list(APPEND ${retval} ${dir})
            else()
                list(APPEND ${retval} ${curdir}/${dir})
            endif()
        endif()
    endforeach()
endmacro()

# add search path to project
macro(nativium_add_search_path new_path)
    list(APPEND NATIVIUM_HEADER_SEARCH_PATHS ${new_path})
endmacro()

# add header files to project
macro(nativium_add_header_files new_path)
    set(FN_OPTIONS_ARGS "INSTALL;GLOB;RECURSIVE")
    set(FN_ONE_VALUE_ARGS "")
    set(FN_MULT_VALUE_ARGS "FILTER;INSTALL_FILTER")

    cmake_parse_arguments(nativium_add_header_files "${FN_OPTIONS_ARGS}" "${FN_ONE_VALUE_ARGS}" "${FN_MULT_VALUE_ARGS}" ${ARGN})

    if(nativium_add_header_files_GLOB AND nativium_add_header_files_RECURSIVE)
        message(FATAL_ERROR "You can't use GLOB and RECURSIVE together")
    endif()

    # prepare files
    if(nativium_add_header_files_GLOB)
        # glob mode
        file(GLOB files "${new_path}")
    elseif(nativium_add_header_files_RECURSIVE)
        # glob and recursive mode
        file(GLOB_RECURSE files "${new_path}")
    else()
        # simple path or path list
        set(files ${new_path})
    endif()

    # filter
    if(nativium_add_header_files_FILTER)
        foreach(filter_item ${nativium_add_header_files_FILTER})
            list(FILTER files EXCLUDE REGEX "${filter_item}")
        endforeach()
    endif()

    list(APPEND NATIVIUM_HEADER_FILES ${files})

    # public headers
    if(nativium_add_header_files_INSTALL)
        if(nativium_add_header_files_INSTALL_FILTER)
            foreach(filter_item ${nativium_add_header_files_INSTALL_FILTER})
                list(FILTER files EXCLUDE REGEX "${filter_item}")
            endforeach()
        endif()

        list(APPEND NATIVIUM_PUBLIC_HEADER_FILES ${files})
    endif()
endmacro()

# add source files to project
macro(nativium_add_source_files new_path)
    set(FN_OPTIONS_ARGS "GLOB;RECURSIVE")
    set(FN_ONE_VALUE_ARGS "")
    set(FN_MULT_VALUE_ARGS "FILTER")

    cmake_parse_arguments(nativium_add_source_files "${FN_OPTIONS_ARGS}" "${FN_ONE_VALUE_ARGS}" "${FN_MULT_VALUE_ARGS}" ${ARGN})

    if(nativium_add_source_files_GLOB AND nativium_add_source_files_RECURSIVE)
        message(FATAL_ERROR "You can't use GLOB and RECURSIVE together")
    endif()

    # prepare files
    if(nativium_add_source_files_GLOB)
        # glob mode
        file(GLOB files "${new_path}")
    elseif(nativium_add_source_files_RECURSIVE)
        # glob and recursive mode
        file(GLOB_RECURSE files "${new_path}")
    else()
        # simple path or path list
        set(files ${new_path})
    endif()

    # filter
    if(nativium_add_source_files_FILTER)
        foreach(filter_item ${nativium_add_source_files_FILTER})
            list(FILTER files EXCLUDE REGEX "${filter_item}")
        endforeach()
    endif()

    list(APPEND NATIVIUM_SOURCE_FILES ${files})
endmacro()

# split version into parts
macro(nativium_version_to_ints major minor patch version)
    string(REGEX REPLACE "([0-9]+).[0-9]+.[0-9]+" "\\1" ${major} ${version})
    string(REGEX REPLACE "[0-9]+.([0-9]+).[0-9]+" "\\1" ${minor} ${version})
    string(REGEX REPLACE "[0-9]+.[0-9]+.([0-9]+)" "\\1" ${patch} ${version})
endmacro()

# get current architecture
macro(nativium_set_current_arch)
    set(NATIVIUM_CURRENT_ARCH "${CMAKE_HOST_SYSTEM_PROCESSOR}")
endmacro()

# set default target
macro(nativium_set_default_target)
    if(NATIVIUM_SYSTEM_WINDOWS)
        set(NATIVIUM_DEFAULT_TARGET "windows")
    endif()

    if(NATIVIUM_SYSTEM_APPLE)
        set(NATIVIUM_DEFAULT_TARGET "macos")
    endif()

    if(NATIVIUM_SYSTEM_LINUX)
        set(NATIVIUM_DEFAULT_TARGET "linux")
    endif()
endmacro()

# copy public headers
macro(nativium_copy_public_headers)
    set(FN_OPTIONS_ARGS "")
    set(FN_ONE_VALUE_ARGS "TARGET;INCLUDE_DIR")
    set(FN_MULT_VALUE_ARGS "")

    cmake_parse_arguments(nativium_copy_public_headers "${FN_OPTIONS_ARGS}" "${FN_ONE_VALUE_ARGS}" "${FN_MULT_VALUE_ARGS}" ${ARGN})

    foreach(file_item ${NATIVIUM_PUBLIC_HEADER_FILES})
        # general
        set(original_file_item "${file_item}")

        # check for module
        string(FIND "${file_item}" "${NATIVIUM_ROOT_PATH}/modules" module_found)

        if(module_found GREATER -1)
            string(REPLACE "${NATIVIUM_ROOT_PATH}/modules/" "" file_item "${file_item}")
            string(REGEX REPLACE "(.*)/gluecode/([A-Za-z0-9_-]*)/([A-Za-z0-9_-]*)/" "" file_item "${file_item}")
        endif()

        # add custom command
        add_custom_command(
            TARGET ${nativium_copy_public_headers_TARGET}
            POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy "${original_file_item}" "$<TARGET_BUNDLE_DIR:${nativium_copy_public_headers_TARGET}>/${nativium_copy_public_headers_INCLUDE_DIR}/${file_item}"
            COMMENT "Public Header Copy: ${original_file_item}"
        )
    endforeach()
endmacro()
