# Developer setup

## Prerequisites

Install the following:

- Python 2.7 or 3.6 (both preferably)
- Pip package manager
- Virtualenv (`pip install virtualenv`)

## Install module locally

From the root of your cloned repo, run the following commands

### MacOS

For python 3.6:

```bash
virtualenv -p python3 env/
. ./env/bin/activate
```

For python 2.7:

```bash
virtualenv -p python2 env27/
. ./env27/bin/activate
```

<<<<<<< HEAD
Then install the required packages and a local symbolic link of the `sfctl`
package:

```bash
pip install -e ./src[test]
```

### Windows and Linux

Similar commands work for other OS environments, but have not been officially
tested

## Testing

Pull requests are gated on passing unit tests and linting, to run these checks
locally run the following commands:
=======
Then install the required packages and a local symbolic link of the `sf-cli`
package:

```bash
pip install -e ./src/
pip install -r requirements.txt
```

## Testing

Pull requests are gated on passing unit tests and linting, to run either of
these checks locally run the following commands:
>>>>>>> master

### MacOS

```bash
<<<<<<< HEAD
./scripts/verify.sh local
=======
./scripts/run_pylint.sh
./scripts/run_tests.sh
>>>>>>> master
```

## VS Code

If using VS Code as your primary editor it is recommended you install two
extensions (`ext install <name>`):

- [python](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python)
- [code-spell-checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)

There is a project dictionary committed, keep this up to date.

For different virtual environments it is also important to update the workspace
Python interpreter. This can be done by running the `Python: Select Workspace
Interpreter` command.