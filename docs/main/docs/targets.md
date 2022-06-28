# Targets

A target describe how the source code will be compiled.

Usually each target is a platform, but you can organize it however you want, including having multiple targets for the same platform.

The target folder contains all files and scripts to build the source code to some platform. You can see all targets inside folder **targets**.

Currently all targets use [CMake](https://cmake.org/) to compile and generate project files ready to build. So each target has their own **cmake** folder with some CMake files, example `targets/linux/cmake/target.cmake` and `targets/linux/cmake/source.cmake`.

Generally all targets share the most C++ code and CMake code in the project. Because this, Nativium has a **commom** CMake folder on root called **cmake**.

Some targets add more source files and compile parameters. For example are the targets **android** that add their JNI files and **ios** that add their Objective-C files.

## Verbs

A target has their **verbs** that can have any name like **build** or **package**. All verbs are files stored inside **verbs** folder of a target **folder**, and the file name will be used to appear on target verb list when you call the target command on terminal. Example:

```python3 nativium.py target linux```

When you execute a **target verb** the Nativium system will search for a file with it name inside **verbs folder**. Example:

```python3 nativium.py target linux build```

It will execute bootstrap file of Nativium, that will do some validations and will search for a file with the path `targets/linux/verbs/build.py` and will send all parameters to a function called **run** inside it.

If you don't remember what verbs are available for a target you can execute the **target command** with **target name** to list all verbs:

```python3 nativium.py target linux```

## Configuration

The target can have a Conan configuration file located in `targets\[NAME]\config\target_conan.py`. It contains some Conan configuration and target dependencies.

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
