import os

from pygemstones.io import file as f
from pygemstones.util import log as l

from core import util
from targets.wasm.config import target as config


# -----------------------------------------------------------------------------
def run(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    archs = util.get_parsed_arch_list(params, target_config)
    build_types = util.get_parsed_build_type_list(params, target_config)

    l.i("Packaging...")

    if archs and len(archs) > 0:
        if build_types and len(build_types) > 0:
            for arch in archs:
                for build_type in build_types:
                    l.i("Copying for: {0}/{1}...".format(arch["arch"], build_type))

                    # create folders
                    dist_dir = os.path.join(
                        proj_path,
                        "dist",
                        target_name,
                        build_type,
                        arch["arch"],
                    )

                    f.recreate_dir(dist_dir)

                    build_dir = os.path.join(
                        proj_path,
                        "build",
                        target_name,
                        build_type,
                        arch["arch"],
                        "target",
                        "bin",
                    )

                    # copy files
                    f.copy_all(build_dir, dist_dir)

            l.ok()
        else:
            l.e('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
