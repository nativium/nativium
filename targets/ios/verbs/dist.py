import os
import subprocess

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.type import list as ls
from pygemstones.util import log as l
from pygemstones.vendor import aws as a

from core import const, net, util
from targets.ios.config import target_config as config


# -----------------------------------------------------------------------------
def run(params):
    args = params["args"]

    if len(args) > 1:
        action = args[1]

        if action:
            if action == "generate":
                generate(params)
            elif action == "download":
                download(params)
            elif action == "upload":
                upload(params)
            else:
                show_help(params)
        else:
            show_help(params)
    else:
        show_help(params)


# -----------------------------------------------------------------------------
def download(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]

    version = util.get_version(params, config)

    build_dir = os.path.join(proj_path, "build", target_name, "dist")

    net.download_dist_file(
        proj_path=proj_path,
        version=version,
        dist_file_path=os.path.join(build_dir, "dist.zip"),
        dist_file_name="dist.zip",
        dist_folder=target_name,
        dist_file_url="{0}/{1}".format(const.AWS_S3_URL, target_name),
    )


# -----------------------------------------------------------------------------
def upload(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]

    version = util.get_version(params, config)
    force = ls.list_has_value(params["args"], "--force")

    build_dir = os.path.join(proj_path, "build", target_name, "dist")
    dest_zip = os.path.join(build_dir, "dist.zip")
    dest_package = os.path.join(build_dir, "Package.swift")

    if not f.file_exists(dest_zip):
        l.e('Dist zip not found at "{0}", run the generate action first'.format(dest_zip))

    if not f.file_exists(dest_package):
        l.e(
            'Package.swift not found at "{0}", run the generate action first'.format(
                dest_package
            )
        )

    aws_key_id = os.getenv(const.AWS_KEY_ID_ENV)
    aws_secret_key = os.getenv(const.AWS_SECRET_KEY_ENV)
    aws_bucket_name = const.AWS_S3_BUCKET_NAME

    # upload both the zip and the Package.swift to the same S3 folder, so the
    # version URL is enough to fetch everything (no need to send files by hand)
    for file_path in [dest_zip, dest_package]:
        a.s3_upload(
            file_path=file_path,
            force=force,
            aws_bucket_name=aws_bucket_name,
            aws_bucket_key="{0}/{1}/{2}/{3}".format(
                const.AWS_S3_BUCKET_PATH,
                target_name,
                version,
                os.path.basename(file_path),
            ),
            aws_key_id=aws_key_id,
            aws_secret_key=aws_secret_key,
        )


# -----------------------------------------------------------------------------
def generate(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]

    target_config = config.run(proj_path, target_name, params)
    version = util.get_version(params, config)
    project_name = target_config["project_name"]
    product_name = target_config["product_name"]

    # spm always ships the release xcframework
    xcframework_dir = os.path.join(
        proj_path,
        "dist",
        target_name,
        "release",
        "{0}.xcframework".format(project_name),
    )

    if not f.dir_exists(xcframework_dir):
        l.e(
            'XCFramework not found at "{0}", run "target {1} package --build=release" first'.format(
                xcframework_dir, target_name
            )
        )

    build_dir = os.path.join(proj_path, "build", target_name, "dist")
    dest_zip = os.path.join(build_dir, "dist.zip")
    dest_package = os.path.join(build_dir, "Package.swift")

    f.create_dir(build_dir)

    # zip the xcframework (ditto preserves symlinks and code signature, same as
    # the previous tar.gz and required by SwiftPM for binary artifacts)
    l.i("Zipping xcframework...")

    f.remove_file(dest_zip)

    r.run(
        [
            "ditto",
            "-c",
            "-k",
            "--sequesterRsrc",
            "--keepParent",
            xcframework_dir,
            dest_zip,
        ],
        cwd=proj_path,
    )

    # compute swift checksum
    l.i("Computing SPM checksum...")

    checksum = (
        subprocess.check_output(
            ["swift", "package", "compute-checksum", dest_zip],
            cwd=proj_path,
        )
        .decode("UTF-8")
        .strip()
    )

    l.i("SPM checksum: {0}".format(checksum))

    # remote url where the zip will be uploaded (see upload action)
    spm_url = "{0}/{1}/{2}/dist.zip".format(const.AWS_S3_URL, target_name, version)

    # generate Package.swift into the build dist folder; consumers drop it into
    # their own project as a local Swift package pointing to the zip on S3
    l.i("Generating Package.swift...")

    template_path = os.path.join(
        "targets", target_name, "support", "spm", "Package.swift"
    )

    f.copy_file(template_path, dest_package)

    f.replace_in_file(dest_package, "{PROJECT_NAME}", project_name)
    f.replace_in_file(dest_package, "{PRODUCT_NAME}", product_name)
    f.replace_in_file(dest_package, "{SPM_URL}", spm_url)
    f.replace_in_file(dest_package, "{SPM_CHECKSUM}", checksum)

    l.ok()


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("List of available verb actions:\n", l.MAGENTA)
    l.m("  - generate")
    l.m("  - download")
    l.m("  - upload")
