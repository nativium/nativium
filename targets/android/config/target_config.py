# -----------------------------------------------------------------------------
def run(proj_path, target_name, params):
    # build types
    has_debug = True
    has_release = True

    build_types = []

    if has_debug:
        build_types.append("debug")

    if has_release:
        build_types.append("relwithdebinfo")

    # archs
    has_arm32 = True
    has_arm64 = True
    has_x32 = True
    has_x64 = True

    archs = []

    # arm32
    if has_arm32:
        archs.extend(
            [
                {
                    "arch": "armeabi-v7a",
                    "conan_arch": "armv7",
                    "conan_profile": "nativium_android_profile",
                    "api_level": 21,
                },
            ]
        )

    # arm64
    if has_arm64:
        archs.extend(
            [
                {
                    "arch": "arm64-v8a",
                    "conan_arch": "armv8",
                    "conan_profile": "nativium_android_profile",
                    "api_level": 21,
                },
            ]
        )

    # x32
    if has_x32:
        archs.extend(
            [
                {
                    "arch": "x86",
                    "conan_arch": "x86",
                    "conan_profile": "nativium_android_profile",
                    "api_level": 21,
                },
            ]
        )

    # x64
    if has_x64:
        archs.extend(
            [
                {
                    "arch": "x86_64",
                    "conan_arch": "x86_64",
                    "conan_profile": "nativium_android_profile",
                    "api_level": 21,
                },
            ]
        )

    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": build_types,
        "entrypoint": "main",
        "archs": archs,
    }
