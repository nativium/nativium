# -----------------------------------------------------------------------------
def run(proj_path, target_name, params):
    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": ["debug", "release"],
        "assets_dir": "",
        "archs": [
            {
                "arch": "x86_64",
                "conan_arch": "x86_64",
                "conan_profile": "nativium_linux_profile",
            },
        ],
    }
