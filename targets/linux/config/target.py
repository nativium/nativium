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
    has_x64 = True

    archs = []

    # x64
    if has_x64:
        archs.extend(
            [
                {
                    "arch": "x86_64",
                    "conan_arch": "x86_64",
                    "conan_profile": "nativium_linux_profile",
                },
            ]
        )

    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": build_types,
        "assets_dir": "",
        "archs": archs,
    }
