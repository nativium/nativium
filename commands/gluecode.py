import importlib
import os
import stat

from pygemstones.io import file as f
from pygemstones.io import net as n
from pygemstones.system import platform as p
from pygemstones.type import list as ls
from pygemstones.util import log as l

from config import gluecode as config
from core import gluecode
from core import module as m


# -----------------------------------------------------------------------------
def run(params):
    args = params["args"]

    if len(args) > 0:
        action = args[0]

        if action:
            if action == "setup":
                setup(params)
            elif action == "generate":
                generate(params)
            elif action == "version":
                version(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def setup(params):
    proj_path = params["proj_path"]

    # version
    version = ls.get_arg_list_value(params["args"], "--version")

    if not version or len(version) == 0:
        gluecode_config = config.run(proj_path, params)
        version = gluecode_config["version"]

    l.i("Glue code tool version: {0}".format(version))

    # prepare tool data
    tool_file_path = gluecode.get_tool_path(params)

    if p.is_windows():
        file_url = "https://github.com/Snapchat/djinni/releases/download/v{0}/djinni.bat".format(
            version
        )
    else:
        file_url = (
            "https://github.com/Snapchat/djinni/releases/download/v{0}/djinni".format(
                version
            )
        )

    # check tool folder
    tool_dir = os.path.dirname(tool_file_path)
    f.recreate_dir(tool_dir)

    # prepare tool data
    try:
        n.download(file_url, tool_file_path)

        # add executable permission
        st = os.stat(tool_file_path)
        os.chmod(tool_file_path, st.st_mode | stat.S_IEXEC)

        # add version
        version_file = os.path.join(tool_dir, ".version")
        f.remove_file(version_file)
        f.set_file_content(version_file, version)
    except Exception as e:
        l.e("Error when download file {0}: {1}".format(file_url, e))

    l.ok()


# -----------------------------------------------------------------------------
def generate(params):
    proj_path = params["proj_path"]

    # single module name
    single_module_name = ls.get_arg_list_value(params["args"], "--name")

    # check modules folder
    modules_path = os.path.join(proj_path, "modules")

    if not os.path.isdir(modules_path):
        l.e("Modules folder not exists: {0}".format(modules_path))

    # get gluecode modules
    module_list = m.get_list(proj_path)

    if module_list:
        if single_module_name:
            l.i("Generating files for single module...")

            if single_module_name in module_list:
                if os.path.isdir(
                    os.path.join(modules_path, single_module_name, "gluecode")
                ):
                    l.i(
                        'Generating glue code files for "{0}"...'.format(
                            single_module_name
                        )
                    )

                    func_path = "modules.{0}.gluecode.generate.run".format(
                        single_module_name
                    )
                    mod_name, func_name = func_path.rsplit(".", 1)
                    mod = importlib.import_module(mod_name)
                    func = getattr(mod, func_name)
                    func(params)
                else:
                    l.i('Module "{0}" was skipped'.format(single_module_name))
        else:
            l.i("Generating files for all modules...")

            for module_name in module_list:
                if not os.path.isdir(
                    os.path.join(modules_path, module_name, "gluecode")
                ):
                    l.i('Module "{0}" was skipped'.format(module_name))
                    continue

                l.i('Generating glue code files for "{0}"...'.format(module_name))

                func_path = "modules.{0}.gluecode.generate.run".format(module_name)
                mod_name, func_name = func_path.rsplit(".", 1)
                mod = importlib.import_module(mod_name)
                func = getattr(mod, func_name)
                func(params)

            l.ok()
    else:
        l.e("No modules to generate")


# -----------------------------------------------------------------------------
def version(params):
    tool_path = gluecode.get_tool_path(params)

    # check tool binary
    if not f.file_exists(tool_path):
        l.e("Glue code tool was not found: {0}".format(tool_path))

    # check version file
    tool_dir = os.path.dirname(tool_path)
    version_file = os.path.join(tool_dir, ".version")

    if not f.file_exists(version_file):
        l.e(
            "Glue code tool version file not found, download it again: {0}".format(
                version_file
            )
        )

    l.i("Version: {0}".format(f.get_file_contents(version_file)))


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("Available actions:\n", l.MAGENTA)
    l.m("  - setup")
    l.m("  - generate")
    l.m("  - version")


# -----------------------------------------------------------------------------
def get_description(params):
    return "Glue code manager tool"
