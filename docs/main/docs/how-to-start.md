# How to start

After read all Nativium concepts before, there are 6 steps to start:

1 - Clone reposity:

```
git clone https://github.com/nativium/nativium.git
```

2 - Enter on cloned folder:

```
cd nativium
```

3 - Create and activate Python virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows
```

4 - Install python requirements:

```
pip install -r requirements.txt
```

5 -  Setup conan tool:

```
python3 nativium.py conan setup
```

6 - Setup glue code tool:

```
python3 nativium.py gluecode setup
```

7 - Now all commands are available. Run the following command to list all targets that you can build:

```
python3 nativium.py target
```

If you are on **Linux**, you can build the **linux** target, if on **macOS** you can build **macos** target and if on **Windows** you can build **windows** target.

Example:

```
python3 nativium.py target linux setup  
python3 nativium.py target linux build  
python3 nativium.py target linux package  
python3 nativium.py target linux dist generate  
```

## Tips

1. You can download the project as a TAR/ZIP file too: [https://github.com/nativium/nativium/archive/main.tar.gz](https://github.com/nativium/nativium/archive/main.tar.gz).
2. After run this commands above, a folder called **dist** will be created with compiled binaries of applications. The rule is the same for other targets.
3. The execution order is important. You need setup files and dependencies, build, package and distribute (setup, build, package and dist verbs).
4. Package verbs will copy files to a non versioned folder called **dist** in root path.
5. You don't need run **setup** verb everytime, only run if you never run it before or if you change configuration (example is version number), added dependencies, changed dependency version or other things that really need call **setup** to generate target files and rebuilt your dependencies.
6. Conan profiles are required to specify basic environment profile things to build targets, but some settings are changed while build, like **arch** and **build_type**.
7. Check [requirements](requirements.md) for each target. Example: iOS target require that you have a macOS system.
