import os

from pygemstones.io import file as f
from pygemstones.util import log as l

from core import const, net


# -----------------------------------------------------------------------------
def run(params):
    # prepare data
    proj_path = params["proj_path"]
    target_name = params["target_name"]

    build_dir = os.path.join(proj_path, "build", target_name, "dist")
    dist_file = os.path.join(build_dir, const.FILE_NAME_DIST_PACKED)

    if not f.file_exists(dist_file):
        l.e("File was not found to serve on path {0}".format(dist_file))

    # serve
    net.serve(build_dir)
