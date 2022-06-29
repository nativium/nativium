import os

from pygemstones.io import file as f
from pygemstones.system import platform as p
from pygemstones.system import runner as r
from pygemstones.util import log as l


# -----------------------------------------------------------------------------
def get_tool_path(params):
    proj_path = params["proj_path"]

    if p.is_windows():
        tool_file_path = os.path.join(proj_path, "build", "gluecode", "djinni.bat")
    else:
        tool_file_path = os.path.join(proj_path, "build", "gluecode", "djinni")

    return tool_file_path


# -----------------------------------------------------------------------------
def generate(params):
    proj_path = params["proj_path"]
    module_data = params["module_data"]

    if not module_data:
        l.e("Module data is invalid")

    # check required tool
    gluecode_tool_path = get_tool_path(params)

    if not os.path.isfile(gluecode_tool_path):
        l.e(
            "Glue code tool was not found: {0}".format(
                gluecode_tool_path,
            )
        )

    # module data
    module_name = module_data["name"]
    tool_params = module_data["tool_params"]

    module_dir = os.path.join(
        proj_path,
        "modules",
        module_name,
        "gluecode",
    )

    # clean old generated src
    f.remove_dir(os.path.join(module_dir, "generated-src"))
    f.remove_dir(os.path.join(module_dir, "yaml"))

    # run
    runner_args = []
    runner_args.extend([gluecode_tool_path])
    runner_args.extend(tool_params)

    r.run(
        args=" ".join(runner_args),
        shell=True,
        cwd=module_dir,
    )
