import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
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
    param_dry_run = ls.list_has_value(params["args"], "--dry-run")

    if param_dry_run:
        l.i("Running in dry mode...")

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

                        # variables
                        build_dir = os.path.join(
                            proj_path,
                            "build",
                            target_name,
                            build_type,
                            arch["group"],
                            arch["arch"],
                            "target",
                        )

                        clean_build_dir = True

                        if param_dry_run and os.path.isdir(build_dir):
                            clean_build_dir = False

                        if clean_build_dir:
                            # clean
                            f.recreate_dir(build_dir)

                        # prepare build profile
                        build_profile = target.get_build_profile()

                        if build_profile != "default":
                            build_profile = os.path.join(
                                proj_path, "conan", "profiles", build_profile
                            )

                        # build
                        run_args = [
                            "conan",
                            "build",
                            os.path.join(
                                proj_path,
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
                        ]

                        # extra run args
                        if "enable_bitcode" in arch:
                            run_args.append("-c:h")
                            run_args.append(
                                "tools.apple:enable_bitcode={0}".format(
                                    arch["enable_bitcode"]
                                )
                            )

                        if "enable_arc" in arch:
                            run_args.append("-c:h")
                            run_args.append(
                                "tools.apple:enable_arc={0}".format(arch["enable_arc"])
                            )

                        if "enable_visibility" in arch:
                            run_args.append("-c:h")
                            run_args.append(
                                "tools.apple:enable_visibility={0}".format(
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

                        target.add_target_setup_common_args(
                            run_args, target_name, target_config, arch, build_type
                        )

                        # final run args
                        run_args.append("--build=missing")
                        run_args.append("--update")

                        r.run(run_args, cwd=build_dir)

                        # find correct info plist file
                        plist_path1 = os.path.join(
                            proj_path,
                            "build",
                            target_name,
                            build_type,
                            arch["group"],
                            arch["arch"],
                            "target",
                            "lib",
                            "{0}.framework".format(target_config["project_name"]),
                            "Info.plist",
                        )

                        plist_path2 = os.path.join(
                            proj_path,
                            "build",
                            target_name,
                            build_type,
                            arch["group"],
                            arch["arch"],
                            "target",
                            "lib",
                            "{0}.framework".format(target_config["project_name"]),
                            "Versions",
                            "A",
                            "Resources",
                            "Info.plist",
                        )

                        plist_path = ""

                        if os.path.exists(plist_path1):
                            plist_path = plist_path1

                        if os.path.exists(plist_path2):
                            plist_path = plist_path2

                        # add minimum version inside plist
                        r.run(
                            [
                                "plutil",
                                "-replace",
                                "MinimumOSVersion",
                                "-string",
                                arch["min_version"],
                                plist_path,
                            ],
                            cwd=proj_path,
                        )

                        # add supported platform inside plist
                        r.run(
                            [
                                "plutil",
                                "-replace",
                                "CFBundleSupportedPlatforms",
                                "-json",
                                '[ "{0}" ]'.format(arch["supported_platform"]),
                                plist_path,
                            ],
                            cwd=proj_path,
                        )

                        # modules
                        support_modules_dir = os.path.join(
                            proj_path,
                            "targets",
                            target_name,
                            "support",
                            "modules",
                        )

                        modules_dir = os.path.join(
                            proj_path,
                            "build",
                            target_name,
                            build_type,
                            arch["group"],
                            arch["arch"],
                            "target",
                            "lib",
                            "{0}.framework".format(target_config["project_name"]),
                            "Modules",
                        )

                        f.recreate_dir(modules_dir)

                        f.copy_file(
                            os.path.join(support_modules_dir, "module.modulemap"),
                            os.path.join(modules_dir, "module.modulemap"),
                        )

                        # umbrella header
                        build_headers_dir = os.path.join(
                            proj_path,
                            "build",
                            target_name,
                            build_type,
                            arch["group"],
                            arch["arch"],
                            "target",
                            "lib",
                            "{0}.framework".format(target_config["project_name"]),
                            "Headers",
                        )

                        header_files = f.find_files(
                            build_headers_dir, "*.h", recursive=True
                        )

                        content = f.get_file_contents(
                            os.path.join(support_modules_dir, "umbrella-header.h")
                        )

                        for header_file in header_files:
                            header_file = header_file.replace(
                                build_headers_dir + "/", ""
                            )

                            content = content + '#import "{0}"\n'.format(header_file)

                        if len(content) > 0:
                            umbrella_file = os.path.join(
                                build_headers_dir, target_config["umbrella_header"]
                            )

                            f.copy_file(
                                os.path.join(support_modules_dir, "umbrella-header.h"),
                                umbrella_file,
                            )

                            f.set_file_content(umbrella_file, content)
                        else:
                            l.e(
                                "{0}".format(
                                    "File not generated because framework headers is empty"
                                )
                            )

                l.ok()

            else:
                l.e('Group list for "{0}" is invalid or empty'.format(target_name))
        else:
            l.e('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
