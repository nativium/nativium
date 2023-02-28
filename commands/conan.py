import os

from pygemstones.system import runner as r
from pygemstones.util import log as l
from pygemstones.system import platform as p


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

    # create default profile
    l.i("Creating default profile...")

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

    # install darwin toolchain
    if p.is_macos():
        l.i("Installing darwin toolchain...")

        r.run(
            ["conan", "create", ".", "nativium/stable"],
            cwd=os.path.join(
                proj_path,
                "conan",
                "darwin-toolchain",
            ),
        )

    l.ok()


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("Available actions:\n", l.MAGENTA)
    l.m("  - setup")


# -----------------------------------------------------------------------------
def get_description(params):
    return "Conan manager tool"
