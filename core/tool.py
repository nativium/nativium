import os
import subprocess

from pygemstones.io import file as f
from pygemstones.system import platform as p
from pygemstones.util import log as l


# -----------------------------------------------------------------------------
def check_tool_gradlew(params, name):
    """Checks if gradlew exists."""
    proj_path = params["proj_path"]
    path = os.path.join(proj_path, "apps", "android", name)

    gradle_tool = os.path.join(path, "gradlew")

    if p.is_windows():
        gradle_tool = gradle_tool + ".bat"

    if not f.file_exists(gradle_tool):
        l.e("Gradle script don't exists: {0}".format(gradle_tool))

    return gradle_tool


# -----------------------------------------------------------------------------
def check_tool_adb():
    """Checks if invoking supplied adb binary works."""
    try:
        subprocess.check_output(["adb", "--version"])
        return True
    except OSError:
        l.e(
            "The tool adb is not installed, check: https://developer.android.com/studio/command-line/adb"
        )
        return False


# -----------------------------------------------------------------------------
def check_tool_xcodebuild():
    """Checks if invoking supplied xcodebuild binary works."""
    try:
        subprocess.check_output(["xcodebuild", "-version"])
        return True
    except OSError:
        l.e(
            "The tool xcodebuild is not installed, check: https://developer.apple.com/xcode/"
        )
        return False


# -----------------------------------------------------------------------------
def check_tool_ios_deploy():
    """Checks if invoking supplied ios-deploy binary works."""
    try:
        subprocess.check_output(["ios-deploy", "--version"])
        return True
    except OSError:
        l.e(
            "The tool ios-deploy is not installed, check: https://github.com/ios-control/ios-deploy"
        )
        return False


# -----------------------------------------------------------------------------
def check_tool_cocoapods():
    """Checks if invoking supplied pod binary works."""
    try:
        subprocess.check_output(["pod", "--version"])
        return True
    except OSError:
        l.e(
            "The tool cocoapods is not installed, check: https://github.com/CocoaPods/CocoaPods"
        )
        return False


# -----------------------------------------------------------------------------
def check_tool_cpp_formatter():
    try:
        subprocess.check_output(["clang-format", "--version"])
        return True
    except OSError:
        l.i(
            "Clang-format is not installed, check: https://clang.llvm.org/docs/ClangFormat.html"
        )
        return False


# -----------------------------------------------------------------------------
def check_tool_python_formatter():
    try:
        subprocess.check_output(["black", "--version"])
        return True
    except OSError:
        l.i("Black is not installed, check: https://github.com/psf/black")
        return False


# -----------------------------------------------------------------------------
def check_tool_cmake_formatter():
    try:
        subprocess.check_output(["cmake-format", "--version"])
        return True
    except OSError:
        l.i(
            "Cmake-format is not installed, check: https://github.com/cheshirekow/cmake_format"
        )
        return False


# -----------------------------------------------------------------------------
def check_tool_mkdocs():
    try:
        subprocess.check_output(["mkdocs", "--version"])
        return True
    except OSError:
        l.e("Mkdocs is not installed, check: https://www.mkdocs.org/")
        return False


# -----------------------------------------------------------------------------
def check_tool_lcov():
    try:
        subprocess.check_output(["lcov", "--version"])
        return True
    except OSError:
        l.e("LCOV is not installed, check: https://github.com/linux-test-project/lcov")
        return False


# -----------------------------------------------------------------------------
def check_tool_lcov_genhtml():
    try:
        subprocess.check_output(["genhtml", "--version"])
        return True
    except OSError:
        l.e(
            "GenHTML from LCOV is not installed, check: https://github.com/linux-test-project/lcov"
        )
        return False
