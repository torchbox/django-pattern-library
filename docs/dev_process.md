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
$ git clone [repo url]
$ cd django-pattern-library
```


### Run a local build without docker
We use [Poetry](https://poetry.eustace.io/docs/) to manage Python dependencies, so make sure you've got it installed.

Then you can install the dependencies and run the test app:

```sh
$ poetry install  # installs the library and its dependencies in editable mode
$ poetry run 'django-admin runserver --settings=tests.settings --pythonpath=.'  # runs the test app using the Django development server
```

### Run a local build with docker
First ensure you have Docker Compose installed and running - see https://docs.docker.com/compose/install/

Install the front-end tooling in the docker container:
```sh
$ docker-compose run frontend npm ci
```

Start the dev server and run the front-end tooling in watch mode:
```sh
$ docker-compose up
```

Once the server is started, the pattern library will be available at `http://localhost:8000/pattern-library/`.


## Making changes

To make changes you need to edit the files under the `pattern_library` folder. You'll be able to see your changes reflected on the localhost.


### Front-end tooling
If you want to make changes to the front-end assets (located in the `pattern_library/static/pattern_library/src` folder), you'll need to enusre
 the tooling is set up in order to build the assets.

If you are [using docker](#run-a-local-build-with-docker) you will already have
the tooling set up and running in watch mode. Otherwise read on to get the tooling set up.

Node version 8 is required for this. If you're using `nvm` to manage node on your machine there's
a `.nvmrc` that means you can run `nvm use` to activate the correct version of node.

To install dependencies and build the assets, run the following commands:

```sh
$ npm install
$ npm run build
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
2. Update the change log found at `CHANGELOG.md` - see https://keepachangelog.com/en/1.0.0/ for guidelines
3. Commit and tag the release:
   ```sh
   $ git commit -m "Updates for version 0.1.14"
   $ git tag -a v0.1.14 -m "Release version v0.1.14"
   $ git push --tags
   ```
4. Check that your working copy is clean by running:
   ```sh
   $ git clean -dxn -e __pycache__
   ```
   Any files returned by this command should be removed before continuing to prevent them being included in the build.
5. Install the locked versions of the `node` dependencies and run the production build.

   You can either do this directly on your local machine:
   ```sh
   $ npm ci
   $ npm run build
   ```

   Or, via the docker container:
   ```sh
   $ docker-compose run frontend npm ci
   $ docker-compose run frontend npm run-script build
   ```
6. Package the new version using `poetry build`

7. Test the newly-built package:
   Find the file ending in `.whl` in the `dist` directory
   Copy it to a test local build.
   Run this to install it on the test build:
   ```sh
   $ pip install django_pattern_library-0.2.6-py3-none-any.whl
   ```
   Verify that the pattern library is working as you expect it to on your local build.

8. Upload the latest version to PyPI (requires credentials): `poetry publish`
