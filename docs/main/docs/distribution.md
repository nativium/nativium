# Distribution

Distribution can be done individually by target. Today all **dist.py** (target verb) upload final file to AWS S3.

You can call **dist** verb from any target, example:

```
python3 nativium.py target linux dist
```

The folder with name **dist** has the data to deploy (Android, iOS, Windows, macOS, Linux and others) and this folder is not versioned, but you can download distribution file with the following command:

```
python3 nativium.py target linux dist download --version=1.0.0
```

This command will download a packed file and will unpack to **dist** folder:

You can also generate a packed **dist** folder again using:

```
python3 nativium.py target linux dist generate --version=1.0.0
```

And you can upload with:

```
python3 nativium.py target linux dist upload --version=1.0.0
```

## Tips

Obs 1: This template come configured with AWS S3 when upload distribution files.

Obs 2: Set environment keys `NATIVIUM_AWS_KEY_ID` and `NATIVIUM_AWS_SECRET_KEY` with your AWS key data.

Obs 3: You can change all AWS configurations like bucket name and bucket path from file **core/const.py**.

Obs 4: The parameter `--version` is optional and if you omit it will use version from the target configuration file.

Obs 5: You can download version 1.0.0 for all targets and not only "linux" because Nativium have everything compiled and uploaded for all targets and version 1.0.0 for tests.

Obs 6: You can force AWS S3 delete file if it exists using parameter `--force`.

## Android

The Android sample project is configured with a custom task to download SDK from AWS S3 or local server. You can change to local path or attach SDK project as module.

1. Local repository mode
2. Remote repository mode
3. Module project
4. Local server mode

When use local server, you need start a simple HTTP server to gradle tool download the file **dist.tar.gz** that was generated. You can do it with the command:

```
python3 nativium.py target android serve
```

## iOS

The iOS sample project is configured with a custom Pod to download SDK from AWS S3 or local server. You can change to local path or remote file.

1. Local repository mode
2. Remote repository mode
3. Local server mode

When use local server, you need start a simple HTTP server to cocoapods tool download the file **dist.tar.gz** that was generated. You can do it with the command:

```
python3 nativium.py target ios serve
```
