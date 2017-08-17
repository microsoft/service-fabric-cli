# Pip and Install Help

Sometimes users report issues installing or referencing the `sfctl` python package.

## Troubleshooting

To eliminate any environmental issues, double check that other packages can be installed and run. For example, try testing with the `virtualenv` package.

```bash
pip install virtualenv
virtualenv -p python2 env/
```

Here are some common issues related to `pip` that can result in the `sfctl` package not working correctly.

### Incorrect pip install

It is reccomended you always run the latest version of pip. Installation of pip varies across operating systems, but here are some tested configurations that are known to work.

#### MacOS with Homebrew

Install using [homebrew](https://brew.sh), then run

```bash
brew install python3
pip3 install sfctl
```

This will install the latest version of Python 3 and then the sfctl package. This has been tested on MacOS 10.12.6

#### Ubuntu

The default `apt-get` installation of `pip` will work in this case, however it will default to the system installed version of Python 2 and an outdated version of `pip`.

```bash
sudo apt-get install python-pip
pip install sfctl
```

This has been tested on Ubuntu Desktop Edition 16.04

### Incorrect path to sfctl

Shims for calling into the `sfctl` module will be automatically created upon install. A users `$PATH` variable should be previously correctly configured to reference any installed python package.

To verify, double check the following returns a non empty path:

```bash
which -a pip
```

The install path to `pip` should also be in the `$PATH` variable.
