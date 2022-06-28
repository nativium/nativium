# Documentation

Nativium come with multiple documentation generator.

Each documentation folder come with files compatible with [mkdocs](https://github.com/mkdocs/mkdocs) tool with [mkdocs-material](https://github.com/squidfunk/mkdocs-material) theme.

Inside folder **docs** you can create how many documentations do you need.

## Test locally

While you write your documentation, you can see it in your browser with the command:

```
python3 nativium.py doc serve --name=main
```

Now, open in your browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Parameters

- `--name:` The folder name and configuration name
- `--force:` Overwrite documentation already published

## Configurations

All documentation settings need be inside file **config/docs.py**.

Obs: The configuration **append_version** will append **version** to folder where documentation is stored when published.
