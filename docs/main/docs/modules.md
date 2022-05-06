# Modules

A module describe what source code and dependencies need be compiled.

Organize the source code in modules is optional and your source code can exists inside only in one general module folder, but generally a project have a lot of code that can be organized in small folders that Nativium call modules.

Some companies create a module for `core` code, other for `repository` code to work with database and a folder for `domain` classes. This varies from project to project.

Nativium come with one module already implemented for test and example called `app-core` and is located in `modules/app-core`.

All modules source code are stored in **modules** folder.

## Configuration

The module can have a Conan configuration file located in `modules\[NAME]\config\module_conan.py`. It contains some Conan configuration and module dependencies.

**Example:**

```
# -----------------------------------------------------------------------------
def configure(params={}):
    conanfile: ConanFile = params["conanfile"]

    conanfile.options["date"].header_only = True


# -----------------------------------------------------------------------------
def requirements(params={}):
    conanfile: ConanFile = params["conanfile"]

    conanfile.requires("date/3.0.1")
```
