# Developer setup

## Prerequisites

Install the following:

- Python 2.7 or 3.6 (both preferably)
- Pip package manager
- Virtualenv (`pip install virtualenv`)

For more information on these, refer to the public documentation on
[Python](https://www.python.org/downloads/) or
[Pip](https://pip.pypa.io/en/stable/installing/)

## Install module locally

From the root of your cloned repo, you'll want to generate a virutal
environment with a specific version of python.

For python 3.6, run the following commands:

```bash
virtualenv -p python3 env/
. ./env/bin/activate
```

For python 2.7, run the following commands:

```bash
virtualenv -p python2 env27/
. ./env27/bin/activate
```

Then install the required packages and a local symbolic link of the `sfctl`
package:

```bash
pip install -e ./src
pip install -r requirements.txt
```

## VS Code Extensions

If using VS Code as your primary editor it is recommended you install two
extensions (`ext install <name>`):

- [python](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python)
- [code-spell-checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

There is a project dictionary committed, keep this up to date.

For different virtual environments it is also important to update the workspace
Python interpreter. This can be done by running the `Python: Select Workspace
Interpreter` command.

## Testing

Pull requests are gated on passing unit tests and linting, to run these checks
locally run the following commands:

```bash
./scripts/verify.sh local
```

For more detailed testing information, see the
[testing article](docs/testing.md).

## Requirements

Before submitting any pull requests for merging, please be sure to review
the requirements and suggestions outlined in the
[contributing guidelines](docs/coding_requirements.md) documentation.
