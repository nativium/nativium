import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
from pygemstones.util import log as l

from config import apps as config
from core import tool


# -----------------------------------------------------------------------------
def run(params):
    args = params["args"]

    if len(args) >= 2:
        action = args[1]

        if action:
            if action == "build":
                ios_build(params)
            elif action == "test":
                ios_test(params)
            elif action == "install":
                ios_install(params)
            elif action == "uninstall":
                ios_uninstall(params)
            elif action == "run":
                ios_run(params)
            elif action == "archive":
                ios_archive(params)
            elif action == "clean":
                ios_clean(params)
            elif action == "pods":
                ios_pods(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def ios_build(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")
    build_type = get_build_type(params)

    l.i("Building application {0} for {1}...".format(name, build_type.lower()))

    # check tool xcodebuild
    tool.check_tool_xcodebuild()

    # run build
    proj_path = params["proj_path"]
    derived_path = os.path.join(proj_path, "build", "derived-data", name)

    run_args = [
        "xcodebuild",
        "-scheme",
        config["scheme"],
        "-derivedDataPath",
        derived_path,
        "-workspace",
        config["workspace"],
        "-configuration",
        build_type,
        "build",
        "-destination",
        config["destination"]["build"],
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def ios_test(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")

    l.i("Testing application {0}...".format(name))

    # check tool xcodebuild
    tool.check_tool_xcodebuild()

    # run test
    proj_path = params["proj_path"]
    derived_path = os.path.join(proj_path, "build", "derived-data", name)

    run_args = [
        "xcodebuild",
        "-scheme",
        config["scheme"],
        "-derivedDataPath",
        derived_path,
        "-workspace",
        config["workspace"],
        "test",
        "-destination",
        config["destination"]["test"],
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def ios_install(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")
    build_type = get_build_type(params)

    l.i("Installing application {0} for {1}...".format(name, build_type.lower()))

    # check tool xcodebuild
    tool.check_tool_xcodebuild()

    # check tool ios deploy
    tool.check_tool_ios_deploy()

    # build
    ios_build(params)

    # run deploy
    proj_path = params["proj_path"]
    derived_path = os.path.join(proj_path, "build", "derived-data", name)

    run_args = [
        "ios-deploy",
        "--bundle",
        os.path.join(
            derived_path,
            "Build",
            "Products",
            "{0}-iphoneos".format(build_type),
            config["product"],
        ),
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def ios_uninstall(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")

    l.i("Uninstalling application {0}...".format(name))

    # check tool ios deploy
    tool.check_tool_ios_deploy()

    # run deploy
    run_args = [
        "ios-deploy",
        "--uninstall_only",
        "--bundle_id",
        config["bundle-id"],
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def ios_run(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")
    build_type = get_build_type(params)

    l.i("Running application {0} for {1}...".format(name, build_type.lower()))

    # check tool xcodebuild
    tool.check_tool_xcodebuild()

    # check tool ios deploy
    tool.check_tool_ios_deploy()

    # build
    ios_build(params)

    # run deploy
    proj_path = params["proj_path"]
    derived_path = os.path.join(proj_path, "build", "derived-data", name)
    bundle_path = os.path.join(
        derived_path,
        "Build",
        "Products",
        "{0}-iphoneos".format(build_type),
        config["product"],
    )

    if not f.dir_exists(bundle_path):
        l.e(
            "You need build first because derived data don't exists: {0}".format(
                bundle_path
            )
        )

    run_args = [
        "ios-deploy",
        "--debug",
        "--noninteractive",
        "--bundle",
        bundle_path,
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def ios_archive(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")

    l.i("Archiving application {0}...".format(name))

    # check tool xcodebuild
    tool.check_tool_xcodebuild()

    # run build
    proj_path = params["proj_path"]
    archive_path = os.path.join(
        proj_path, "build", "archive-data", "{0}.xcarchive".format(name)
    )

    f.remove_dir(archive_path)

    run_args = [
        "xcodebuild",
        "-scheme",
        config["name"],
        "-workspace",
        config["workspace"],
        "-destination",
        config["destination"]["archive"],
        "archive",
        "-archivePath",
        archive_path,
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def ios_clean(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")
    build_type = get_build_type(params)

    l.i("Cleaning application {0} for {1}...".format(name, build_type.lower()))

    # check tool xcodebuild
    tool.check_tool_xcodebuild()

    # run build
    proj_path = params["proj_path"]
    derived_path = os.path.join(proj_path, "build", "derived-data", name)

    run_args = [
        "xcodebuild",
        "-scheme",
        config["name"],
        "-workspace",
        config["workspace"],
        "-destination",
        config["destination"]["archive"],
        "-derivedDataPath",
        derived_path,
        "clean",
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def ios_pods(params):
    # parameters
    name = get_name(params)
    path = get_ios_path(params)
    config = get_config(params, "ios")

    l.i("Running cocoapods for {0}...".format(name))

    # check tool cocoapods
    tool.check_tool_cocoapods()

    # run cocoapods
    run_args = [
        "pod",
        "install",
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def get_name(params):
    proj_path = params["proj_path"]
    name = ls.get_arg_list_value(params["args"], "--app")

    if not name:
        name = "runner"

    path = os.path.join(proj_path, "apps", "android", name)

    if not f.dir_exists(path):
        l.e("The application {0} don't exists: {1}".format(name, path))

    return name


# -----------------------------------------------------------------------------
def get_android_path(params):
    proj_path = params["proj_path"]
    name = get_name(params)

    return os.path.join(proj_path, "apps", "android", name)


# -----------------------------------------------------------------------------
def get_ios_path(params):
    proj_path = params["proj_path"]
    name = get_name(params)

    return os.path.join(proj_path, "apps", "ios", name)


# -----------------------------------------------------------------------------
def get_build_type(params):
    build_type = ls.get_arg_list_value(params["args"], "--build")

    if build_type:
        if build_type.lower() == "debug":
            build_type = "Debug"
        elif build_type.lower() == "release":
            build_type = "Release"
    else:
        build_type = "Debug"

    return build_type


# -----------------------------------------------------------------------------
def get_config(params, platform):
    proj_path = params["proj_path"]
    name = get_name(params)
    config_data = config.run(proj_path, params)

    if platform in config_data:
        if name in config_data[platform]:
            return config_data[platform][name]

    l.e(
        "Configuration for application {0} and platform {1} don't exists".format(
            name, platform
        )
    )


# -----------------------------------------------------------------------------
def get_description(params):
    return "Application manager tool"


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("Available actions:\n", l.MAGENTA)
    l.m("  - build")
    l.m("  - test")
    l.m("  - install")
    l.m("  - uninstall")
    l.m("  - run")
    l.m("  - archive")
    l.m("  - clean")
    l.m("  - pods")
