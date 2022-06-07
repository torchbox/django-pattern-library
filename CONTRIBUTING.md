# Contributing guidelines

This document contains information for anyone wishing to contribute to the project.


## Installation

The repo includes a simple test application that can be run to develop the pattern library itself. Give it a try by [opening django-pattern-library in Gitpod](https://gitpod.io/#https://github.com/torchbox/django-pattern-library), or follow the instructions below for a local setup.

First, clone the repo:

```sh
git clone git@github.com:torchbox/django-pattern-library.git
cd django-pattern-library
```

Once you have the code, there are several ways of running the project:

- [In a VS Code devcontainer](#vs-code-devcontainer)
- [In Docker, via docker-compose](#docker-compose)
- [Locally, with Poetry](#run-locally-with-poetry)

### VS Code devcontainer

For users of Docker and VS Code, there is a [devcontainer](https://code.visualstudio.com/docs/remote/containers) setup included in the repository
that will automatically install the Python dependencies and start the frontend tooling.

Once the container is built, open a terminal with VS Code and run `django-admin runserver` and click the URL (normally http://127.0.0.1:8000/) to open the app in your browser. You'll see a 404 page, because there's nothing at `/`, add `pattern-libary/` to the end of the URL to view the demo app.

### `docker-compose`

First [install Docker and docker-compose](https://docs.docker.com/compose/install/), and make sure Docker is started. Then:

```sh
# Install the front-end tooling in the docker container:
docker-compose run frontend npm ci
# Bring up the web container and run the front-end tooling in watch mode:
docker-compose up
# Run the development server:
docker-compose exec web django-admin runserver 0.0.0.0:8000
```

Once the server is started, the pattern library will be available at `http://localhost:8000/`.

### Run locally with Poetry

We use [Poetry](https://python-poetry.org/docs/) to manage Python dependencies, so make sure you've got it installed.

Then you can install the dependencies and run the test app:

```sh
poetry install
# Start the server for testing:
poetry run django-admin runserver --settings=tests.settings.dev --pythonpath=.
# Or to try out the render_patterns command:
poetry run django-admin render_patterns --settings=tests.settings.dev --pythonpath=. --dry-run --verbosity 2
```

## Front-end tooling

If you want to make changes to the front-end assets (located in the `pattern_library/static/pattern_library/src` folder), you'll need to ensure the tooling is set up in order to build the assets.

If you are using Docker, you will already have the tooling set up and running in watch mode. You can view the logs with `docker-compose logs frontend` from your host machine.

Otherwise, we recommend using [`nvm`](https://github.com/nvm-sh/nvm):

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

## Documentation

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

On the `main` branch:

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

8. Upload the latest version to PyPI (requires credentials, ask someone named in `pyproject.toml` authors): `poetry publish`
