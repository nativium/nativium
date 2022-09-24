import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.util import log as l

from core import const, target, util
from targets.ios.config import target_config as config


# -----------------------------------------------------------------------------
def run(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    archs = util.get_parsed_arch_list(params, target_config)
    build_types = util.get_parsed_build_type_list(params, target_config)
    groups = util.get_parsed_group_list(params, target_config)

    if archs and len(archs) > 0:
        if build_types and len(build_types) > 0:
            if groups and len(groups) > 0:
                for arch in archs:
                    for build_type in build_types:
                        if arch["group"] not in groups:
                            continue

                        l.i(
                            "Building for: {0}/{1}/{2}...".format(
                                arch["arch"], build_type, arch["group"]
                            )
                        )

                        # conan install
                        build_dir = os.path.join(
                            proj_path,
                            "build",
                            target_name,
                            build_type,
                            arch["group"],
                            arch["arch"],
                            "conan",
                        )

                        f.recreate_dir(build_dir)

                        build_profile = target.get_build_profile()

                        if build_profile != "default":
                            build_profile = os.path.join(
                                proj_path, "conan", "profiles", build_profile
                            )

                        run_args = [
                            "conan",
                            "install",
                            os.path.join(
                                proj_path,
                                "conan",
                                "recipe",
                                const.FILE_NAME_CONANFILE_PY,
                            ),
                            "-pr:b",
                            build_profile,
                            "-pr:h",
                            os.path.join(
                                proj_path, "conan", "profiles", arch["conan_profile"]
                            ),
                            "-s:h",
                            "os.version={0}".format(arch["min_version"]),
                            "-c",
                            'tools.cmake.cmaketoolchain:generator="Xcode"',
                        ]

                        target.add_target_setup_common_args(
                            run_args, target_name, target_config, arch, build_type
                        )

                        # extra run args
                        if "enable_bitcode" in arch:
                            run_args.append("-o:h")
                            run_args.append(
                                "darwin-toolchain:enable_bitcode={0}".format(
                                    arch["enable_bitcode"]
                                )
                            )

                        if "enable_arc" in arch:
                            run_args.append("-o:h")
                            run_args.append(
                                "darwin-toolchain:enable_arc={0}".format(
                                    arch["enable_arc"]
                                )
                            )

                        if "enable_visibility" in arch:
                            run_args.append("-o:h")
                            run_args.append(
                                "darwin-toolchain:enable_visibility={0}".format(
                                    arch["enable_visibility"]
                                )
                            )

                        if "subsystem_ios_version" in arch:
                            run_args.append("-s:h")
                            run_args.append(
                                "os.subsystem.ios_version={0}".format(
                                    arch["subsystem_ios_version"]
                                )
                            )

                        # final run args
                        run_args.append("--build=missing")
                        run_args.append("--update")

                        # execute
                        r.run(run_args, cwd=build_dir)

                l.ok()

            else:
                l.e('Group list for "{0}" is invalid or empty'.format(target_name))
        else:
            l.e('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
