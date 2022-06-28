import os

from pygemstones.io import file as f
from pygemstones.type import list as ls
from pygemstones.util import log as l

from core import net
from targets.wasm.config import target as config


# -----------------------------------------------------------------------------
def run(params):
    # prepare data
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    # prepare data
    source = ls.get_arg_list_value(params["args"], "--source")
    build_type = ls.get_arg_list_value(params["args"], "--build")
    arch = ls.get_arg_list_value(params["args"], "--arch")

    # source
    if source:
        source = source.lower()
    else:
        source = "build"

    check_source(source)

    l.i("Source defined: {0}".format(source))

    # build type
    if not build_type:
        build_type = "debug"

    found = False

    for item in target_config["build_types"]:
        if item.lower() == build_type.lower():
            build_type = item
            found = True

    if found:
        l.i("Build type defined: {0}".format(build_type))
    else:
        l.e("Build type is invalid: {0}".format(build_type))

    # arch
    if not arch:
        arch = "wasm"

    l.i("Arch defined: {0}".format(arch))

    # output folder
    if source == "build":
        output_path = os.path.join(
            proj_path,
            "build",
            target_name,
            build_type,
            arch,
            "target",
            "bin",
        )
    elif source == "dist":
        output_path = os.path.join(proj_path, "dist", target_name, build_type, arch)

    if not f.dir_exists(output_path):
        l.e("Output folder not exists: {0}".format(output_path))

    # serve
    net.serve(output_path)


# -----------------------------------------------------------------------------
def check_source(source):
    if not source.lower() in ["build", "dist"]:
        l.e("Invalid source: {0}".format(source.lower()))
