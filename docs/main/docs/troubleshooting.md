# Troubleshooting

### Enable conan debug

```
export CONAN_VERBOSE_TRACEBACK=1
export CONAN_LOGGING_LEVEL=0
export CONAN_PRINT_RUN_COMMANDS=1
```

### Linux error when execute commands

If you get a message with **distutils.dir_util** error, try install the separated package for it with the command:

```
sudo apt install python3-pip
```
