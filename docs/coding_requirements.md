# Coding and contributing requirements

Before making any contributions, be sure your code does not violate any of the
following rules and guidelines.

## Unwritten style rules

There are some rules that PyLint does not check for that should be obeyed

- Use only `'` for strings except in docstrings

## PyLint exclusions

When specifying PyLint exclusions, use the human readable string format
for the rule rather than the number value.

A correct example:

```python
# pylint: disable=too-few-public-methods
```

## Spell check

Run a form of spell checker over command names and comments. If using VS Code
it is recommended, you install the
[Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) extension.

## History and version updates

When making any code change, be sure to update the release history accordingly
in the README file located at `src\README.rst`. Any new changes should be
added to a new version called `unreleased`.

At the time of releasing a new CLI version, the code owners change
the `README.rst` file to represent the released code version.

## Code ownership

When adding new command groups and files, be sure to update the
`CODEOWNERS` file at the root of the repository. For more information, see the
[GitHub documentation](https://help.github.com/articles/about-codeowners/)
on code owners.

## Supporting Python 2.7 and 3.6

The Service Fabric CLI supports the latest versions of both Python 2 and 3.
Be sure that your code runs in both 2.7 and 3.6. The test suites should be
run in virtual environments for both supported versions.
