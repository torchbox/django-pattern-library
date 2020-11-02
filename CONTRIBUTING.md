# Contributing guidelines

This document contains information for anyone wishing to contribute to the project.

## Install

The repo includes a simple test application that can be run locally to develop the pattern library itself.
First, clone the repo:

```sh
git clone git@github.com:torchbox/django-pattern-library.git
cd django-pattern-library
```

### Run a local build with Poetry

We use [Poetry](https://poetry.eustace.io/docs/) to manage Python dependencies, so make sure you've got it installed.

Then you can install the dependencies and run the test app:

```sh
poetry install
# Start the server for testing:
poetry run django-admin runserver --settings=tests.settings.dev --pythonpath=.
# Or to try out the render_patterns command:
poetry run django-admin render_patterns --settings=tests.settings.dev --pythonpath=. --dry-run --verbosity 2
```

### Run a local build with docker

First [install Docker and docker-compose](https://docs.docker.com/compose/install/), and make sure Docker is started.

```sh
# Install the front-end tooling in the docker container:
docker-compose run frontend npm ci
# Start the dev server and run the front-end tooling in watch mode:
docker-compose up
```

Once the server is started, the pattern library will be available at `http://localhost:8000/pattern-library/`.

### Front-end tooling

If you want to make changes to the front-end assets (located in the `pattern_library/static/pattern_library/src` folder), you'll need to ensure the tooling is set up in order to build the assets.

If you are using Docker you will already have the tooling set up and running in watch mode. Otherwise,

```sh
# Install the correct version of Node
nvm install
# Install Node dependencies locally
npm install
# Build the assets
npm run build
# Watch files and build as needed
npm run start
```

### Documentation

The project’s documentation website is built with [MkDocs](https://www.mkdocs.org/).

```sh
# One-off build.
poetry run mkdocs build --strict
# Rebuild the docs as you work on them
poetry run mkdocs serve
```

## Running the tests

To run the python tests, use the script in the root of the repo:

```sh
poetry run ./runtests.py
```

To run the tests using different Python versions, use [`tox`](https://tox.readthedocs.io/). Note your Python versions will need to be installed on your machine, for example with [pyenv](https://github.com/pyenv/pyenv).

## Writing tests

There is a simple test pattern library app in the `tests/` folder. The tests modules themselves and are `tests/tests`.

## Code review

Create a pull request with your changes so that it can be code reviewed by a maintainer. Ensure that you give a summary with the purpose of the change and any steps that the reviewer needs to take to test your work. Please make sure to provide unit tests for your work.

## Releasing a new version

On the `master` branch:

1. Bump the release number in `pyproject.toml`
2. Update the CHANGELOG
3. Commit and tag the release:
   ```sh
   git commit -m "Updates for version 0.1.14"
   git tag -a v0.1.14 -m "Release version v0.1.14"
   git push --tags
   ```
4. Check that your working copy is clean by running:
   ```sh
   git clean -dxn -e __pycache__
   ```
   Any files returned by this command should be removed before continuing to prevent them being included in the build.
5. Install the locked versions of the `node` dependencies and run the production build.

   You can either do this directly on your local machine:

   ```sh
   npm ci
   npm run build
   ```

   Or, via the docker container:

   ```sh
   docker-compose run frontend npm ci
   docker-compose run frontend npm run-script build
   ```

6. Package the new version using `poetry build`

7. Test the newly-built package:
   Find the file ending in `.whl` in the `dist` directory
   Copy it to a test local build.
   Run this to install it on the test build:

   ```sh
   pip install django_pattern_library-0.2.6-py3-none-any.whl
   ```

   Verify that the pattern library is working as you expect it to on your local build.

8. Upload the latest version to PyPI (requires credentials): `poetry publish`
