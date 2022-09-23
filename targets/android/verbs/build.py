import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
from pygemstones.util import log as l

from core import const, util
from targets.android.config import target as config


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

                    conan_dir = os.path.join(
                        proj_path,
                        "build",
                        target_name,
                        build_type,
                        arch["arch"],
                        "conan",
                    )

                    clean_build_dir = True

                    # dry run
                    if param_dry_run and os.path.isdir(build_dir):
                        clean_build_dir = False

                    # clean
                    if clean_build_dir:
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
                    ]

                    if param_dry_run:
                        run_args.append("--build")

                    r.run(run_args, cwd=conan_dir)

            l.ok()
        else:
            l.e('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
