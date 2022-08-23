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

## Sample of Podfile

```
source 'https://github.com/CocoaPods/Specs.git'

# variables
IOS_PLATFORM = '9.0'
WATCHOS_PLATFORM = '6.2'
TVOS_PLATFORM = '14.0'

NATIVIUM_LIBRARY_LOCAL_PATH = true
NATIVIUM_LIBRARY_LOCAL_SERVER = false
NATIVIUM_LIBRARY_VERSION = '1.0.0'
NATIVIUM_IS_DEBUGGABLE = false

# settings
use_frameworks!

# dependencies
def shared_pods

  if NATIVIUM_LIBRARY_LOCAL_PATH
    pod 'nativium', :path => '../../../dist/ios'
  elsif NATIVIUM_LIBRARY_LOCAL_SERVER
    pod 'nativium', :http => 'http://127.0.0.1:8000/dist.tar.gz'
  else
    pod 'nativium', :http => 'https://nativium.s3.amazonaws.com/dist/ios/' + NATIVIUM_LIBRARY_VERSION + '/dist.tar.gz'
  end

end

target 'Runner' do
  platform :ios, IOS_PLATFORM
  shared_pods

  target 'Runner-Tests' do
    # specific pods
  end
end

target 'Runner-WatchExtension' do
  platform :watchos, WATCHOS_PLATFORM
  shared_pods
end

target 'Runner-Tv' do
  platform :tvos, TVOS_PLATFORM
  shared_pods
end

post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['EXCLUDED_ARCHS[sdk=watchsimulator*]'] = 'i386'
    end
  end
end
```

## Sample of Bridging Header file

```
#ifndef Bridging_Header_h
#define Bridging_Header_h

#include <Nativium/Nativium.h>

#endif /* Bridging_Header_h */
```

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

if #available(macOS 10.9, *) {
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

if (@available(macOS 10.9, *)) {
  // compiles for OS X
} else if (@available(iOS 9, *)) {
  // compiles for iOS
} else if (@available(tvOS 11, *)) {
  // compiles for TV OS
} else if (@available(watchOS 5, *)) {
  // compiles for Watch OS
}

or

if (@available(macOS 10.9, iOS 9, tvOS 11, watchOS 5, *)) {
  // compiles for OS X and iOS and TV OS and Watch OS with specified versions
}
```

## Package for development

If you are developing the framework locally, you can set the Podfile variable `NATIVIUM_LIBRARY_LOCAL_PATH` to `true` and package the framework for development using `--dev` flag. Example:

```
python3 nativium.py target ios package --no-framework --dev
```

The flag `--dev` change all paths inside `podspec` to your local path.

This is useful if you don't want start the local HTTP server to Cocoapods download the binary archive.

And when you package for development with local HTTP server or for production, remove the `--dev` flag, because it is exclusive for development with local path enabled.

## Simulator for watchOS

Compilation for watchOS 32-bits was removed. If you need it follow the steps:

1 - Remove the lines from `Podfile`:

```
post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['EXCLUDED_ARCHS[sdk=watchsimulator*]'] = 'i386'
    end
  end
end
```

2 - Add target data in file `targets/ios/config/target.py`.

3 - Remove `Exclude Architectures` from Xcode project watchOS `extension` project.
