# Libraries

Nativium can use any C or C++ library that works for your target platform.

The C/C++ dependency manager used in Nativium is [Conan](https://conan.io/). With Conan you can add any library that fit your needs.

Conan main recipe list is hosted on Github:

[https://github.com/conan-io/conan-center-index/tree/master/recipes](https://github.com/conan-io/conan-center-index/tree/master/recipes)

## Support library

The glue code is automatically generated using Djinni tool.

The support library embedded in Nativium come from Djinni and is a wrapper between C++ and platforms code, like [JNI](https://developer.android.com/training/articles/perf-jni) and [Objective-C](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html).

 The support library can be removed if you don't use in your project. It is located in `modules/support-lib`.
