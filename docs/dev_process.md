# Overview

This document contains information for anyone wishing to contribute to the project.

If you would like to contribute, you will follow these steps:

- [Set up a local build](#how-to-set-up-a-local-build)
- [Make your changes](#making-changes)
- [Submit your changes for code review](#code-review)
- [Build the package ready for release](#how-to-build-the-package)
- [Release a new version](#releasing-a-new-version)


## Dependencies

To work on the package, you need Python 3.6 or later and Node 8.


## How to set up a local build

The repo includes a simple test application that can be run locally to develop the pattern library itself.
First, clone the repo:

```sh
git clone [repo url]
cd django-pattern-library
```

You'll need to set up a virtual environment to run the code in:

```sh
python3 -m venv venv
source venv/bin/activate
```

Next, install the dependencies and run the test app:

```sh
pip install -e .  # installs the library and its dependencies in editable mode
./runserver.sh    # runs the test app using the Django development server
```

Once the server is started, the pattern library will be available at `http://localhost:8000/pattern-library/`.


## Making changes

To make changes you need to edit the files under the `pattern_library` folder. You'll be able to see your changes reflected on the localhost.

If you want to make changes to the front-end assets (located in the `pattern_library/static/pattern_library/src` folder), you'll need to set
up the tooling in order to build the assets. Node version 8 is required for this. If you're using `nvm` to manage node on your machine there's
a `.nvmrc` that means you can run `nvm use` to activate the correct version of node.

To install dependencies and build the assets, run the following commands:

```sh
npm install
npm run build
```

If you want to run the tooling in watch mode while making updates, you can use `npm run start`


## Running the tests

To run the python tests, use the script in the root of the repo:

```sh
$ ./runstests.sh
```

To run the tests using different Python versions (currently 3.6 and 3.7, which you'll need to have installed on your machine), use `tox`.
You'll need to install `tox` first, please see the documentation here: https://tox.readthedocs.io/en/latest/install.html


## Writing tests

There is a simple test pattern library app in the `tests/` folder. The tests modules themselves and are `tests/tests`.


## Code review

Create a pull request with your changes so that it can be code reviewed by a core developer. Ensure that you give a summary with the purpose
of the change and any steps that the reviewer needs to take to test your work. Please provide unit tests for your work, if possible!


## How to build the package

To build the package you need to use Python 3.

Build the python package:

```sh
virtualenv -p python3.6 venv
source venv/bin/activate
python ./setup.py bdist_wheel
```

## Releasing a new version

On the `master branch`:

1. Bump the release number in `pattern_library/__init__.py`.
2. Update the change log found at `CHANGELOG.md`
3. Commit and tag the release: `git tag -a v0.1.14 -m "Release version v0.1.14"`
4. Build the project: `python3 setup.py sdist bdist_wheel`
5. Upload the latest version to PyPI (requires credentials): `python3 -m twine upload dist/*`
