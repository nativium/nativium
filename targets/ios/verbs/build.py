import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
from pygemstones.util import log as l

from core import const, util
from targets.ios.config import target as config


# -----------------------------------------------------------------------------
def run(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    archs = util.get_parsed_arch_list(params, target_config)
    build_types = util.get_parsed_build_type_list(params, target_config)
    groups = util.get_parsed_group_list(params, target_config)
    install_headers = target_config["install_headers"]
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

                        # build
                        run_args = [
                            "conan",
                            "build",
                            os.path.join(
                                proj_path,
                                "conan",
                                "recipe",
                                const.FILE_NAME_CONANFILE_PY,
                            ),
                            "--source-folder",
                            proj_path,
                            "--build-folder",
                            os.path.join(
                                proj_path,
                                "build",
                                target_name,
                                build_type,
                                arch["group"],
                                arch["arch"],
                                "target",
                            ),
                            "--install-folder",
                            os.path.join(
                                proj_path,
                                "build",
                                target_name,
                                build_type,
                                arch["group"],
                                arch["arch"],
                                "conan",
                            ),
                        ]

                        if param_dry_run:
                            run_args.append("--build")

                        r.run(run_args, build_dir)

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
                            proj_path,
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
                            proj_path,
                        )

                        # headers
                        dist_headers_dir = os.path.join(
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

                        f.create_dir(dist_headers_dir)

                        if install_headers:
                            for header in install_headers:
                                source_header_dir = os.path.join(
                                    proj_path, header["path"]
                                )

                                if header["type"] == "dir":
                                    f.copy_dir(
                                        source_header_dir,
                                        dist_headers_dir,
                                        ignore_file=_header_ignore_list,
                                        symlinks=True,
                                    )
                                else:
                                    l.e(
                                        "Invalid type for install header list for {0}".format(
                                            target_name
                                        )
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


# -----------------------------------------------------------------------------
def _header_ignore_list(filename):
    return not filename.lower().endswith(".h") or "+Private" in filename
