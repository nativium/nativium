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
def add_target_prepare_common_args(
    run_args, target_name, target_config, arch, build_type
):
    run_args.append("-s:h")
    run_args.append("build_type={0}".format(build_type))

    run_args.append("-s:h")
    run_args.append("arch={0}".format(arch["conan_arch"]))

    run_args.append("-o")
    run_args.append("nativium_target={0}".format(target_name))

    run_args.append("-o")
    run_args.append("nativium_arch={0}".format(arch["conan_arch"]))

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
