import os

from pygemstones.io import file as f
from pygemstones.system import platform as p
from pygemstones.util import log as l

from core import const


# -----------------------------------------------------------------------------
def get_all_targets(proj_path, throw_error=True):
    results = []

    targets_path = os.path.join(proj_path, "targets")

    if not os.path.isdir(targets_path):
        if throw_error:
            l.e("Target folder not exists: {0}".format(targets_path))
        else:
            return results

    targets = f.find_dirs(targets_path, "*")

    if targets:
        for target_path in targets:
            target_name = os.path.basename(target_path)

            if target_name:
                results.append(target_name)

    results.sort()

    return results


# -----------------------------------------------------------------------------
def get_all_target_verbs(proj_path, target_name):
    results = []

    target_verbs_list = f.find_files(
        os.path.join(
            proj_path,
            "targets",
            target_name,
            "verbs",
        ),
        "*.py",
    )

    if target_verbs_list:
        for verb_file in target_verbs_list:
            verb_name = os.path.basename(verb_file)
            verb_name = os.path.splitext(verb_name)[0]

            if verb_name:
                results.append(verb_name)

    results.sort()
    return results


# -----------------------------------------------------------------------------
def add_target_setup_common_args(
    run_args, target_name, target_config, arch, build_type
):
    run_args.append("-s:h")
    run_args.append("build_type={0}".format(get_build_type(build_type)))

    run_args.append("-s:h")
    run_args.append("arch={0}".format(arch["conan_arch"]))

    if "sdk" in arch:
        run_args.append("-s:h")
        run_args.append("os.sdk={0}".format(arch["sdk"]))

    run_args.append("-o")
    run_args.append("nativium_target={0}".format(target_name))

    run_args.append("-o")
    run_args.append("nativium_build_type={0}".format(build_type))

    run_args.append("-o")
    run_args.append("nativium_arch={0}".format(arch["arch"]))

    run_args.append("-o")
    run_args.append("nativium_project_name={0}".format(target_config["project_name"]))

    run_args.append("-o")
    run_args.append(
        "nativium_product_name={0}".format(
            target_config["product_name"] if "product_name" in target_config else ""
        )
    )

    run_args.append("-o")
    run_args.append("nativium_version={0}".format(target_config["version"]))

    run_args.append("-o")
    run_args.append(
        "nativium_version_code={0}".format(
            target_config["version_code"] if "version_code" in target_config else ""
        )
    )

    if "group" in arch:
        run_args.append("-o"),
        run_args.append("nativium_group={0}".format(arch["group"]))

    if "entrypoint" in target_config:
        run_args.append("-o"),
        run_args.append("nativium_entrypoint={0}".format(target_config["entrypoint"]))


# -----------------------------------------------------------------------------
def get_build_profile():
    if p.is_linux():
        return const.PROFILE_BUILD_LINUX
    elif p.is_windows():
        return const.PROFILE_BUILD_WINDOWS
    elif p.is_macos():
        return const.PROFILE_BUILD_MACOS
    else:
        return const.PROFILE_BUILD_DEFAULT


# -----------------------------------------------------------------------------
def get_build_type(build_type):
    # Debug: no optimization, asserts enabled, [custom debug (output) code enabled], debug info included in executable (so you can step through the code with a debugger and have address to source-file:line-number translation)
    # Release: high optimization level, no debug info, code or asserts
    # RelWithDebInfo: optimized, with debug info, but no debug (output) code or asserts
    # MinSizeRel: same as Release but optimizing for size rather than speed

    if not build_type:
        build_type = const.BUILD_TYPE_DEFAULT

    build_type = build_type.lower()

    if build_type == "debug":
        return "Debug"
    elif build_type == "release":
        return "Release"
    elif build_type == "rel_with_deb_info":
        return "RelWithDebInfo"
    elif build_type == "rel-with-deb-info":
        return "RelWithDebInfo"
    elif build_type == "release_with_debug_info":
        return "RelWithDebInfo"
    elif build_type == "release-with-debug-info":
        return "RelWithDebInfo"
    elif build_type == "relwithdebinfo":
        return "RelWithDebInfo"
    elif build_type == "min_size_rel":
        return "MinSizeRel"
    elif build_type == "min-size-rel":
        return "MinSizeRel"
    elif build_type == "min_size_release":
        return "MinSizeRel"
    elif build_type == "min-size-release":
        return "MinSizeRel"
    elif build_type == "minimum_size_release":
        return "MinSizeRel"
    elif build_type == "minimum-size-release":
        return "MinSizeRel"
    elif build_type == "minimize_size_release":
        return "MinSizeRel"
    elif build_type == "minimize-size-release":
        return "MinSizeRel"
    elif build_type == "minsizerel":
        return "MinSizeRel"
    else:
        l.e("Invalid build type: {0}".format(build_type))
