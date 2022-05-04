from pygemstones.util import log as l

from core import app_android, app_ios


# -----------------------------------------------------------------------------
def run(params):
    args = params["args"]

    if len(args) >= 1:
        platform = args[0]

        if platform:
            if platform == "android":
                app_android.run(params)
            elif platform == "ios":
                app_ios.run(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def get_description(params):
    return "Application manager tool"


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("Available platforms:\n", l.MAGENTA)
    l.m("  - android")
    l.m("  - ios")
