# -----------------------------------------------------------------------------
def run(proj_path, target_name, params):
    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": ["debug", "release"],
        "entrypoint": "main",
        "archs": [
            {
                "arch": "armeabi-v7a",
                "conan_arch": "armv7",
                "conan_profile": "nativium_android_profile",
                "api_level": 19,
            },
            {
                "arch": "arm64-v8a",
                "conan_arch": "armv8",
                "conan_profile": "nativium_android_profile",
                "api_level": 21,
            },
            {
                "arch": "x86",
                "conan_arch": "x86",
                "conan_profile": "nativium_android_profile",
                "api_level": 19,
            },
            {
                "arch": "x86_64",
                "conan_arch": "x86_64",
                "conan_profile": "nativium_android_profile",
                "api_level": 21,
            },
        ],
    }
