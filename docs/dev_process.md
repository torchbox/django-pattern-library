# Overview

This document contains information for anyone wishing to contribute to the project.

If you would like to contribute, you will follow these steps:

- [Set up a local build](#how-to-set-up-a-local-build)
- [Make your changes](#making-changes)
- [Running the tests](#running-the-tests)
- [Writing tests](#writing-tests)
- [Submit your changes for code review](#code-review)
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

We use [Poetry](https://poetry.eustace.io/docs/) to manage Python dependencies, so make sure you've got it installed.

Then you can install the dependencies and run the test app:

```sh
poetry install  # installs the library and its dependencies in editable mode
poetry run ./runserver.sh  # runs the test app using the Django development server
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
$ poetry run ./runtests.py
```

To run the tests using different Python versions (currently 3.6 and 3.7, which you'll need to have installed on your machine), use `tox`.
You'll need to install `tox` first, please see the documentation here: https://tox.readthedocs.io/en/latest/install.html


## Writing tests

There is a simple test pattern library app in the `tests/` folder. The tests modules themselves and are `tests/tests`.


## Code review

Create a pull request with your changes so that it can be code reviewed by a core developer. Ensure that you give a summary with the purpose
of the change and any steps that the reviewer needs to take to test your work. Please provide unit tests for your work, if possible!


## Releasing a new version

On the `master branch`:

1. Bump the release number in `pyproject.toml`
2. Update the change log found at `CHANGELOG.md`
3. Commit and tag the release: `git tag -a v0.1.14 -m "Release version v0.1.14"`
4. Check that your working copy is clean by running `git clean -dxn -e __pycache__`.
   Any files returned by this command should be removed before continuing to prevent them being included in the build.
5. Install the locked versions of the `node` dependencies and run the production build:
   ```sh
   $ npm ci
   $ npm run build
   ```
6. Package the new version using `poetry build`
7. Test the newly-built package by installing it an existing project using `django-pattern-library` and verifying
   everything is as you expect it to be.
8. Upload the latest version to PyPI (requires credentials): `poetry publish`
