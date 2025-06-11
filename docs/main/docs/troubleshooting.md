# Troubleshooting

### Enable conan debug

```
export CONAN_VERBOSE_TRACEBACK=1
export CONAN_LOGGING_LEVEL=0
export CONAN_PRINT_RUN_COMMANDS=1
```

### Linux error when execute commands

If you get a message with `distutils.dir_util` error, try install the separated package for it with the command:

```
sudo apt install python3-pip
```

### Build for iOS but get macOS compiler instead

There is a problem on native Python 3 from macOS because it come with an environment variable when python start that break `cmake` tool.

The environment variable `SDKROOT` that Python 3 for macOS already define, is used by tools like `cmake` to find the correct compiler and other things required to compile the code.

If you have this problem, you can solve it by installing Python 3 from [Homebrew](https://brew.sh/).

To test if this is your case, execute on terminal:

```
python3 -c 'import os; print(os.environ["SDKROOT"])'
```

If it shows something like this, you will have problems:

```
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk
```

But if you have an `error` like this, you don't have this problem in your python installation:

```
KeyError: 'SDKROOT'
```

### Application for iOS don't archive using local path

If you are using `local path` enabled inside `apps/ios/runner/Podfile` and get an error like `framework not found` when archive your application, use `local server` instead, changing the file `apps/ios/runner/Podfile` to:

```
NATIVIUM_LIBRARY_LOCAL_PATH = false
NATIVIUM_LIBRARY_LOCAL_SERVER = true
```

### IDE can't find dependencies or libraries

If your IDE can't find the dependencies or libraries, it might be because the dependencies are managed by Conan and your IDE needs to be configured with the proper toolchain.

You need to configure your IDE to use the **conan toolchain** file that is generated after building the project.

The toolchain file location follows this pattern:
`build/{platform}/{configuration}/{architecture}/conan/generators/conan_toolchain.cmake`

**Examples:**

- **macOS ARM64:** `build/macos/debug/arm64/conan/generators/conan_toolchain.cmake`
- **macOS x86-64:** `build/macos/debug/x86_64/conan/generators/conan_toolchain.cmake`

Configure your IDE to use the appropriate toolchain file for your target platform and architecture.
