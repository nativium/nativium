# -----------------------------------------------------------------------------
def run(proj_path, target_name, params):
    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": ["Debug", "Release"],
        "assets_dir": "targets/wasm/support/web",
        "publish_bucket_name": "nativium",
        "publish_bucket_path": "demo",
        "append_version": True,
        "url": "https://nativium.s3.amazonaws.com/demo",
        "archs": [
            {
                "arch": "wasm",
                "conan_arch": "wasm",
                "conan_profile": "nativium_wasm_profile",
            },
        ],
    }
