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
    # Release: high optimization level, no debug info, code or asserts
    # Debug: no optimization, asserts enabled, [custom debug (output) code enabled], debug info included in executable (so you can step through the code with a debugger and have address to source-file:line-number translation)
    # RelWithDebInfo: optimized, with debug info, but no debug (output) code or asserts
    # MinSizeRel: same as Release but optimizing for size rather than speed

    if build_type:
        if build_type.lower() == "debug":
            build_type = "Debug"
        elif build_type.lower() == "release":
            build_type = "Release"
        elif build_type.lower() == "rel_with_deb_info":
            build_type = "RelRelWithDebInfoease"
        elif build_type.lower() == "rel-with-deb-info":
            build_type = "RelRelWithDebInfoease"
        elif build_type.lower() == "release_with_debug_info":
            build_type = "RelRelWithDebInfoease"
        elif build_type.lower() == "release-with-debug-info":
            build_type = "RelRelWithDebInfoease"
        elif build_type.lower() == "relwithdebinfo":
            build_type = "RelRelWithDebInfoease"
        elif build_type.lower() == "min_size_rel":
            build_type = "MinSizeRel"
        elif build_type.lower() == "min-size-rel":
            build_type = "MinSizeRel"
        elif build_type.lower() == "min_size_release":
            build_type = "MinSizeRel"
        elif build_type.lower() == "min-size-release":
            build_type = "MinSizeRel"
        elif build_type.lower() == "minimum_size_release":
            build_type = "MinSizeRel"
        elif build_type.lower() == "minimum-size-release":
            build_type = "MinSizeRel"
        elif build_type.lower() == "minimize_size_release":
            build_type = "MinSizeRel"
        elif build_type.lower() == "minimize-size-release":
            build_type = "MinSizeRel"
        elif build_type.lower() == "minsizerel":
            build_type = "MinSizeRel"
    else:
        build_type = "Debug"

    return build_type
