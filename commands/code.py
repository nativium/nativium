import os

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
from pygemstones.util import log as l

from core import module as m
from core import target
from core import tool


# -----------------------------------------------------------------------------
def run(params):
    args = params["args"]

    if len(args) > 0:
        action = args[0]

        if action:
            if action == "format":
                code_format(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def code_format(params):
    proj_path = params["proj_path"]
    format_path = proj_path

    # custom path
    custom_path = ls.get_arg_list_value(params["args"], "--path")

    if custom_path:
        format_path = os.path.abspath(custom_path)

    # all files
    all_files = ls.list_has_value(params["args"], "--all")

    # get all targets
    targets = target.get_all_targets(format_path, throw_error=False)

    # get all modules
    modules = m.get_list(proj_path)

    # process
    if all_files:
        # format c++ files
        has_tool = tool.check_tool_cpp_formatter()

        if has_tool:
            path_list = [
                {
                    "path": format_path,
                    "patterns": ["*.cpp", "*.hpp", "*.c", "*.h", "*.m", "*.mm"],
                },
            ]

            if path_list:
                l.i("Formatting C++ files...")

                format(
                    path_list=path_list,
                    formatter=lambda file_item: r.run(
                        [
                            "clang-format",
                            "-style",
                            "file",
                            "-i",
                            os.path.relpath(file_item),
                        ],
                        cwd=proj_path,
                    ),
                    ignore_path_list=[],
                )

                l.ok()
            else:
                l.i("No C++ files found to format")

        # format python files
        has_tool = tool.check_tool_python_formatter()

        if has_tool:
            path_list = [
                {
                    "path": format_path,
                    "patterns": ["*.py"],
                },
            ]

            if path_list:
                l.i("Formatting Python files...")

                format(
                    path_list=path_list,
                    formatter=lambda file_item: r.run(
                        [
                            "black",
                            "-q",
                            file_item,
                        ],
                        cwd=proj_path,
                    ),
                    ignore_path_list=[],
                )

                l.ok()
            else:
                l.i("No Python files found to format")

        # format cmake files
        has_tool = tool.check_tool_cmake_formatter()

        if has_tool:
            path_list = [
                {
                    "path": format_path,
                    "patterns": ["*.cmake", "CMakeLists.txt"],
                },
            ]

            if path_list:
                l.i("Formatting CMake files...")

                format(
                    path_list=path_list,
                    formatter=lambda file_item: r.run(
                        [
                            "cmake-format",
                            "-c",
                            ".cmake-format",
                            "-i",
                            file_item,
                        ],
                        cwd=proj_path,
                    ),
                    ignore_path_list=[],
                )

                l.ok()
            else:
                l.i("No CMake files found to format")
    else:
        # format c++ files
        has_tool = tool.check_tool_cpp_formatter()

        if has_tool:
            path_list = [
                {
                    "path": os.path.join(format_path, "apps", "desktop"),
                    "patterns": ["*.cpp", "*.hpp", "*.c", "*.h", "*.m", "*.mm"],
                },
                {
                    "path": os.path.join(format_path, "apps", "android"),
                    "patterns": ["*.cpp", "*.hpp", "*.c", "*.h", "*.m", "*.mm"],
                },
                {
                    "path": os.path.join(format_path, "apps", "ios"),
                    "patterns": ["*.cpp", "*.hpp", "*.c", "*.h", "*.m", "*.mm"],
                },
                {
                    "path": os.path.join(format_path, "apps", "wasm"),
                    "patterns": ["*.cpp", "*.hpp", "*.c", "*.h", "*.m", "*.mm"],
                },
                {
                    "path": os.path.join(format_path, "conan", "darwin-toolchain"),
                    "patterns": ["*.cpp", "*.hpp", "*.c", "*.h", "*.m", "*.mm"],
                },
            ]

            for module_name in modules:
                path_list.append(
                    {
                        "path": os.path.join(
                            format_path, "modules", module_name, "implementation"
                        ),
                        "patterns": ["*.cpp", "*.hpp", "*.c", "*.h", "*.m", "*.mm"],
                    },
                )

            if path_list:
                l.i("Formatting C++ files...")

                format(
                    path_list=path_list,
                    formatter=lambda file_item: r.run(
                        [
                            "clang-format",
                            "-style",
                            "file",
                            "-i",
                            os.path.relpath(file_item),
                        ],
                        cwd=proj_path,
                    ),
                    ignore_path_list=[
                        os.path.join(format_path, "apps", "ios", "runner", "Pods"),
                        os.path.join(format_path, "modules", "support-lib"),
                        os.path.join(
                            format_path,
                            "conan",
                            "darwin-toolchain",
                            "test_package",
                            "build",
                        ),
                    ],
                )

                l.ok()
            else:
                l.i("No C++ files found to format")

        # format python files
        has_tool = tool.check_tool_python_formatter()

        if has_tool:
            path_list = [
                {
                    "path": os.path.join(format_path, "nativium.py"),
                },
                {
                    "path": os.path.join(format_path, "commands"),
                    "patterns": ["*.py"],
                },
                {
                    "path": os.path.join(format_path, "common"),
                    "patterns": ["*.py"],
                },
                {
                    "path": os.path.join(format_path, "config"),
                    "patterns": ["*.py"],
                },
                {
                    "path": os.path.join(format_path, "core"),
                    "patterns": ["*.py"],
                },
                {
                    "path": os.path.join(format_path, "modules"),
                    "patterns": ["*.py"],
                },
                {
                    "path": os.path.join(format_path, "targets"),
                    "patterns": ["*.py"],
                },
                {
                    "path": os.path.join(format_path, "conan", "darwin-toolchain"),
                    "patterns": ["*.py"],
                },
            ]

            for module_name in modules:
                path_list.append(
                    {
                        "path": os.path.join(
                            format_path, "modules", module_name, "generate.py"
                        ),
                    },
                )

            if path_list:
                l.i("Formatting Python files...")

                format(
                    path_list=path_list,
                    formatter=lambda file_item: r.run(
                        [
                            "black",
                            "-q",
                            file_item,
                        ],
                        cwd=proj_path,
                    ),
                    ignore_path_list=[
                        os.path.join(format_path, "apps", "ios", "runner", "Pods"),
                        os.path.join(format_path, "modules", "support-lib"),
                        os.path.join(
                            format_path,
                            "conan",
                            "darwin-toolchain",
                            "test_package",
                            "build",
                        ),
                    ],
                )

                l.ok()
            else:
                l.i("No Python files found to format")

        # format cmake files
        has_tool = tool.check_tool_cmake_formatter()

        if has_tool:
            path_list = [
                {
                    "path": os.path.join(format_path, "CMakeLists.txt"),
                },
                {
                    "path": os.path.join(format_path, "cmake"),
                    "patterns": ["*.cmake"],
                },
                {
                    "path": os.path.join(format_path, "conan", "darwin-toolchain"),
                    "patterns": ["CMakeLists.txt"],
                },
            ]

            for module_name in modules:
                path_list.append(
                    {
                        "path": os.path.join(
                            format_path, "modules", module_name, "cmake"
                        ),
                        "patterns": ["*.cmake", "CMakeLists.txt"],
                    },
                )

            for target_name in targets:
                path_list.extend(
                    [
                        {
                            "path": os.path.join(
                                format_path,
                                "targets",
                                target_name,
                                "cmake",
                            ),
                            "patterns": ["*.cmake"],
                        },
                        {
                            "path": os.path.join(
                                format_path,
                                "targets",
                                target_name,
                                "cmake",
                            ),
                            "patterns": ["CMakeLists.txt"],
                        },
                        {
                            "path": os.path.join(
                                format_path,
                                "targets",
                                target_name,
                                "support",
                            ),
                            "patterns": ["*.cmake"],
                        },
                        {
                            "path": os.path.join(
                                format_path,
                                "targets",
                                target_name,
                                "support",
                            ),
                            "patterns": ["CMakeLists.txt"],
                        },
                    ]
                )

            if path_list:
                l.i("Formatting CMake files...")

                format(
                    path_list=path_list,
                    formatter=lambda file_item: r.run(
                        [
                            "cmake-format",
                            "-c",
                            ".cmake-format",
                            "-i",
                            file_item,
                        ],
                        cwd=proj_path,
                    ),
                    ignore_path_list=[
                        os.path.join(format_path, "apps", "ios", "runner", "Pods"),
                        os.path.join(format_path, "modules", "support-lib"),
                        os.path.join(
                            format_path,
                            "conan",
                            "darwin-toolchain",
                            "test_package",
                            "build",
                        ),
                    ],
                )

                l.ok()
            else:
                l.i("No CMake files found to format")


# -----------------------------------------------------------------------------
def format(path_list, formatter, ignore_path_list):
    for path_list_item in path_list:
        patterns = path_list_item["patterns"] if "patterns" in path_list_item else None

        if patterns:
            for pattern_item in patterns:
                files = f.find_files(
                    path_list_item["path"],
                    pattern_item,
                    recursive=True,
                    follow_links=True,
                )

                for file_item in files:
                    ignore_file = False

                    if ignore_path_list:
                        for ignore_path in ignore_path_list:
                            if ignore_path in os.path.abspath(file_item):
                                ignore_file = True

                    if not ignore_file:
                        if f.file_exists(os.path.abspath(file_item)):
                            l.i(
                                "Formatting file: {0}...".format(
                                    os.path.relpath(file_item)
                                )
                            )

                            formatter(file_item)
        else:
            file_item = path_list_item["path"] if "path" in path_list_item else None

            if file_item:
                ignore_file = False

                if ignore_path_list:
                    for ignore_path in ignore_path_list:
                        if ignore_path in os.path.abspath(file_item):
                            ignore_file = True

                if not ignore_file:
                    if f.file_exists(os.path.abspath(file_item)):
                        l.i(
                            "Formatting file: {0}...".format(os.path.relpath(file_item))
                        )

                        formatter(file_item)


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("Available actions:\n", l.MAGENTA)
    l.m("  - format")


# -----------------------------------------------------------------------------
def get_description(params):
    return "Code manager tool"
