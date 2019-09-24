# Overview

This document contains information for anyone wishing to contribute to the project.

If you would like to contribute, you will follow these steps:

- Set up a local build - see [here](#how-to-set-up-a-local-build)
- Make your changes - see [here](#making-changes)
- Submit your changes for code review - see [here](#code-review)
- Build the package ready for release - see [here](#how-to-build-the-package)
- Release a new version - see [here](#releasing-a-new-version)

## How to set up a local build

The repo includes a simple test application that can be run locally to develop the pattern library itself.
First, clone the repo:

```sh
git clone [repo url]
cd django-pattern-library
```

You'll need to set up a virtual environment to run the code in. If you've not used `virtualenv` before, see https://packaging.python.org/guides/installing-using-pip-and-virtual-environments

```sh
virtualenv -p python3.6 venv
source venv/bin/activate
```

Next, install the dependencies and run a test app

```sh
pip install -e .  # installs the library and its dependencies in editable mode
./runserver.sh    # runs the test app using the Django development server
```

Once the server is started, the pattern library will be available at `http://localhost:8000/pattern-library/`.

## Writing tests
TODO

## Code review
Create a pull request with your changes so that it can be code reviewed by a core developer. Ensure that you give a summary with the purpose of the change

## How to build the package

To build the package you need to Python 3 and Nodejs 8.

Install FE dependencies and build static:

```sh
npm install
npm run build
```

Build the python package:

```sh
virtualenv -p python3.6 venv
source venv/bin/activate
python ./setup.py bdist_wheel
```

## Releasing a new version

1. Bump the release number in `pattern_library/__init__.py`.
2. Update the change log found at `CHANGELOG.md`
3. Commit and tag the release: `git tag -a v0.1.14 -m "Release version v0.1.14"`
4. Build the project: `python3 setup.py sdist bdist_wheel`
5. Upload the latest version to PyPi: `python3 -m twine upload dist/*`

