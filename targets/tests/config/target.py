from pygemstones.system import platform as p


# -----------------------------------------------------------------------------
def run(proj_path, target_name, params):
    # build types
    has_debug = True
    has_release = False

    build_types = []

    if has_debug:
        build_types.append("debug")

    if has_release:
        build_types.append("release")

    return {
        "project_name": "tests",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": build_types,
        "assets_dir": get_assets_dir(),
        "archs": get_archs(),
    }


# -----------------------------------------------------------------------------
def get_assets_dir():
    return ""


# -----------------------------------------------------------------------------
def get_archs():
    # archs
    has_x64 = True

    archs = []

    if p.is_linux():
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
    elif p.is_macos():
        # x64
        if has_x64:
            archs.extend(
                [
                    {
                        "arch": "x86_64",
                        "conan_arch": "x86_64",
                        "conan_profile": "nativium_macos_profile",
                        "min_version": "10.9",
                    }
                ]
            )
    elif p.is_windows():
        # x64
        if has_x64:
            archs.extend(
                [
                    {
                        "arch": "x86_64",
                        "conan_arch": "x86_64",
                        "conan_profile": "nativium_windows_profile",
                    }
                ]
            )
    else:
        raise Exception("Running platform is unknown")

    return archs
