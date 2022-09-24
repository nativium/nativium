import os

from pygemstones.io import file as f
from pygemstones.system import platform as p
from pygemstones.system import runner as r
from pygemstones.util import log as l

from core import const, module, util
from targets.android.config import target_config as config


# -----------------------------------------------------------------------------
def run(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    archs = util.get_parsed_arch_list(params, target_config)
    build_types = util.get_parsed_build_type_list(params, target_config)
    android_module_name = "library"

    l.i("Creating AAR library...")

    if archs and len(archs) > 0:
        if build_types and len(build_types) > 0:
            for build_type in build_types:
                l.i("Creating AAR library for: {0}...".format(build_type))

                build_dir = os.path.join(proj_path, "build", target_name, build_type)

                # copy library project template
                android_library_build_dir = os.path.join(build_dir, "aar")

                f.recreate_dir(android_library_build_dir)

                android_project_dir = os.path.join(
                    proj_path,
                    "targets",
                    target_name,
                    "support",
                    "android-aar-project",
                )

                f.copy_dir(
                    android_project_dir,
                    android_library_build_dir,
                    symlinks=True,
                )

                # replace data
                build_gradle_file = os.path.join(
                    android_library_build_dir,
                    "library",
                    "build.gradle",
                )

                f.replace_in_file(
                    build_gradle_file, "{VERSION}", target_config["version"]
                )

                f.replace_in_file(
                    build_gradle_file, "{VERSION_CODE}", target_config["version_code"]
                )

                # copy support lib files
                gluecode_support_lib_dir = os.path.join(
                    proj_path,
                    "modules",
                    "support-lib",
                )

                f.copy_all(
                    os.path.join(gluecode_support_lib_dir, "djinni", "java"),
                    os.path.join(
                        android_library_build_dir,
                        android_module_name,
                        "src",
                        "main",
                        "java",
                    ),
                )

                # copy entrypoint loader
                if target_config["entrypoint"] == "loader":
                    f.copy_all(
                        os.path.join(gluecode_support_lib_dir, "nativium", "java"),
                        os.path.join(
                            android_library_build_dir,
                            android_module_name,
                            "src",
                            "main",
                            "java",
                        ),
                    )

                # copy all modules glue code files
                modules_dir = os.path.join(
                    proj_path,
                    "modules",
                )

                modules = module.get_list(proj_path)

                for m in modules:
                    module_dir = os.path.join(
                        modules_dir,
                        m,
                        "gluecode",
                        "generated-src",
                        "java",
                    )

                    if f.dir_exists(module_dir):
                        f.copy_all(
                            module_dir,
                            os.path.join(
                                android_library_build_dir,
                                android_module_name,
                                "src",
                                "main",
                                "java",
                            ),
                        )

                # copy all modules implementation files
                modules_dir = os.path.join(
                    proj_path,
                    "modules",
                )

                modules = module.get_list(proj_path)

                for m in modules:
                    module_dir = os.path.join(
                        modules_dir,
                        m,
                        "implementation",
                        "java",
                    )

                    if f.dir_exists(module_dir):
                        f.copy_all(
                            module_dir,
                            os.path.join(
                                android_library_build_dir,
                                android_module_name,
                                "src",
                                "main",
                                "java",
                            ),
                        )

                # copy all native libraries
                for arch in archs:
                    compiled_arch_dir = os.path.join(
                        build_dir,
                        arch["arch"],
                        "target",
                        "lib",
                    )

                    target_arch_dir = os.path.join(
                        android_library_build_dir,
                        "library",
                        "src",
                        "main",
                        "jniLibs",
                        arch["arch"],
                    )

                    f.copy_all(compiled_arch_dir, target_arch_dir)

                # build aar
                android_module_dir = os.path.join(
                    android_library_build_dir,
                    android_module_name,
                )

                if p.is_windows():
                    os.chdir(android_module_dir)

                    run_args = [
                        os.path.join("..", "gradlew.bat"),
                        "bundle{0}Aar".format(get_build_type(build_type)),
                    ]
                else:
                    run_args = [
                        os.path.join("..", "gradlew"),
                        "bundle{0}Aar".format(get_build_type(build_type)),
                    ]

                r.run(run_args, cwd=android_module_dir)

                # copy files
                arr_dir = os.path.join(
                    android_library_build_dir,
                    android_module_name,
                    "build",
                    "outputs",
                    "aar",
                )

                dist_dir = os.path.join(
                    proj_path, "dist", target_name, get_build_type_dir(build_type)
                )

                f.remove_dir(dist_dir)

                f.copy_all(arr_dir, dist_dir)

            l.ok()
        else:
            l.i('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.i('Arch list for "{0}" is invalid or empty'.format(target_name))


# -----------------------------------------------------------------------------
def get_build_type(build_type):
    if not build_type:
        build_type = const.BUILD_TYPE_DEFAULT

    build_type = build_type.lower()

    if build_type == "debug":
        return "Debug"
    elif build_type.startswith("rel"):
        return "Release"
    else:
        l.e("Invalid build type: {0}".format(build_type))


# -----------------------------------------------------------------------------
def get_build_type_dir(build_type):
    build_type = build_type.lower()

    if build_type == "debug":
        return "debug"
    elif build_type.startswith("rel"):
        return "release"
    else:
        l.e("Invalid build type: {0}".format(build_type))
