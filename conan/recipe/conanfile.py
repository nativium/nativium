import os
import sys

from conan.tools.apple import is_apple_os, to_apple_arch
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy
from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.util import log as l

from conan import ConanFile

proj_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(proj_path)

from core import const as c
from core import module as m


class TargetConan(ConanFile):
    name = "nativium"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "nativium_project_name": [None, "ANY"],
        "nativium_product_name": [None, "ANY"],
        "nativium_version": [None, "ANY"],
        "nativium_version_code": [None, "ANY"],
        "nativium_build_type": [None, "ANY"],
        "nativium_arch": [None, "ANY"],
        "nativium_target": [None, "ANY"],
        "nativium_group": [None, "ANY"],
        "nativium_entrypoint": [None, "ANY"],
        "nativium_code_coverage": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "nativium_project_name": "nativium",
        "nativium_product_name": "nativium",
        "nativium_version": None,
        "nativium_version_code": None,
        "nativium_build_type": None,
        "nativium_arch": None,
        "nativium_target": None,
        "nativium_group": "",
        "nativium_entrypoint": "",
        "nativium_code_coverage": False,
    }

    # -----------------------------------------------------------------------------
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    # -----------------------------------------------------------------------------
    def layout(self):
        # generators
        generators_dir = os.path.join(
            "build",
            str(self.get_options("nativium_target")),
            str(self.get_options("nativium_build_type")),
        )

        if self.get_options("nativium_group"):
            generators_dir = os.path.join(
                generators_dir,
                str(self.get_options("nativium_group")),
            )

        generators_dir = os.path.join(
            generators_dir,
            str(self.get_options("nativium_arch")),
            "conan",
            "generators",
        )

        # build dir
        build_dir = os.path.join(
            "build",
            str(self.get_options("nativium_target")),
            str(self.get_options("nativium_build_type")),
        )

        if self.get_options("nativium_group"):
            build_dir = os.path.join(
                build_dir,
                str(self.get_options("nativium_group")),
            )

        build_dir = os.path.join(
            build_dir,
            str(self.get_options("nativium_arch")),
            "target",
        )

        # others
        self.folders.root = os.path.join("..", "..")
        self.folders.source = "."
        self.folders.build = build_dir
        self.folders.generators = generators_dir

    # -----------------------------------------------------------------------------
    def export_sources(self):
        copy(
            self,
            "CMakeLists.txt",
            os.path.join(self.recipe_folder, os.path.join("..", "..")),
            self.export_sources_folder,
        )

    # -----------------------------------------------------------------------------
    def generate(self):
        # generator
        generator = None

        if is_apple_os(self):
            generator = "Xcode"

        # toolchain
        tc = CMakeToolchain(self, generator=generator)

        # apple specific
        if is_apple_os(self):
            os_version = str(self.get_settings("os.version"))
            tc.variables["NATIVIUM_DEPLOYMENT_TARGET"] = os_version

            apple_arch = str(to_apple_arch(self))
            tc.variables["NATIVIUM_PLATFORM_ARCH"] = apple_arch

        # nativium specific
        tc.variables["NATIVIUM_PROJECT_NAME"] = str(
            self.get_options("nativium_project_name"),
        )

        tc.variables["NATIVIUM_PRODUCT_NAME"] = str(
            self.get_options("nativium_product_name"),
        )

        tc.variables["NATIVIUM_TARGET"] = str(
            self.get_options("nativium_target"),
        )

        tc.variables["NATIVIUM_BUILD_TYPE"] = str(
            self.get_options("nativium_build_type"),
        )

        tc.variables["NATIVIUM_ARCH"] = str(
            self.get_options("nativium_arch"),
        )

        tc.variables["NATIVIUM_GROUP"] = str(
            self.get_options("nativium_group"),
        )

        tc.variables["NATIVIUM_VERSION"] = str(
            self.get_options("nativium_version"),
        )

        tc.variables["NATIVIUM_VERSION_CODE"] = str(
            self.get_options("nativium_version_code"),
        )

        tc.variables["NATIVIUM_ENTRYPOINT"] = str(
            self.get_options("nativium_entrypoint"),
        )

        tc.variables["NATIVIUM_CODE_COVERAGE"] = bool(
            self.get_options("nativium_code_coverage")
        )

        # general
        tc.variables["CMAKE_BUILD_TYPE"] = str(
            self.settings.build_type,
        )

        tc.generate()

        # dependencies
        deps = CMakeDeps(self)
        deps.generate()

    # -----------------------------------------------------------------------------
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    # -----------------------------------------------------------------------------
    def configure(self):
        # extend from modules
        module_list = m.get_list(proj_path)
        modules_path = os.path.join(proj_path, "modules")

        for module_name in module_list:
            module_config_path = os.path.join(modules_path, module_name, "config")
            module_config_file = os.path.join(module_config_path, "module_conan.py")

            if f.file_exists(module_config_file):
                l.i(
                    "Nativium: Extending conan configuration with module {0}".format(
                        module_name
                    )
                )

                params = {
                    "conanfile": self,
                }

                r.run_external(
                    path=module_config_path,
                    module_name="module_conan",
                    command_name="configure",
                    command_params=params,
                    show_log=False,
                    show_error_log=True,
                    throw_error=True,
                )

        # extend from target
        target_name = str(self.options.get_safe("nativium_target"))
        targets_path = os.path.join(proj_path, "targets")
        target_config_path = os.path.join(targets_path, target_name, "config")
        target_config_file = os.path.join(target_config_path, "target_conan.py")

        if f.file_exists(target_config_file):
            l.i(
                "Nativium: Extending conan configuration with target {0}".format(
                    target_name
                )
            )

            params = {
                "conanfile": self,
            }

            r.run_external(
                path=target_config_path,
                module_name="target_conan",
                command_name="configure",
                command_params=params,
                show_log=False,
                show_error_log=True,
                throw_error=True,
            )

    # -----------------------------------------------------------------------------
    def requirements(self):
        # extend from modules
        module_list = m.get_list(proj_path)
        modules_path = os.path.join(proj_path, "modules")

        for module_name in module_list:
            module_config_path = os.path.join(modules_path, module_name, "config")
            module_config_file = os.path.join(module_config_path, "module_conan.py")

            if f.file_exists(module_config_file):
                l.i(
                    "Nativium: Extending conan requirements with module {0}".format(
                        module_name
                    )
                )

                params = {
                    "conanfile": self,
                }

                r.run_external(
                    path=module_config_path,
                    module_name="module_conan",
                    command_name="requirements",
                    command_params=params,
                    show_log=False,
                    show_error_log=True,
                    throw_error=True,
                )

        # extend from target
        target_name = str(self.options.get_safe("nativium_target"))
        targets_path = os.path.join(proj_path, "targets")
        target_config_path = os.path.join(targets_path, target_name, "config")
        target_config_file = os.path.join(target_config_path, "target_conan.py")

        if f.file_exists(target_config_file):
            l.i(
                "Nativium: Extending conan requirements with target {0}".format(
                    target_name
                )
            )

            params = {
                "conanfile": self,
            }

            r.run_external(
                path=target_config_path,
                module_name="target_conan",
                command_name="requirements",
                command_params=params,
                show_log=False,
                show_error_log=True,
                throw_error=True,
            )

    # -----------------------------------------------------------------------------
    def package(self):
        cmake = CMake(self)
        cmake.install()

    # -----------------------------------------------------------------------------
    def get_options(self, key):
        return self.options.get_safe(key)

    # -----------------------------------------------------------------------------
    def get_settings(self, key):
        return self.settings.get_safe(key)
