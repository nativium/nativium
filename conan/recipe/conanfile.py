import os
import sys

proj_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(proj_path)

from conan import ConanFile
from conan.tools.apple.apple import to_apple_arch
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import copy
from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.util import log as l

from core import const as c
from core import module as m


class TargetConan(ConanFile):
    name = "nativium"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "nativium_project_name": "ANY",
        "nativium_product_name": "ANY",
        "nativium_version": "ANY",
        "nativium_version_code": "ANY",
        "nativium_build_type": "ANY",
        "nativium_arch": "ANY",
        "nativium_target": "ANY",
        "nativium_group": "ANY",
        "nativium_entrypoint": "ANY",
        "nativium_code_coverage": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "nativium_project_name": "nativium",
        "nativium_product_name": "nativium",
        "nativium_version": "ANY",
        "nativium_version_code": "ANY",
        "nativium_build_type": "ANY",
        "nativium_arch": "ANY",
        "nativium_target": "ANY",
        "nativium_group": "",
        "nativium_entrypoint": "",
        "nativium_code_coverage": False,
    }
    generators = "CMakeToolchain", "CMakeDeps"

    # -----------------------------------------------------------------------------
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    # -----------------------------------------------------------------------------
    def layout(self):
        generators_dir = os.path.join(
            "build",
            self.options.get_safe("nativium_target").value,
            self.options.get_safe("nativium_build_type").value,
            self.options.get_safe("nativium_arch").value,
            "conan",
            "generators",
        )

        build_dir = os.path.join(
            "build",
            self.options.get_safe("nativium_target").value,
            self.options.get_safe("nativium_build_type").value,
            self.options.get_safe("nativium_arch").value,
            "target",
        )

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
        # toolchain
        tc = CMakeToolchain(self)

        if self.settings.os in c.APPLE_OS_LIST:
            os_version = self.get_setting("os.version")
            tc.cache_variables["NATIVIUM_DEPLOYMENT_TARGET"] = os_version

        if self.settings.os in c.APPLE_MOBILE_OS_LIST:
            apple_arch = to_apple_arch(self.get_setting("arch"))
            tc.cache_variables["NATIVIUM_PLATFORM_ARCH"] = apple_arch

        tc.cache_variables["CMAKE_BUILD_TYPE"] = self.settings.build_type
        tc.cache_variables["NATIVIUM_PROJECT_NAME"] = self.get_opt("nativium_project_name")
        tc.cache_variables["NATIVIUM_PRODUCT_NAME"] = self.get_opt("nativium_product_name")
        tc.cache_variables["NATIVIUM_TARGET"] = self.get_opt("nativium_target")
        tc.cache_variables["NATIVIUM_BUILD_TYPE"] = self.get_opt("nativium_build_type")
        tc.cache_variables["NATIVIUM_ARCH"] = self.get_opt("nativium_arch")
        tc.cache_variables["NATIVIUM_GROUP"] = self.get_opt("nativium_group")
        tc.cache_variables["NATIVIUM_VERSION"] = self.get_opt("nativium_version")
        tc.cache_variables["NATIVIUM_VERSION_CODE"] = self.get_opt("nativium_version_code")
        tc.cache_variables["NATIVIUM_ENTRYPOINT"] = self.get_opt("nativium_entrypoint")
        tc.cache_variables["NATIVIUM_CODE_COVERAGE"] = self.get_opt("nativium_code_coverage")

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
    def get_opt(self, key):
        return self.options.get_safe(key).value

    # -----------------------------------------------------------------------------
    def get_setting(self, key):
        return self.settings.get_safe(key).value
