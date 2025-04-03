import os
from datetime import datetime

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
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
    param_dry_run = ls.list_has_value(params["args"], "--dry-run")

    if param_dry_run:
        l.i("Running in dry mode...")

    if archs and len(archs) > 0:
        if build_types and len(build_types) > 0:
            for arch in archs:
                for build_type in build_types:
                    l.i("Building for: {0}/{1}...".format(arch["arch"], build_type))

                    # variables
                    build_dir = os.path.join(
                        proj_path,
                        "build",
                        target_name,
                        build_type,
                        arch["arch"],
                        "target",
                    )

                    clean_build_dir = True

                    # dry run
                    if param_dry_run and os.path.isdir(build_dir):
                        clean_build_dir = False

                    # clean
                    if clean_build_dir:
                        f.recreate_dir(build_dir)

                    # prepare build profile
                    build_profile = target.get_build_profile()

                    if build_profile != "default":
                        build_profile = os.path.join(
                            proj_path, "conan", "profiles", build_profile
                        )

                    # build
                    run_args = [
                        "conan",
                        "build",
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

                    # copy assets
                    if "assets_dir" in target_config:
                        assets_dir = target_config["assets_dir"]

                        if assets_dir:
                            assets_dir = os.path.join(proj_path, assets_dir)

                            if os.path.isdir(assets_dir):
                                target_dir = os.path.join(build_dir, "bin")
                                f.copy_all(assets_dir, target_dir)

                    # replace data in index.html
                    index_file = os.path.join(build_dir, "bin", "index.html")

                    if f.file_exists(index_file):
                        f.replace_in_file(
                            index_file,
                            "{nativium-timestamp}",
                            str(int(datetime.timestamp(datetime.now()))),
                        )

                        f.replace_in_file(
                            index_file,
                            "{nativium-project-name}",
                            target_config["project_name"],
                        )

                        f.replace_in_file(
                            index_file,
                            "{nativium-product-name}",
                            target_config["product_name"],
                        )

                        f.replace_in_file(
                            index_file, "{nativium-version}", target_config["version"]
                        )

            l.ok()
        else:
            l.e('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
