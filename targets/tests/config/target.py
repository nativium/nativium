from pygemstones.system import platform as p


# -----------------------------------------------------------------------------
def run(proj_path, target_name, params):
    return {
        "project_name": "tests",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": ["Release"],
        "assets_dir": get_assets_dir(),
        "archs": get_archs(),
    }


# -----------------------------------------------------------------------------
def get_assets_dir():
    return ""


# -----------------------------------------------------------------------------
def get_archs():
    if p.is_linux():
        return [
            {
                "arch": "x86_64",
                "conan_arch": "x86_64",
                "conan_profile": "nativium_linux_profile",
            },
        ]
    elif p.is_macos():
        return [
            {
                "arch": "x86_64",
                "conan_arch": "x86_64",
                "conan_profile": "nativium_macos_profile",
                "min_version": "10.9",
            }
        ]
    elif p.is_windows():
        return [
            {
                "arch": "x86_64",
                "conan_arch": "x86_64",
                "conan_profile": "nativium_windows_profile",
            }
        ]
    else:
        raise Exception("Running platform is unknown")
