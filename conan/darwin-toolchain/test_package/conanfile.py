import os

from conan.tools.cmake import CMake, cmake_layout

from conan import ConanFile


class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    # VirtualBuildEnv and VirtualRunEnv can be avoided if "tools.env.virtualenv:auto_use" is defined
    # (it will be defined in Conan 2.0)
    generators = "CMakeDeps", "CMakeToolchain", "VirtualBuildEnv", "VirtualRunEnv"
    apply_env = False
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if self.settings.os != "Macos":
            # Ensure it fails
            try:
                self.run_tests()
            except:
                pass
            else:
                raise Exception("Cross building failed!")
        else:
            self.run_tests()

    def run_tests(self):
        cmd = os.path.join(self.cpp.build.bindirs[0], "example")
        self.run(cmd, env="conanrun")
