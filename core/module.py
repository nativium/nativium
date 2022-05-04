import os

from pygemstones.io import file as f


# -----------------------------------------------------------------------------
def get_list(proj_path):
    module_dir = os.path.join(
        proj_path,
        "modules",
    )

    modules_found = f.find_dirs(module_dir, "*")
    modules = []

    for m in modules_found:
        module_dir_name = os.path.basename(m)

        if module_dir_name == "support-lib":
            # support lib already have their files
            continue

        modules.append(module_dir_name)

    return modules
