import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
from pygemstones.util import log as l

from core import const
from targets.windows.config import target as config


# -----------------------------------------------------------------------------
def run(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    archs = target_config["archs"]
    build_types = target_config["build_types"]
    param_dry_run = ls.list_has_value(params["args"], "--dry-run")

    if param_dry_run:
        l.i("Running in dry mode...")

    if archs and len(archs) > 0:
        for arch in archs:
            for build_type in build_types:
                l.i("Building for: {0}/{1}...".format(arch["conan_arch"], build_type))

                # variables
                build_dir = os.path.join(
                    proj_path,
                    "build",
                    target_name,
                    build_type,
                    arch["conan_arch"],
                    "target",
                )

                clean_build_dir = True

                if param_dry_run and os.path.isdir(build_dir):
                    clean_build_dir = False

                if clean_build_dir:
                    # clean
                    f.recreate_dir(build_dir)

                # build
                run_args = [
                    "conan",
                    "build",
                    os.path.join(
                        proj_path,
                        "conan",
                        "recipe",
                        const.FILE_NAME_CONANFILE_PY,
                    ),
                    "--source-folder",
                    proj_path,
                    "--build-folder",
                    os.path.join(
                        proj_path,
                        "build",
                        target_name,
                        build_type,
                        arch["conan_arch"],
                        "target",
                    ),
                    "--install-folder",
                    os.path.join(
                        proj_path,
                        "build",
                        target_name,
                        build_type,
                        arch["conan_arch"],
                        "conan",
                    ),
                ]

                if param_dry_run:
                    run_args.append("--build")

                r.run(run_args, build_dir)

                # copy dependencies
                deps_bin_dir = os.path.join(
                    proj_path,
                    "build",
                    target_name,
                    build_type,
                    arch["conan_arch"],
                    "conan",
                    "bin",
                )

                build_bin_dir = os.path.join(build_dir, "bin")

                if os.path.isdir(deps_bin_dir):
                    f.copy_all(deps_bin_dir, build_bin_dir)

                # copy assets
                if "assets_dir" in target_config:
                    assets_dir = target_config["assets_dir"]

                    if assets_dir:
                        assets_dir = os.path.join(proj_path, assets_dir)

                        if os.path.isdir(assets_dir):
                            target_dir = os.path.join(build_dir, "bin")
                            f.copy_all(assets_dir, target_dir)

        l.ok()
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
