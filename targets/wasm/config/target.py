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
    has_wasm = True

    archs = []

    # wasm
    if has_wasm:
        archs.extend(
            [
                {
                    "arch": "wasm32",
                    "conan_arch": "wasm",
                    "conan_profile": "nativium_wasm_profile",
                },
            ]
        )

    return {
        "project_name": "nativium",
        "product_name": "Nativium",
        "version": "1.0.0",
        "version_code": "1",
        "build_types": build_types,
        "assets_dir": "targets/wasm/support/web",
        "publish_bucket_name": "nativium",
        "publish_bucket_path": "demo",
        "append_version": True,
        "url": "https://nativium.s3.amazonaws.com/demo",
        "archs": archs,
    }
