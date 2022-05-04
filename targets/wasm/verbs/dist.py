import mimetypes as mime
import os

import boto3
from pygemstones.io import file as f
from pygemstones.type import list as ls
from pygemstones.util import log as l
from pygemstones.vendor import aws as a

from core import const, net, pack, util
from targets.wasm.config import target as config


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
            elif action == "publish":
                publish(params)
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

    build_dir = os.path.join(proj_path, "build", target_name, "dist")

    version = util.get_version(params, config)
    dist_file_path = os.path.join(build_dir, const.FILE_NAME_DIST_PACKED)
    dist_file_name = const.FILE_NAME_DIST_PACKED
    dist_folder = target_name
    aws_s3_url = "{0}/{1}".format(const.AWS_S3_URL, target_name)

    net.download_dist_file(
        proj_path=proj_path,
        version=version,
        dist_file_path=dist_file_path,
        dist_file_name=dist_file_name,
        dist_folder=dist_folder,
        dist_file_url=aws_s3_url,
    )


# -----------------------------------------------------------------------------
def upload(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]

    build_dir = os.path.join(proj_path, "build", target_name, "dist")

    version = util.get_version(params, config)
    force = ls.list_has_value(params["args"], "--force")
    dist_file_path = os.path.join(build_dir, const.FILE_NAME_DIST_PACKED)
    aws_key_id = os.getenv(const.AWS_KEY_ID_ENV)
    aws_secret_key = os.getenv(const.AWS_SECRET_KEY_ENV)
    aws_bucket_name = const.AWS_S3_BUCKET_NAME
    aws_bucket_path = "{0}/{1}/{2}/{3}".format(
        const.AWS_S3_BUCKET_PATH, target_name, version, const.FILE_NAME_DIST_PACKED
    )

    a.s3_upload(
        file_path=dist_file_path,
        force=force,
        aws_bucket_name=aws_bucket_name,
        aws_bucket_key=aws_bucket_path,
        aws_key_id=aws_key_id,
        aws_secret_key=aws_secret_key,
    )


# -----------------------------------------------------------------------------
def generate(params):
    # prepare data
    proj_path = params["proj_path"]
    target_name = params["target_name"]

    target_config = config.run(proj_path, target_name, params)
    build_types = target_config["build_types"]

    version = util.get_version(params, config)
    source_files = []

    dist_folder = os.path.join(proj_path, "dist", target_name)

    # add folders
    for build_type in build_types:
        source_files.append(
            {
                "path": os.path.join(dist_folder, build_type),
                "arcname": build_type,
            }
        )

    # generate
    pack.generate(
        proj_path=proj_path,
        target_name=target_name,
        version=version,
        source_files=source_files,
    )


# -----------------------------------------------------------------------------
def publish(params):
    proj_path = params["proj_path"]
    target_name = params["target_name"]
    target_config = config.run(proj_path, target_name, params)

    # prepare data
    version = target_config["version"] if "version" in target_config else None
    append_version = (
        target_config["append_version"] if "append_version" in target_config else None
    )
    force = ls.list_has_value(params["args"], "--force")
    build_type = ls.get_arg_list_value(params["args"], "--build")

    aws_key_id = os.getenv(const.AWS_KEY_ID_ENV)
    aws_secret_key = os.getenv(const.AWS_SECRET_KEY_ENV)
    aws_bucket_name = target_config["publish_bucket_name"]
    aws_bucket_path = target_config["publish_bucket_path"]

    if append_version:
        aws_bucket_path = "{0}/{1}".format(aws_bucket_path, version)

    ignore_files = [".DS_Store", "Thumbs.db"]

    # version
    if append_version:
        if not version or len(version) == 0:
            l.e("You need define version name (parameter: --version)")

    l.i("Version defined: {0}".format(version))

    # build type
    if not build_type:
        build_type = "debug"

    found = False

    for item in target_config["build_types"]:
        if item.lower() == build_type:
            build_type = item
            found = True

    if found:
        l.i("Build type defined: {0}".format(build_type))
    else:
        l.e("Build type is invalid: {0}".format(build_type))

    # output folder
    output_path = os.path.join(proj_path, "dist", target_name, build_type, "wasm")

    if not f.dir_exists(output_path):
        l.e("Distribution folder not exists: {0}".format(output_path))

    # aws
    if not aws_key_id or not aws_secret_key:
        l.e("Your AWS credentials are invalid")

    s3_client = boto3.client(
        service_name="s3",
        aws_secret_access_key=aws_secret_key,
        aws_access_key_id=aws_key_id,
    )

    # checking for existing path
    l.i(
        'Checking if remote path "{0}" exists on AWS...'.format(
            aws_bucket_path,
        )
    )

    has_remote_path = a.s3_path_exists(
        s3_client,
        aws_bucket_name,
        aws_bucket_path,
    )

    if has_remote_path:
        if force:
            l.i(
                'The path "{0}" already exists on AWS, removing...'.format(
                    aws_bucket_path
                )
            )

            a.s3_delete_path(
                s3_client,
                aws_bucket_name,
                aws_bucket_path,
            )
        else:
            l.e('The path "{0}" already exists on AWS'.format(aws_bucket_path))

    # create path folder
    a.s3_create_path(
        s3_client,
        aws_bucket_name,
        aws_bucket_path,
    )

    # upload
    walks = os.walk(output_path)

    for source, dirs, files in walks:
        l.i("Entering directory: {0}".format(source))

        for filename in files:
            if filename in ignore_files:
                continue

            local_file_path = os.path.join(source, filename)
            relative_path = os.path.relpath(local_file_path, output_path)

            s3_file = os.path.join(aws_bucket_path, relative_path)

            l.i(
                'Uploading file "{0}" to S3 bucket "{1}"...'.format(
                    relative_path, aws_bucket_name
                )
            )

            extra_args = {}

            if os.path.isdir(local_file_path):
                extra_args = {
                    "ACL": "public-read",
                }
            elif os.path.isfile(local_file_path):
                mime_type = mime.guess_type(local_file_path)

                extra_args = {
                    "ACL": "public-read",
                    "ContentType": (
                        mime_type[0]
                        if mime_type != None
                        and len(mime_type) > 0
                        and mime_type[0] != None
                        else ""
                    ),
                }

            s3_client.upload_file(
                local_file_path,
                aws_bucket_name,
                s3_file,
                ExtraArgs=extra_args,
                Callback=a.ProgressPercentage(local_file_path),
            )

    if append_version:
        l.colored(
            "[DONE] You can access the application here: {0}/{1}/index.html".format(
                target_config["url"],
                version,
            ),
            l.GREEN,
        )
    else:
        l.colored(
            "[DONE] You can access the application here: {0}/index.html".format(
                target_config["url"],
            ),
            l.GREEN,
        )


# -----------------------------------------------------------------------------
def show_help(params):
    l.colored("List of available verb actions:\n", l.MAGENTA)
    l.m("  - generate")
    l.m("  - download")
    l.m("  - upload")
    l.m("  - publish")
