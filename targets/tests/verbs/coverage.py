import os

from pygemstones.system import runner as r
from pygemstones.util import log as l

from core import const, tool, util
from targets.tests.config import target_config as config


# -----------------------------------------------------------------------------
def run(params):
    tool.check_tool_lcov()
    tool.check_tool_lcov_genhtml()

    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    archs = util.get_parsed_arch_list(params, target_config)
    build_types = util.get_parsed_build_type_list(params, target_config)

    if archs and len(archs) > 0:
        if build_types and len(build_types) > 0:
            for arch in archs:
                for build_type in build_types:
                    l.i(
                        "Code coverage for: {0}/{1}...".format(arch["arch"], build_type)
                    )

                    # prepare
                    build_dir = os.path.join(
                        proj_path,
                        "build",
                        target_name,
                        build_type,
                        arch["arch"],
                    )

                    coverage_info_file = os.path.join(
                        build_dir,
                        "lcov.coverage.info",
                    )

                    output_dir = os.path.join(
                        build_dir,
                        "coverage-html",
                    )

                    html_file = os.path.join(
                        output_dir,
                        "index.html",
                    )

                    # lcov
                    l.i(
                        "Generating coverage data for: {0}/{1}...".format(
                            arch["arch"], build_type
                        )
                    )

                    run_args = [
                        "lcov",
                        "-d",
                        build_dir,
                        "-c",
                        "-o",
                        coverage_info_file,
                    ]

                    r.run(run_args, cwd=proj_path)

                    # lcov - remove
                    l.i(
                        "Remove unuseful coverage data for: {0}/{1}...".format(
                            arch["arch"], build_type
                        )
                    )

                    run_args = [
                        "lcov",
                        "-r",
                        coverage_info_file,
                    ]

                    run_args.extend(const.CODE_COVERAGE_EXCLUDE_LIST)

                    run_args.extend(
                        [
                            "-o",
                            coverage_info_file,
                        ]
                    )

                    r.run(run_args, cwd=proj_path)

                    # genhtml
                    l.i(
                        "Generating HTML report for: {0}/{1}...".format(
                            arch["arch"], build_type
                        )
                    )

                    run_args = [
                        "genhtml",
                        coverage_info_file,
                        "--output-directory",
                        output_dir,
                    ]

                    r.run(run_args, cwd=proj_path)

                    # results
                    l.i("Code coverage report: {0}".format(html_file))

            l.ok()
        else:
            l.e('Build type list for "{0}" is invalid or empty'.format(target_name))
    else:
        l.e('Arch list for "{0}" is invalid or empty'.format(target_name))
