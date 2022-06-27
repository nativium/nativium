from pygemstones.system import bootstrap as b

from core import command, util


# -----------------------------------------------------------------------------
def run(proj_path, args):
    util.remove_sdkroot_from_env()
    b.init()
    command.process_command(proj_path, args[1:])
