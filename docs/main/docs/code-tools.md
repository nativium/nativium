# Code tools

Nativium has support for automatic source code format with command **code** .

To format all supported files, run the following command:  

```
python3 nativium.py code format  
```

Obs 1: Code format use **clang-format** tool inside to format C++ files. You need have it installed and in your **path** to be located.

Obs 2: Code format use **black** tool inside to format PYTHON files. You need have it installed and in your **path** to be located.

Obs 3: Code format use **cmake-format** tool inside to format CMAKE files. You need have it installed and in your **path** to be located.

## Custom path

In case you want to format a folder outside the project structure, use the `--path` parameter passing the folder path. The same rules configured in the `code` command will be applied in the folder informed in the parameter.

Example:

```
python3 nativium.py code format --path=../nativium-game/custom
```

## macOS

On macOS you can install all required tools with [Brew](https://brew.sh/):

```
brew install clang-format
python3 -m pip install cmake-format
python3 -m pip install black
```
