# Requirements

The general minimum requirements that you need is:

1. Python 3 ([https://www.python.org](https://www.python.org))
2. PIP ([https://pip.pypa.io](https://pip.pypa.io))
3. CMake 3.20.0 ([https://cmake.org](https://cmake.org))
4. Conan 1.48.0 ([https://conan.io](https://conan.io))
5. Java 11 (JDK) ([https://www.oracle.com/java/technologies/downloads](https://www.oracle.com/java/technologies/downloads))

These are the tools that Nativium need to work. Check on terminal if you have every tool in your path typing their names (python, pip, cmake, conan and java).

And for each platform you need have others small requirements.

## Requirements for Android

1. Supported operational system: macOS, Linux or Windows.  
    
```
Conan will download NDK and other things to build based on your system.
```

NDK WebSite: https://developer.android.com/ndk

## Requirements for iOS, tvOS, watchOS and macCatalyst

1. Supported operational system: macOS.
2. Xcode.
3. Command line tools (run on terminal: `xcode-select --install`).

## Requirements for macOS

1. Supported operational system: macOS.
2. Xcode.
3. Command line tools (run on terminal: `xcode-select --install`).
4. Optional system headers (only if you have problems on old macOS versions). Run on terminal: `open /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg`

Obs: On step #4 the path can change for each macOS version (10.14 is mojave) and this is required because old softwares search on old places for this headers, like old openssl versions.

## Requirements for Linux

1. Supported operational system: Linux.
2. C++ compiler installed (example on Ubuntu: `sudo apt install build-essential`).

## Requirements for Windows

1. Supported operational system: Windows.
2. Visual Studio installed.  

Obs 1: Everything can be tested and compiled using community version. On Visual Studio installation process select "Desktop development with C++".

Visual Studio Site: [https://visualstudio.microsoft.com/vs/](https://visualstudio.microsoft.com/vs/)

## Requirements for Web Assembly (WASM)

1. Supported operational system: macOS, Linux or Windows.  
    
```
Conan will download Emscripten and other things to build based on your system.
```

Emscripten Site: [https://emscripten.org](https://emscripten.org)

Emscripten Repository: [https://github.com/emscripten-core/emscripten](https://github.com/emscripten-core/emscripten)

