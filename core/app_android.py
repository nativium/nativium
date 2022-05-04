import os
import subprocess

from pygemstones.io import file as f
from pygemstones.system import platform as p
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
            # android
            if action == "build":
                android_build(params)
            elif action == "test":
                android_test(params)
            elif action == "integration-test":
                android_integration_test(params)
            elif action == "install":
                android_install(params)
            elif action == "uninstall":
                android_uninstall(params)
            elif action == "run":
                android_run(params)
            elif action == "bundle":
                android_bundle(params)
            elif action == "logcat":
                android_logcat(params)
            elif action == "clean":
                android_clean(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def android_build(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)
    build_type = get_build_type(params)

    l.i("Building application {0} for {1}...".format(name, build_type.lower()))

    # check tool gradlew
    tool.check_tool_gradlew(params, name)

    # run build
    if p.is_windows():
        os.chdir(path)

        run_args = ["gradlew.bat"]
    else:
        run_args = ["./gradlew"]

    run_args.append("assemble{0}".format(build_type))

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_test(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)

    l.i("Testing application {0}...".format(name))

    # check tool gradlew
    tool.check_tool_gradlew(params, name)

    # run test
    if p.is_windows():
        os.chdir(path)

        run_args = ["gradlew.bat"]
    else:
        run_args = ["./gradlew"]

    run_args.append("test")

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_integration_test(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)

    l.i("Testing application {0}...".format(name))

    # check tool gradlew
    tool.check_tool_gradlew(params, name)

    # run test
    if p.is_windows():
        os.chdir(path)

        run_args = ["gradlew.bat"]
    else:
        run_args = ["./gradlew"]

    run_args.append("connectedAndroidTest")

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_install(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)
    build_type = get_build_type(params)

    l.i("Installing application {0} for {1}...".format(name, build_type.lower()))

    # check tool gradlew
    tool.check_tool_gradlew(params, name)

    # run install
    if p.is_windows():
        os.chdir(path)

        run_args = ["gradlew.bat"]
    else:
        run_args = ["./gradlew"]

    run_args.append("install{0}".format(build_type))

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_uninstall(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)

    l.i("Uninstalling application {0}...".format(name))

    # check tool gradlew
    tool.check_tool_gradlew(params, name)

    # run build
    if p.is_windows():
        os.chdir(path)

        run_args = ["gradlew.bat"]
    else:
        run_args = ["./gradlew"]

    run_args.append("uninstallAll")

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_run(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)
    config = get_config(params, "android")
    build_type = get_build_type(params)

    l.i("Running application {0} for {1}...".format(name, build_type.lower()))

    # check tool adb
    tool.check_tool_adb()

    # install
    android_install(params)

    # open
    run_args = [
        "adb",
        "shell",
        "am",
        "start",
        "-n",
        "{0}/{1}".format(config["package"], config["activity"]),
    ]

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_bundle(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)
    build_type = get_build_type(params)

    l.i(
        "Building {0} bundle for application {1}...".format(
            build_type.lower(),
            name,
        )
    )

    # check tool gradlew
    tool.check_tool_gradlew(params, name)

    # run bundle
    if p.is_windows():
        os.chdir(path)

        run_args = ["gradlew.bat"]
    else:
        run_args = ["./gradlew"]

    run_args.append("bundle{0}".format(build_type))

    r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_logcat(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)
    config = get_config(params, "android")
    clean_action = ls.list_has_value(params["args"], "--clean")

    if clean_action:
        l.i("Cleaning logcat...")

        # check tool adb
        tool.check_tool_adb()

        # clean
        run_args = [
            "adb",
            "logcat",
            "-c",
        ]

        r.run(run_args, path)
    else:
        l.i(
            "Logcat for application {0} and package {1}...".format(
                name, config["package"]
            )
        )

        # check tool adb
        tool.check_tool_adb()

        # get pid
        run_args = [
            "adb",
            "shell",
            "pidof",
            "-s",
            config["package"],
        ]

        adb_pid = subprocess.check_output(run_args).decode("utf-8").strip()

        if adb_pid == None or adb_pid == "":
            l.e("Process not found for package {0}".format(config["package"]))

        l.i(
            "The process number (PID) for package {0} is {1}".format(
                config["package"], adb_pid
            )
        )

        # logcat with filter by pid
        run_args = [
            "adb",
            "logcat",
            "-v",
            "color",
            "--pid={0}".format(adb_pid),
        ]

        r.run(run_args, path)

    l.ok()


# -----------------------------------------------------------------------------
def android_clean(params):
    # parameters
    name = get_name(params)
    path = get_android_path(params)

    l.i("Cleaning application {0}...".format(name))

    # check tool gradlew
    tool.check_tool_gradlew(params, name)

    # run install
    if p.is_windows():
        os.chdir(path)

        run_args = ["gradlew.bat"]
    else:
        run_args = ["./gradlew"]

    run_args.append("clean")

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
    l.m("  - integration-test")
    l.m("  - install")
    l.m("  - uninstall")
    l.m("  - run")
    l.m("  - bundle")
    l.m("  - logcat")
    l.m("  - clean")
