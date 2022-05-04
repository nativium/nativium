import glob
import importlib
import os
from collections import OrderedDict

nativium_command_list = OrderedDict()


# -----------------------------------------------------------------------------
def get_all_commands(proj_path, args):
    # search on project path
    project_command_path = os.path.join(proj_path)

    command_list = glob.glob(os.path.join(project_command_path, "commands", "*.py"))

    if command_list:
        for command_path in command_list:
            command_name = os.path.basename(command_path)
            command_name = os.path.splitext(command_name)[0]

            if command_name.startswith("__"):
                continue

            command_package = "{0}.{1}".format("commands", command_name)
            command_module = importlib.import_module(command_package)

            nativium_command_list[command_name] = command_module


# -----------------------------------------------------------------------------
def run_method(command_name, method, params):
    if command_name in nativium_command_list.keys():
        method = getattr(nativium_command_list[command_name], method)
        return method(params)


# -----------------------------------------------------------------------------
def show_help(params):
    params["command_name"] = "show_help"
    nativium_command_list["help"].run(params)


# -----------------------------------------------------------------------------
def process_command(proj_path, args):
    get_all_commands(proj_path, args)

    params = {"args": args, "proj_path": proj_path}

    if len(args) > 0:
        command_name = str(args[0])
        args.pop(0)

        if command_name in nativium_command_list.keys():
            params["command_name"] = command_name
            nativium_command_list[command_name].run(params)
        else:
            show_help(params)
    else:
        show_help(params)
