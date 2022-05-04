from pygemstones.system import bootstrap as b

from core import command


# -----------------------------------------------------------------------------
def run(proj_path, args):
    b.init()
    command.process_command(proj_path, args[1:])
