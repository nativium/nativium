from conan.errors import ConanInvalidConfiguration
from conan.tools.apple import XCRun, is_apple_os

from conan import ConanFile

required_conan_version = ">=2.0.0"


class DarwinToolchainConan(ConanFile):
    name = "darwin-toolchain"
    version = "1.0.0"
    license = "MIT"
    settings = "os", "arch", "build_type", "compiler"
    options = {
        "enable_bitcode": [True, False, None],
        "enable_arc": [True, False, None],
        "enable_visibility": [True, False, None],
    }
    default_options = {
        "enable_bitcode": None,
        "enable_arc": None,
        "enable_visibility": None,
    }
    description = "Darwin toolchain to (cross) compile macOS/iOS/watchOS/tvOS"
    url = "https://github.com/nativium/nativium"

    # In Conan 2.0, build_policy="missing" is replaced by package_id_mode
    package_id_mode = "recipe_revision_mode"

    def config_options(self):
        if self.settings.os == "Macos":
            self.options.enable_bitcode = None

        if self.settings.os == "watchOS":
            self.options.enable_bitcode = True

        if self.settings.os == "tvOS":
            self.options.enable_bitcode = True

    def validate(self):
        if self.settings.os_build != "Macos":
            raise ConanInvalidConfiguration("Build machine must be Macos")

        if not is_apple_os(self):
            raise ConanInvalidConfiguration("OS must be an Apple OS")

        if self.settings.os in ["watchOS", "tvOS"] and not self.options.enable_bitcode:
            raise ConanInvalidConfiguration("Bitcode is required on watchOS/tvOS")

        if self.settings.os == "Macos" and self.settings.arch not in [
            "x86",
            "x86_64",
            "armv8",
        ]:
            raise ConanInvalidConfiguration(
                "macOS: Only supported archs: [x86, x86_64, armv8]"
            )

        if self.settings.os == "iOS" and self.settings.arch not in [
            "armv7",
            "armv7s",
            "armv8",
            "armv8.3",
            "x86",
            "x86_64",
        ]:
            raise ConanInvalidConfiguration(
                "iOS: Only supported archs: [armv7, armv7s, armv8, armv8.3, x86, x86_64]"
            )

        if self.settings.os == "tvOS" and self.settings.arch not in ["armv8", "x86_64"]:
            raise ConanInvalidConfiguration(
                "tvOS: Only supported archs: [armv8, x86_64]"
            )

        if self.settings.os == "watchOS" and self.settings.arch not in [
            "armv7k",
            "armv8_32",
            "x86",
            "x86_64",
        ]:
            raise ConanInvalidConfiguration(
                "watchOS: Only supported archs: [armv7k, armv8_32, x86, x86_64]"
            )

    def generate(self):
        # Sysroot and Settings
        xcrun = XCRun(self, use_settings_target=True)
        sysroot = xcrun.sdk_path
        settings_target = xcrun.settings

        # Variables for CMake
        self.output.info(f"Setting SDKROOT to {sysroot}")

        # Set variables as part of the conanbuild.sh/bat file
        # Bitcode
        if self.options.enable_bitcode is None or self.options.enable_bitcode == "None":
            self.output.info("Bitcode enabled: IGNORED")
        else:
            if self.options.enable_bitcode:
                self.output.info("Bitcode enabled: YES")
                self.conf.define("tools.apple:enable_bitcode", True)

                build_type = settings_target.get_safe("build_type")
                if build_type.lower() == "debug":
                    self.conf.define("tools.apple:bitcode_mode", "marker")
                else:
                    self.conf.define("tools.apple:bitcode_mode", "bitcode")
            else:
                self.output.info("Bitcode enabled: NO")
                self.conf.define("tools.apple:enable_bitcode", False)

        # ARC
        if self.options.enable_arc is None or self.options.enable_arc == "None":
            self.output.info("ObjC ARC enabled: IGNORED")
        else:
            if self.options.enable_arc:
                self.output.info("ObjC ARC enabled: YES")
                self.conf.define("tools.apple:enable_arc", True)
            else:
                self.output.info("ObjC ARC enabled: NO")
                self.conf.define("tools.apple:enable_arc", False)

        # Visibility
        if (
            self.options.enable_visibility is None
            or self.options.enable_visibility == "None"
        ):
            self.output.info("Visibility enabled: IGNORED")
        else:
            if self.options.enable_visibility:
                self.output.info("Visibility enabled: YES")
                self.conf.define("tools.apple:enable_visibility", True)
            else:
                self.output.info("Visibility enabled: NO")
                self.conf.define("tools.apple:enable_visibility", False)

        # Set the SDK path
        self.conf.define("tools.apple:sdk_path", sysroot)

    def package_id(self):
        self.info.clear()

    def package_info(self):
        # In Conan 2.0, we use the cpp_info and conf objects
        xcrun = XCRun(self, use_settings_target=True)
        sysroot = xcrun.sdk_path

        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.frameworkdirs = []
        self.cpp_info.builddirs = []

        # Set the sysroot in cpp_info
        self.cpp_info.sysroot = sysroot

        # Common flags
        common_flags = [f"-isysroot{sysroot}"]

        # Apply bitcode flags
        if self.options.enable_bitcode and self.options.enable_bitcode != "None":
            if self.settings.build_type and self.settings.build_type.lower() == "debug":
                common_flags.append("-fembed-bitcode-marker")
            else:
                common_flags.append("-fembed-bitcode")

        # Apply ARC flags
        if self.options.enable_arc and self.options.enable_arc != "None":
            common_flags.append("-fobjc-arc" if self.options.enable_arc else "-fno-objc-arc")

        # Apply visibility flags
        if self.options.enable_visibility and self.options.enable_visibility != "None":
            common_flags.append("-fvisibility=default" if self.options.enable_visibility else "-fvisibility=hidden")

        # Set flags in cpp_info
        self.cpp_info.cflags.extend(common_flags)
        self.cpp_info.cxxflags.extend(common_flags)
        self.cpp_info.sharedlinkflags.extend(common_flags)
        self.cpp_info.exelinkflags.extend(common_flags)
