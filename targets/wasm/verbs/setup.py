import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.util import log as l

from core import const, target, util
from targets.wasm.config import target_config as config


# -----------------------------------------------------------------------------
def run(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    archs = util.get_parsed_arch_list(params, target_config)
    build_types = util.get_parsed_build_type_list(params, target_config)

    if archs and len(archs) > 0:
        if build_types and len(build_types) > 0:
            for arch in archs:
                for build_type in build_types:
                    l.i("Building for: {0}/{1}...".format(arch["arch"], build_type))

                    # conan install
                    build_dir = os.path.join(
                        proj_path,
                        "build",
                        target_name,
                        build_type,
                        arch["arch"],
                        "conan",
                    )

                    f.recreate_dir(build_dir)

                    build_profile = target.get_build_profile()

                    if build_profile != "default":
                        build_profile = os.path.join(
                            proj_path, "conan", "profiles", build_profile
                        )

                    run_args = [
                        "conan",
                        "install",
                        os.path.join(
                            proj_path,
                            const.FILE_NAME_CONANFILE_PY,
                        ),
                        "-pr:b",
                        build_profile,
                        "-pr:h",
                        os.path.join(
                            proj_path, "conan", "profiles", arch["conan_profile"]
                        ),
                    ]

                    target.add_target_setup_common_args(
                        run_args, target_name, target_config, arch, build_type
                    )

                    run_args.append("--build=missing")
                    run_args.append("--update")

                    r.run(run_args, cwd=build_dir)

            l.ok()
        else:
            l.e('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
