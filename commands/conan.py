from pygemstones.system import runner as r
from pygemstones.util import log as l


# -----------------------------------------------------------------------------
def run(params):
    args = params["args"]

    if len(args) > 0:
        action = args[0]

        if action:
            if action == "setup":
                setup(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def setup(params):
    proj_path = params["proj_path"]

    l.i("Creating default profile...")

    # create default profile
    r.run(
        [
            "conan",
            "profile",
            "new",
            "default",
            "--detect",
            "--force",
        ],
        cwd=proj_path,
    )

    l.ok()


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("Available actions:\n", l.MAGENTA)
    l.m("  - setup")


# -----------------------------------------------------------------------------
def get_description(params):
    return "Conan manager tool"
