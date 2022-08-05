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
    has_mac_x64 = True
    has_mac_arm64 = True

    archs = []

    # macos - x64
    if has_mac_x64:
        archs.extend(
            [
                {
                    "arch": "x86_64",
                    "conan_arch": "x86_64",
                    "conan_profile": "nativium_macos_profile",
                    "min_version": "10.9",
                    "sdk": "macosx",
                },
            ]
        )

    # macos - arm64
    if has_mac_arm64:
        archs.extend(
            [
                {
                    "arch": "arm64",
                    "conan_arch": "armv8",
                    "conan_profile": "nativium_macos_profile",
                    "min_version": "11.0",
                    "sdk": "macosx",
                },
            ]
        )

    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": build_types,
        "universal_binary": True,
        "assets_dir": "",
        "archs": archs,
    }
