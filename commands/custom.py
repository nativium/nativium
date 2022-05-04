import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
from pygemstones.util import log as l


# -----------------------------------------------------------------------------
def run(params):
    args = params["args"]

    if len(args) > 0:
        action = args[0]

        if action:
            if action == "install":
                install(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def install(params):
    proj_path = params["proj_path"]

    # custom path
    custom_path = ls.get_arg_list_value(params["args"], "--path")

    if not custom_path:
        custom_path = os.path.join(proj_path, "custom")

    # config file
    config_file = os.path.join(custom_path, "custom_config.py")

    if not f.file_exists(config_file):
        l.e("Configuration file not exists: {0}".format(config_file))

    # process
    l.i("Processing custom files from {0}...".format(custom_path))

    install_list = r.run_external(
        path=custom_path,
        module_name="custom_config",
        command_name="run",
        command_params=params,
        show_log=False,
        show_error_log=True,
        throw_error=True,
    )

    if install_list:
        for install_item in install_list:
            # data
            install_type = install_item["type"] if "type" in install_item else ""
            install_source = install_item["source"] if "source" in install_item else ""
            install_target = install_item["target"] if "target" in install_item else ""
            install_path = install_item["path"] if "path" in install_item else ""

            # prepare
            if install_source:
                install_source = os.path.abspath(
                    os.path.join(custom_path, install_source)
                )

            if install_target:
                install_target = os.path.abspath(
                    os.path.join(proj_path, install_target)
                )

            if install_path:
                install_path = os.path.abspath(os.path.join(proj_path, install_path))

            # process
            if install_type == "copy-file":
                l.i("Copying file {0}".format(install_source))
                f.copy_file(install_source, install_target)
            elif install_type == "copy-dir":
                l.i("Copying directory {0}".format(install_source))
                f.copy_dir(install_source, install_target, symlinks=True)
            elif install_type == "symlink":
                l.i("Creating symbolic link for {0}".format(install_source))
                is_dir = os.path.isdir(install_source)
                f.symlink(
                    install_source,
                    install_target,
                    recreate=True,
                    target_is_directory=is_dir,
                )
            elif install_type == "remove-file":
                l.i("Removing file {0}".format(install_path))
                f.remove_file(install_path)
            elif install_type == "remove-dir":
                l.i("Removing directory {0}".format(install_path))
                f.remove_dir(install_path)
            elif install_type == "remove-symlink":
                l.i("Remove symbolic link {0}".format(install_path))
                f.unlink(install_path)
            elif install_type == "replace-text":
                install_replace_list = (
                    install_item["list"] if "list" in install_item else None
                )

                if install_replace_list:
                    l.i("Replacing text from {0}".format(install_path))

                    for replace_item in install_replace_list:
                        install_old_text = (
                            replace_item["old"] if "old" in replace_item else ""
                        )

                        install_new_text = (
                            replace_item["new"] if "new" in replace_item else ""
                        )

                        f.replace_in_file(
                            install_path, install_old_text, install_new_text
                        )
            else:
                l.e("Invalid install type: {0}".format(install_type))

    l.ok()


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("Available actions:\n", l.MAGENTA)
    l.m("  - install")


# -----------------------------------------------------------------------------
def get_description(params):
    return "Custom files manager tool"
