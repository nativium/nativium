# Tests

Nativium come with C++ test support using the [Google Testing and Mocking Framework](https://github.com/google/googletest).

You can test C++ code with the following commands:

```
python3 nativium.py target tests setup
python3 nativium.py target tests run
```

Obs: The verb **setup** install all tests dependencies and follows the previous instructions that it only needs to be done once.

## Source

You can add, remove or edit tests changing files inside folder **apps/tests**.

On tests folder you have some folders:

- **include:** contains include files and it is added as search path
- **include/fixtures:** contains all tests fixtures
- **src:** contains all tests sources

On target tests you have some folders:

- **cmake:** contains cmake module instructions by platform

## Code coverage

The tests come configure to export coverage data when the tests run.

Coverage option can be enabled of disabled in tests config target: `targets/tests/config/target.py`.

You can run coverage tool with the following command:

```
python3 nativium.py target tests coverage
```

After run coverage tool open the HTML page from last coverage information, example:

```
open build/tests/debug/x86_64/coverage-html/index.html
```

You need have installed these tool:

* LCOV (macOS: `brew install lcov`, Linux: `apt install lcov`)
