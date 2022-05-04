import os
import sys

proj_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(proj_path)

from conans import CMake, ConanFile, tools
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
        "nativium_arch": "ANY",
        "nativium_target": "ANY",
        "nativium_group": "ANY",
        "nativium_entrypoint": "ANY",
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "nativium_project_name": "nativium",
        "nativium_product_name": "nativium",
        "nativium_version": "ANY",
        "nativium_version_code": "ANY",
        "nativium_arch": "ANY",
        "nativium_target": "ANY",
        "nativium_group": "",
        "nativium_entrypoint": "",
    }
    exports_sources = "*"
    generators = "cmake"

    # -----------------------------------------------------------------------------
    def build(self):
        # initialize cmake
        if self.settings.os in c.APPLE_OS_LIST:
            cmake = CMake(self, generator="Xcode")

            cmake.definitions["NATIVIUM_DEPLOYMENT_TARGET"] = self.settings.get_safe(
                "os.version"
            )
        elif self.settings.os == "Android":
            cmake = CMake(self, generator="Unix Makefiles")
        else:
            cmake = CMake(self)

        if self.settings.os in c.APPLE_MOBILE_OS_LIST:
            cmake.definitions["NATIVIUM_PLATFORM_ARCH"] = tools.to_apple_arch(
                self.options.get_safe("nativium_arch"),
            )

        # definitions
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["NATIVIUM_PROJECT_NAME"] = self.options.get_safe(
            "nativium_project_name"
        )
        cmake.definitions["NATIVIUM_PRODUCT_NAME"] = self.options.get_safe(
            "nativium_product_name"
        )
        cmake.definitions["NATIVIUM_ARCH"] = self.options.get_safe("nativium_arch")
        cmake.definitions["NATIVIUM_GROUP"] = self.options.get_safe("nativium_group")
        cmake.definitions["NATIVIUM_TARGET"] = self.options.get_safe("nativium_target")
        cmake.definitions["NATIVIUM_BUILD_TYPE"] = self.settings.build_type

        cmake.definitions["NATIVIUM_VERSION"] = self.options.get_safe(
            "nativium_version"
        )

        cmake.definitions["NATIVIUM_VERSION_CODE"] = self.options.get_safe(
            "nativium_version_code"
        )

        cmake.definitions["NATIVIUM_ENTRYPOINT"] = self.options.get_safe(
            "nativium_entrypoint"
        )

        # configure and build
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
    def imports(self):
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", src="lib")
            self.copy("*.dylib", dst="bin", src="lib")
