# Glue code

Almost all modules use **Djinni** as glue code tool to generate glue code files between C++ and platform code (C++ with JNI and C++ with Objective-C).

To install the glue code tool use the following command:

```
python3 nativium.py gluecode setup
```

And to check the version use:

```
python3 nativium.py gluecode version
```

Obs: Version command is optional and is used to check current installed version.

## Generate

When you want generate all glue code files again, use the following command:

```
python3 nativium.py gluecode generate
```

If you want create more modules with Djinni support, Nativium come with a easy way to do it. Only duplicate (copy and paste) any module inside **modules** and change files:

- proj.djinni
- generate.py

The file **proj.djinni** contain all interface that will be generated and require C++ implementation.

The file **generate.py** contain the method with instructions for that module that will be called automatically when you generate glue code (example: package name, namespace, include paths etc).

If you need to set the generation order because of dependencies between modules, set the order by module name within the gluecode configuration file located in `config/gluecode.py`.

If you don't use any glue code tool in your project, ignore this section, because some people prefer create the glue code files manually and is not a requirement in Nativium that modules have these files.

## Djinni forks

- Community: [https://github.com/cross-language-cpp](https://github.com/cross-language-cpp)
- Snapchat: [https://github.com/Snapchat/djinni](https://github.com/Snapchat/djinni)
