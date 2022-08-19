import os

from pygemstones.io import file as f

from core import module as m


# -----------------------------------------------------------------------------
def run(proj_path, target_name, params):
    # build types
    has_debug = True
    has_release = True

    build_types = []

    if has_debug:
        build_types.append("debug")

    if has_release:
        build_types.append("release")

    # archs
    has_ios_arm32 = True
    has_ios_arm64 = True
    has_ios_simulator_x64 = True
    has_ios_simulator_arm64 = True
    has_tvos_arm64 = True
    has_tvos_simulator_x64 = True
    has_watchos_arm32 = True
    has_watchos_arm64 = True
    has_watchos_simulator_x64 = True
    has_mac_catalyst_x64 = True
    has_mac_catalyst_arm64 = True

    archs = []

    # ios - arm32
    if has_ios_arm32:
        archs.extend(
            [
                {
                    "arch": "armv7",
                    "conan_arch": "armv7",
                    "conan_profile": "nativium_ios_profile",
                    "min_version": "9.0",
                    "supported_platform": "iPhoneOS",
                    "enable_bitcode": True,
                    "sdk": "iphoneos",
                    "group": "ios",
                },
            ]
        )

    # ios - arm64
    if has_ios_arm64:
        archs.extend(
            [
                {
                    "arch": "arm64",
                    "conan_arch": "armv8",
                    "conan_profile": "nativium_ios_profile",
                    "min_version": "9.0",
                    "supported_platform": "iPhoneOS",
                    "enable_bitcode": True,
                    "sdk": "iphoneos",
                    "group": "ios",
                },
            ]
        )

    # ios simulator - x64
    if has_ios_simulator_x64:
        archs.extend(
            [
                {
                    "arch": "x86_64",
                    "conan_arch": "x86_64",
                    "conan_profile": "nativium_ios_profile",
                    "min_version": "9.0",
                    "supported_platform": "iPhoneSimulator",
                    "enable_bitcode": False,
                    "sdk": "iphonesimulator",
                    "group": "ios_simulator",
                },
            ]
        )

    # ios simulator - arm64
    if has_ios_simulator_arm64:
        archs.extend(
            [
                {
                    "arch": "arm64",
                    "conan_arch": "armv8",
                    "conan_profile": "nativium_ios_profile",
                    "min_version": "9.0",
                    "supported_platform": "iPhoneSimulator",
                    "enable_bitcode": False,
                    "sdk": "iphonesimulator",
                    "group": "ios_simulator",
                },
            ]
        )

    # tvos - arm64
    if has_tvos_arm64:
        archs.extend(
            [
                {
                    "arch": "arm64",
                    "conan_arch": "armv8",
                    "conan_profile": "nativium_tvos_profile",
                    "min_version": "11.0",
                    "supported_platform": "AppleTVOS",
                    "enable_bitcode": True,
                    "sdk": "appletvos",
                    "group": "tvos",
                },
            ]
        )

    # tvos simulator - x64
    if has_tvos_simulator_x64:
        archs.extend(
            [
                {
                    "arch": "x86_64",
                    "conan_arch": "x86_64",
                    "conan_profile": "nativium_tvos_profile",
                    "min_version": "11.0",
                    "supported_platform": "AppleTVSimulator",
                    "enable_bitcode": False,
                    "sdk": "appletvsimulator",
                    "group": "tvos_simulator",
                },
            ]
        )

    # watchos - arm32
    if has_watchos_arm32:
        archs.extend(
            [
                {
                    "arch": "armv7k",
                    "conan_arch": "armv7k",
                    "conan_profile": "nativium_watchos_profile",
                    "min_version": "5.0",
                    "supported_platform": "WatchOS",
                    "enable_bitcode": True,
                    "sdk": "watchos",
                    "group": "watchos",
                },
            ]
        )

    # watchos - arm64
    if has_watchos_arm64:
        archs.extend(
            [
                {
                    "arch": "arm64_32",
                    "conan_arch": "armv8_32",
                    "conan_profile": "nativium_watchos_profile",
                    "min_version": "5.0",
                    "supported_platform": "WatchOS",
                    "enable_bitcode": True,
                    "sdk": "watchos",
                    "group": "watchos",
                },
            ]
        )

    # watchos - x64
    if has_watchos_simulator_x64:
        archs.extend(
            [
                {
                    "arch": "x86_64",
                    "conan_arch": "x86_64",
                    "conan_profile": "nativium_watchos_profile",
                    "min_version": "5.0",
                    "supported_platform": "WatchSimulator",
                    "enable_bitcode": False,
                    "sdk": "watchsimulator",
                    "group": "watchos_simulator",
                },
            ]
        )

    # mac catalyst
    if has_mac_catalyst_x64:
        archs.extend(
            [
                {
                    "arch": "x86_64",
                    "conan_arch": "x86_64",
                    "conan_profile": "nativium_catalyst_profile",
                    "min_version": "10.15",
                    "supported_platform": "MacOSX",
                    "enable_bitcode": False,
                    "sdk": "macosx",
                    "group": "ios_catalyst",
                    "subsystem_ios_version": "13.1",
                },
            ]
        )

    # mac catalyst arm
    if has_mac_catalyst_arm64:
        archs.extend(
            [
                {
                    "arch": "arm64",
                    "conan_arch": "armv8",
                    "conan_profile": "nativium_catalyst_profile",
                    "min_version": "10.15",
                    "supported_platform": "MacOSX",
                    "enable_bitcode": True,
                    "sdk": "macosx",
                    "group": "ios_catalyst",
                    "subsystem_ios_version": "13.1",
                },
            ]
        )

    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": build_types,
        "archs": archs,
        "umbrella_header": "Nativium.h",
        "install_headers": get_header_dir_list(
            proj_path,
            target_name,
            params,
        ),
    }


# -----------------------------------------------------------------------------
def get_header_dir_list(proj_path, target_name, params):
    result = []
    filter_gen_src = []
    filter_impl_src = []

    module_list = m.get_list(proj_path)
    modules_path = os.path.join(proj_path, "modules")

    for module_name in module_list:
        gluecode_dir = os.path.join(
            modules_path,
            module_name,
            "gluecode",
        )

        module_gen_dir = os.path.join(
            gluecode_dir,
            "generated-src",
            "objc",
        )

        module_impl_dir = os.path.join(
            modules_path,
            module_name,
            "implementation",
            "objc",
        )

        # generated src
        if module_name not in filter_gen_src:
            if f.dir_exists(module_gen_dir):
                result.append(
                    {
                        "type": "dir",
                        "path": module_gen_dir,
                    }
                )

        # implementation
        if module_name not in filter_impl_src:
            if f.dir_exists(module_impl_dir):
                result.append(
                    {
                        "type": "dir",
                        "path": module_impl_dir,
                    }
                )

    return result
