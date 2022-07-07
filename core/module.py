import os

from pygemstones.io import file as f

from config import gluecode as config


# -----------------------------------------------------------------------------
def get_list(proj_path):
    # general
    module_dir = os.path.join(
        proj_path,
        "modules",
    )

    modules_found = f.find_dirs(module_dir, "*")
    modules_found.sort()

    gluecode_config = config.run(proj_path, {})
    modules_order = gluecode_config["order"] if "order" in gluecode_config else None

    # sort modules
    if modules_order:
        sorted_module_list = []
        no_sorted_module_list = []

        # found modules that are within the sort list
        for module_order_name in modules_order:
            found = False

            for module_found in modules_found:
                module_dir_name = os.path.basename(module_found)

                if module_order_name == module_dir_name:
                    found = True
                    break

            if found:
                sorted_module_list.append(module_found)

        # found modules that are not within the sort list
        for module_found in modules_found:
            module_dir_name = os.path.basename(module_found)

            if module_dir_name not in modules_order:
                no_sorted_module_list.append(module_found)

        modules_found = sorted_module_list + no_sorted_module_list

    # validate module list
    modules = []

    for module_found in modules_found:
        module_dir_name = os.path.basename(module_found)

        if module_dir_name == "support-lib":
            # support lib already have their files
            continue

        modules.append(module_dir_name)

    return modules
