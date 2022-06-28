# Custom

This is a feature that allows you to use the entire architecture of the Nativium project **without** having to have a **copy** of it in your repository.

Through the command `python3 nativium.py custom install` a configuration file is read and processed, creating, copying or deleting files from the original project and adding the **custom files** from your project.

The main advantage is use the **updated** Nativium architecture everytime that you need build your project.

## How to use

If you plan to use it, your project only need have the **custom** folder with the files to be merged later by the command mentioned above.

Example:

```
git clone https://github.com/nativium/nativium.git nativium
cp -r custom nativium/custom
cd nativium
python3 nativium.py custom install
```

or

```
git clone https://github.com/nativium/nativium.git nativium
cd nativium
python3 nativium.py custom install --path=../custom
```

## Example

Imagine a folder called **custom** in your project root with this content:

```
> /custom
--> custom_config.py
--> /targets/linux/cmake/target.cmake
--> /my-folder/my-other-folder
> /nativium
--> [all nativum files]
```

The file `custom_config.py` has the content:

```
def run(params):
    return [
        {
            "type": "copy-dir",
            "source": "targets",
            "target": "targets",
        },
        {
            "type": "copy-dir",
            "source": "my-folder",
            "target": "config",
        }
    ]
```

When you execute the following command:

```
cd nativium
python3 nativium.py custom install --path=../custom
```

Nativium will read the config file `custom_config.py` from root folder `custom` and will do:

1. Copy folder `custom/targets` to `/targets` of Nativium root folder.
2. Copy folder `custom/my-folder` to `/config` of Nativium root folder.

You can download Nativium only when will use it to build or develop and can delete it after use or add folder `nativium` to `.gitignore` file.

## Operations

Custom install has support for some operations:

- **copy-file**: copy a file from source to target path
- **copy-dir**: copy a folder from source to target path
- **symlink**: create a symbolic link from source to target path
- **remove-file**: remove a file from path
- **remove-dir**: remove a folder from path
- **remove-symlink**: remove a symbolic link from path
- **replace-text**: replace an old text using a new text from a file in path
