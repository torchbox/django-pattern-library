# Overview

This document contains information for project developers.

## How to build the package

To build the package you need to Python 3 and Nodejs 8.

Install FE dependencies and build static:

```
npm install
npm run build
```

Build the python package:

```
virtualenv -p python3.6 venv
source venv/bin/activate
python ./setup.py bdist_wheel
```

## Releasing a new version

1. Bump the release number in `pattern_library/__init__.py`.
2. Commit and tag the release: `git tag -a v0.1.14 -m "Release version v0.1.14"`
3. Build the project: `python3 setup.py sdist bdist_wheel`
4. Upload the latest version to PyPi: `python3 -m twine upload dist/*`
