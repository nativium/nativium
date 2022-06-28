import os

from pygemstones.system import env as e
from pygemstones.type import list as l

from core import const


# -----------------------------------------------------------------------------
def get_version(params, config):
    version = l.get_arg_list_value(params["args"], "--version")

    if not version or len(version) == 0:
        proj_path = params["proj_path"]
        target_name = params["target_name"]
        target_config = config.run(proj_path, target_name, params)
        version = target_config["version"]

    return version


# -----------------------------------------------------------------------------
def remove_sdkroot_from_env():
    if const.REMOVE_SDKROOT_FROM_ENV:
        e.remove_var("SDKROOT")


# -----------------------------------------------------------------------------
def get_parsed_arch_list(params, target_config):
    param_archs = l.get_arg_list_values(params["args"], "--arch")
    target_archs = target_config["archs"] if "archs" in target_config else None

    if not param_archs:
        return target_archs

    if not target_archs:
        return None

    archs = []

    for param_arch in param_archs:
        for target_arch in target_archs:
            arch_name = target_arch["arch"]

            if arch_name.lower() == param_arch.lower():
                archs.append(target_arch)

    return archs


# -----------------------------------------------------------------------------
def get_parsed_build_type_list(params, target_config):
    param_build_types = l.get_arg_list_values(params["args"], "--build")
    target_build_types = (
        target_config["build_types"] if "build_types" in target_config else None
    )

    if not param_build_types:
        return target_build_types

    if not target_build_types:
        return None

    build_types = []

    for param_build_type in param_build_types:
        for target_build_type in target_build_types:
            if param_build_type.lower() == target_build_type.lower():
                build_types.append(target_build_type)

    return build_types
