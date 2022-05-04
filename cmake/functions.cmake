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
macro(nativium_add_header_files new_file_list)
    list(APPEND NATIVIUM_HEADER_FILES ${new_file_list})
endmacro()

# add header files to project using glob
macro(nativium_add_header_files_g new_path)
    file(GLOB files "${new_path}")
    list(APPEND NATIVIUM_HEADER_FILES ${files})
endmacro()

# add header files to project using glob recursive
macro(nativium_add_header_files_gr new_path)
    file(GLOB_RECURSE files "${new_path}")
    list(APPEND NATIVIUM_HEADER_FILES ${files})
endmacro()

# add source files to project
macro(nativium_add_source_files new_file_list)
    list(APPEND NATIVIUM_SOURCE_FILES ${new_file_list})
endmacro()

# add source files to project using glob
macro(nativium_add_source_files_g new_path)
    file(GLOB files "${new_path}")
    list(APPEND NATIVIUM_SOURCE_FILES ${files})
endmacro()

# add source files to project using glob recursive
macro(nativium_add_source_files_gr new_path)
    file(GLOB_RECURSE files "${new_path}")
    list(APPEND NATIVIUM_SOURCE_FILES ${files})
endmacro()

# split version into parts
macro(nativium_version_to_ints major minor patch version)
    string(REGEX REPLACE "([0-9]+).[0-9]+.[0-9]+" "\\1" ${major} ${version})
    string(REGEX REPLACE "[0-9]+.([0-9]+).[0-9]+" "\\1" ${minor} ${version})
    string(REGEX REPLACE "[0-9]+.[0-9]+.([0-9]+)" "\\1" ${patch} ${version})
endmacro()

# add conan build information file
macro(nativium_add_conan_build_info)
    if(EXISTS "${NATIVIUM_BUILD_PATH}/conan/conanbuildinfo.cmake")
        include(${NATIVIUM_BUILD_PATH}/conan/conanbuildinfo.cmake)
        conan_basic_setup()
    else()
        message(FATAL_ERROR "Did you forget to run the prepare command? Conan file for dependencies was not found in path: ${NATIVIUM_BUILD_PATH}/conan/conanbuildinfo.cmake")
    endif()
endmacro()
