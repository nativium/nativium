# Apple


## macOS

If you are on a machine with ARM (M1) processor and have problems with `conan`, you can change your macOS profile file `nativium_macos_profile` or the default profile file `arch` and `arch_build` settings for `x86_64` with the following commands:

```
conan profile new default --detect
conan profile update settings.arch="x86_64" default
conan profile update settings.arch_build="x86_64" default
```

## iOS

1. Add your framework or xcframework as dependency (see example files below)
2. Create **Objective-C Bridging Header** file to include your public headers or the main header file
3. Add to your target **Build Settings** in row **Objective-C Bridging Header** the path of bridging header file, example: `Runner/Runner-Bridging-Header.h`

## watchOS

1. Add your framework or xcframework as dependency (see example files below)
2. Create **Objective-C Bridging Header** file to include your public headers or the main header file
3. Add to your target **Build Settings** in row **Objective-C Bridging Header** the path of bridging header file, example: `Runner-WatchExtension/Runner-Bridging-Header.h`
4. Add to your target **Build Settings** that is a **watch extension** in row **Excluded Architectures**:

```
> Debug > Any watchOS Simulator SDK > i386      
> Release > Any watchOS Simulator SDK > i386  
```

## tvOS

1. Add your framework or xcframework as dependency (see example files below)
2. Create **Objective-C Bridging Header** file to include your public headers or the main header file
3. Add to your target **Build Settings** in row **Objective-C Bridging Header** the path of bridging header file, example: `Runner-Tv/Runner-Bridging-Header.h`

## Consuming the SDK via Swift Package Manager

The SDK is distributed as a binary `xcframework` hosted on S3 and consumed via
Swift Package Manager as a **local package**. Only the binary comes from S3 — the
manifest lives inside your own project, so no git access to the SDK repository is
required.

Keep a local package folder (e.g. `NativiumSDK/`) with a `Package.swift` pointing
to the desired version:

```swift
// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "Nativium",
    platforms: [.iOS(.v12), .tvOS(.v12), .watchOS(.v5)],
    products: [.library(name: "nativium", targets: ["nativium"])],
    targets: [
        .binaryTarget(
            name: "nativium",
            url: "https://nativium.s3.amazonaws.com/dist/ios/1.0.0/dist.zip",
            checksum: "<checksum of this version>"
        ),
    ]
)
```

The `Package.swift` of each version (already filled with the correct url and
checksum) is published next to the binary on S3, so you can just download it:

```
https://nativium.s3.amazonaws.com/dist/ios/1.0.0/Package.swift
```

Add the `nativium` library to the targets that use the SDK (Runner, Runner-Tv,
Runner-WatchExtension, Runner-Tests).

## Sample of project.yml (XcodeGen)

The sample app declares the local package and links it to each target through
[XcodeGen](https://github.com/yonaskolb/XcodeGen). See
`apps/ios/runner/project.yml` for the full multi-platform example (iOS, tvOS and
watchOS app + extension). The relevant bits are:

```yaml
packages:
  Nativium:
    path: NativiumSDK

targets:
  Runner:
    type: application
    platform: iOS
    dependencies:
      - package: Nativium
        product: nativium
```

Generate the project with `xcodegen generate` (or `make project`), and download
the SDK manifest with `make sdk`.

## Sample of Bridging Header file

```
#ifndef Bridging_Header_h
#define Bridging_Header_h

#include <nativium/Nativium.h>

#endif /* Bridging_Header_h */
```

Or, since the framework is a self-contained Clang module, you can simply use
`@import nativium;` (Objective-C) / `import nativium` (Swift) instead of a
bridging header.

## Utilities

Some useful macros to check OS and execute specific code for that OS:

#### Swift

```
#if os(OSX)
  // compiles for OS X
#elseif os(iOS)
  // compiles for iOS
#elseif os(tvOS)
  // compiles for TV OS
#elseif os(watchOS)
  // compiles for Watch OS
#endif

or

if #available(macOS 10.15, *) {
  // compiles for OS X
} else if #available(iOS 9, *) {
  // compiles for iOS
} else if #available(tvOS 11, *) {
  // compiles for TV OS
} else if #available(watchOS 5, *) {
  // compiles for Watch OS
}

or

#if os(OSX) && os(iOS)
  // compiles for OS X and iOS
#endif

or

#if os(OSX) || os(iOS)
  // compiles for OS X or iOS
#endif
```

#### Objective-C

```
#if TARGET_OS_OSX
    // compiles for OS X
#elif TARGET_OS_IOS
    // compiles for iOS
#elif TARGET_OS_TV
    // compiles for TV OS
#elif TARGET_OS_WATCH
    // compiles for WATCH OS
#endif

or 

if (@available(macOS 10.15, *)) {
  // compiles for OS X
} else if (@available(iOS 9, *)) {
  // compiles for iOS
} else if (@available(tvOS 11, *)) {
  // compiles for TV OS
} else if (@available(watchOS 5, *)) {
  // compiles for Watch OS
}

or

if (@available(macOS 10.15, iOS 9, tvOS 11, watchOS 5, *)) {
  // compiles for OS X and iOS and TV OS and Watch OS with specified versions
}
```

## Package for local development

If you are developing the framework locally, point the `binaryTarget` in your
`NativiumSDK/Package.swift` to the local `xcframework` instead of the S3 url,
using `path` instead of `url`/`checksum`. Example:

```swift
.binaryTarget(
    name: "nativium",
    path: "../../../dist/ios/release/nativium.xcframework"
)
```

Build the framework locally with:

```
python3 nativium.py target ios package --no-framework
```

Then resolve the package again (`make sdk-clean`, or just re-open the project).

## Simulator for watchOS

Compilation for watchOS 32-bits was removed. If you need it follow the steps:

1 - Remove the `EXCLUDED_ARCHS[sdk=watchsimulator*]` setting from the watchOS
extension target in `apps/ios/runner/project.yml`.

2 - Add target data in file `targets/ios/config/target_config.py`.

3 - Regenerate the project with `xcodegen generate`.
